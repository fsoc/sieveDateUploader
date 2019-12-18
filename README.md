# SDU - Sieve Date Uploader
Uploads a sievescript blocking date-based catch-all email prefixes.
Also has the added functionality to block specific email aliases.

## Help
python slib.py -h

## Usage
python slib.py -d domain -f banfile -u username -p password

## Banfile
add one entry per line like so:
```
foo
bar
```

and it will block foo@domain, bar@domain


## Example
This is how an sieve-config uploaded might look like:
``` 
require ["fileinto","imap4flags", "regex"];
if address :regex "to" [".*2016@example.com",
   ".*2017@example.com",
   ".*2018@example.com",
   ".*01.2019@example.com",
   ".*02.2019@example.com",
   ".*03.2019@example.com",
   ".*04.2019@example.com",
   ".*05.2019@example.com",
   ".*06.2019@example.com",
   ".*07.2019@example.com",
   ".*08.2019@example.com"]
{
  setflag "\\Seen";
  fileinto "Junk";
}
if address :is "to" ["webshop1@example.com",
   "spamhere@example.com",
]
{
  setflag "\\Seen";
  fileinto "Junk";
}
``` 
