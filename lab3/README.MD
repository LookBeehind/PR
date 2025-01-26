# Dicol Oliviu
### TI-211 FR
### Lab 3 - Aplicație de tip client DNS
### ----------------------------------------------------------------------------------------------------------------------------
## To run the app, you need to provide the arguments:
1. `-u <ip>` to set a custom DNS
2. `-d <domain>` to resolve a domain
3. `-i <ip>` to resolve an IP
## It is possible to combine.
### A list of available commands to test:
`python dns_resolver.py -u 8.8.8.8 -d google.com`

`python dns_resolver.py -d google.com`

`python dns_resolver.py -u 8.8.8.8 -i 172.217.18.14`

`python dns_resolver.py -i 172.217.18.14`

### However, if you specify both `<ip>` and `<domain>`, the last argument will process.
`python dns_resolver.py -u 8.8.8.8 -i 172.217.18.14 -d google.com`

### Error handling tests:
#### Invalid `<ip>`:
`python dns_resolver.py -i 1.2.3.999`

#### Invalid `<domain>`:
`python dns_resolver.py -d vasea.vasea`

#### Invalid `<dns>`:
`python dns_resolver.py -u 1.2.3.999`

### Enjoy <3