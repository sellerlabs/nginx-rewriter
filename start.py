#!/usr/bin/python
from yaml import load,dump
import urllib2
import select
import os
import sys
from subprocess import PIPE, Popen

class NginxRewriter(object):
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.confd = '/etc/nginx/conf.d/'
        self.webroot = '/var/www/nginx-rewriter/'
        config_url = os.getenv('CONFIG_URL',"https://raw.githubusercontent.com/sellerlabs/nginx-rewriter/master/rewrite-rules.example.yaml")
        response = urllib2.urlopen(config_url)
        self.config = load(response)
        self.email_addr = self.config['email']
        self.target_domains = self.config['target_domains']

        self.gen_config()

    def gen_cert(self, redir_domains):
        print redir_domains
        command = Popen(["/usr/bin/certbot","certonly","--staging","--dry-run","--email",self.email_addr,"-n","--agree-tos","-t","--standalone","--standalone-supported-challenges","http-01","-d",redir_domains])
        command.wait()

    def gen_config(self):
        print "loading domains"

        for target_domain in self.target_domains:
            redir_domains = self.target_domains[target_domain]['redir_domains']
            redir_domains_spaces = "  ".join(redir_domains)
            redir_domains_csv = ",".join(redir_domains)

            p = Popen(["mkdir",self.webroot+target_domain])
            p.wait()

            print self.webroot+target_domain
            self.gen_cert(redir_domains_csv)

            c = open(self.confd + target_domain + ".conf", 'w')

            print "Nginx config %s" % target_domain
            server_conf = """
server {
    listen 80;
    server_name %s;
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name %s;
    return 301 https://%s$request_uri;

    ssl_certificate /etc/letsencrypt/live/%s/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/%s/privkey.pem;
}
            """ % (redir_domains_spaces, redir_domains_spaces, target_domain, redir_domains[0], redir_domains[0])

            print server_conf

            c.write(server_conf)
            c.close

        self.start_nginx()

    def start_nginx(self):
        print "testing config..."
        sys.stdout.flush()
        p = Popen(["/usr/sbin/nginx","-t"], stderr=PIPE, stdout=PIPE)
        p.wait()
        output = p.communicate()[1]
        print output
        if "test failed" in output:
            # Exit program with status code "1" if tests failed.
            sys.exit(1)
        print "starting nginx in the foreground"
        sys.stdout.flush()
        p = Popen(["/usr/sbin/nginx","-g", "daemon off;"], stderr=sys.stderr, stdout=sys.stdout)
        p.wait()

if __name__ == "__main__":
    NginxRewriter()
