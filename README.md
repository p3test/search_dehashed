# Search dehashed
Script for searching for compromised data (passwords, IP addresses, usernames) via the DeHashed service.

Dehashed API Search Tool v2
```
options:
  -h, --help           show this help message and exit
  -k, --key KEY        Dehashed API key
  -q, --query QUERY    Search value (domain/username/phone/email)
  -o, --output OUTPUT  Output file (default: results.json)
  -a, --append         Append to output file
  --wildcard           Enable wildcard search
  --regex              Enable regex search
  --dedupe             Remove duplicate results
```
Usage:
```python
python3 dehashed.py -h
```

```python
python3 dehashed.py -q DOMAIN.COM -k b3suH4kzm1D9HACXBd
```

