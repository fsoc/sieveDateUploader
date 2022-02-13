# SDU - Sieve Date Uploader
Uploads a sievescript blocking date-based catch-all email prefixes.
Also has the added functionality to block specific email aliases.

A typical use-case is when you shop online and dont want to get any spam months or years after the purchase. Just type in an email like user.12.2024@example.com, so if you shop in november then the tracking code for shipping will be delivered to you. But as soon as december hits, any further emails will be send to the spam-folder.

There is also the possibility to use a "mv" suffix to send emails copies to another inbox in the domain.

## Help
python slib.py -h

## Usage
python slib.py -d domain -f banfile -u username -p password -m copydestination

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
