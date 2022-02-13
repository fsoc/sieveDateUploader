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
require ["fileinto","imap4flags", "regex", "reject"];
if address :is "to" ["foo@example.com",
"bar@example.com"]
{
    reject "I hereby request a GDPR removal from all your systems.";
    stop;
}
if address :regex "to" [".*2016@example.com", 
".*2017@example.com", 
".*2018@example.com", 
".*2019@example.com", 
".*01.2020@example.com"]
{
    setflag "\\Seen";
    fileinto "Junk";
    stop;
}
``` 
