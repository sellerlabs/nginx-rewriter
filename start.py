#!/usr/bin/python
from yaml import load,dump
import urllib2
import select
import os
import sys
from subprocess import PIPE, Popen

home = os.path.expanduser("~")
confd = '/etc/nginx/conf.d/'

print "preparing to start nginx-rewriter ..."
config_url = os.getenv('CONFIG_URL',"https://raw.githubusercontent.com/sellerlabs/nginx-rewriter/master/rewrite-rules.example.yaml")
print "CONFIG_URL: " + config_url

response = urllib2.urlopen(config_url)
config = load(response)

print "loading domains"
for domain in config:
  print domain
  c = open(confd + domain + ".conf", 'w')
  c.write('server {\n  server_name ' + domain + ';\n')
  print "adding rules"
  for rule in config[domain]['rewriterules']:
    print rule
    c.write('  rewrite ' + rule + '\n')
  c.write('}')
  c.close

print "testing config..."
sys.stdout.flush()
p = Popen(["/usr/sbin/nginx","-t"], stderr=sys.stderr, stdout=sys.stdout)
p.wait()
print "starting nginx in the foreground"
sys.stdout.flush()
p = Popen(["/usr/sbin/nginx","-g", "daemon off;"], stderr=sys.stderr, stdout=sys.stdout)
p.wait()
