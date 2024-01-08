import sievelib
import datetime
from argparse import ArgumentParser
from sievelib.managesieve import Client

def getCli(usr, pwd):
    client = Client("imap.mailbox.org")
    conn = client.connect(usr, pwd, starttls=True, authmech="LOGIN")
    check(conn, "connection")
    return client

def check(retVal, op):
    if (retVal == False):
        print("%s failed" % op)
        exit(1)

def setScript(usr, pwd, script):
    cli = getCli(usr, pwd)

    put = cli.putscript("default", script)
    check(put, "putscript")

    setActive = cli.setactive("default")
    check(setActive, "setActive")

    print(script)

def genSuffixes(startYear):
    now = datetime.datetime.now()
    suffixes = []

    for y in range(startYear, now.year + 1):
        if (y == now.year):
            monthRange = 12
            monthRange = now.month
            for m in range(1, monthRange + 1):
                if (m < 10):
                    m = "0"+ str(m)
                suffixes.append("%s.%s" % (m, y))
        if (y < now.year): # and m == undefined or y < now.year):
            suffixes.append(y)
    return suffixes

def genAdrs(domain, startYear):
    adrs = []
    for suffix in genSuffixes(startYear):
        adr = "\".*%s(.mv)?@%s\"" % (suffix, domain)
        adrs.append(adr)
    return adrs

def generateHeader():
    return """
require ["copy", "fileinto","imap4flags", "regex", "reject", "editheader", "variables"];"""

def generateCalendarScript(domain, startYear):
    adrs = ", \n".join(genAdrs(domain, startYear))

    script = """
if address :regex ["to","delivered-to"] [%s]
{
    if address :regex ["to","delivered-to"] [".*\.bf\..*"] {
        reject "I hereby request a GDPR removal from all your systems.";
        stop;
    } else {
        setflag "\\\\Seen";
        fileinto "Junk";
        stop;
    }
}"""
    return script % (adrs)

def generateCopyScript(domain, copyName):

    script = """
    if address :regex ["to","delivered-to"] [".*\.mv(\..*)?@%s"]
{
    if header :matches "Subject" "*" {
        set "subject" "${1}";
    }
    if header :matches "To" "*" {
        set "to" "${1}";
    }

    deleteheader "Subject";
    addheader :last "Subject" " ${subject} [redir, to:${to}]";
    redirect :copy "%s@%s";
    stop;
}"""
    return script % (domain, copyName, domain)

def generateBanFileScript(banFile, domain):
    adrs = genBanFileAdrs(banFile, domain)

    script = """
if address :is ["to","delivered-to"] [%s]
{
    reject "I hereby request a GDPR removal from all your systems.";
    stop;
}"""
    return script % (adrs)

def genBanFileAdrs(banFile, domain):
    #banFileAdrs = parseFile(banFile)
    lines = []
    with open(banFile) as f:
        lines = [line.rstrip() for line in f]

    lines = map(lambda x: "\"%s@%s\"" % (x, domain), lines)

    return ", \n".join(lines)

def addCustom(domain):
    return """
if address :regex ["to","delivered-to"] ["pc@%s"]
{
    setflag "\\Seen";
    fileinto "pc";
    stop;
}""" % domain

def generateScripts(domain, banFile, startYear, copyName):
    s = generateCalendarScript(domain, startYear)
    if (banFile is not None):
        s = generateBanFileScript(banFile, domain) + s
    return generateHeader() + s + generateCopyScript(domain, copyName) + addCustom(domain)

parser = ArgumentParser()
parser.add_argument("-d", dest="domain", help="domain name", required=True)
parser.add_argument("-f", dest="banFile", help="explicit ban file")
parser.add_argument("-u", dest="usr", required=True)
parser.add_argument("-p", dest="pwd", required=True)
parser.add_argument("-m", dest="copyName", required=True)

args = parser.parse_args()


print(generateScripts(args.domain, args.banFile, 2016, args.copyName))
setScript(args.usr, args.pwd, generateScripts(args.domain, args.banFile, 2016,args.copyName))
