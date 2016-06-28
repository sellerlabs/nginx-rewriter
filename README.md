# nginx-rewriter
feed this container multiple domains and their rewrite rules via a YAML file to have nginx rewrite all of your domains to their real homes.

## Environment Variables
CONFIG_URL - URL of the YAML config file

## Example Configuration File
    ---
    email: support@yourdomain.com
    target_domains:
      google.com:
        redir_domains:
          - foogle.com
          - hoogle.com
          - toogle.com
      gmail.com:
        redir_domains:
          - fmail.com
          - hmail.com
          - tmail.com
