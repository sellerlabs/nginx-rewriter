# nginx-rewriter
feed this container multiple domains and their rewrite rules via a YAML file to have nginx rewrite all of your domains to their real homes.  SSL is not yet supported.

## Environment Variables
CONFIG_URL - URL of the YAML config file

## Config File Format
    ---
    domain1:
      rewriterules:
        - sourcepattern destinationpattern type

## Example Configuration File
    ---
    example.cn:
      rewriterules:
        - ^/images/(.*)$ http://images.example.com/$1 redirect;
        - ^/js/(.*)$ http://scripts.example.com/$1 permanent;
    another.com:
      rewriterules:
        - ^(.*)$ https://thirdname.com/$1 permanent;
