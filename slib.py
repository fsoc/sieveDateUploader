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
        if (y < now.year):
            suffixes.append(y)
    return suffixes

def genAdrs(domain, startYear):
    adrs = []
    for suffix in genSuffixes(startYear):
        adr = "\".*%s@%s\"" % (suffix, domain)
        adrs.append(adr)
    return adrs


def generateCalendarScript(domain, startYear):
    adrs = ", \n".join(genAdrs(domain, startYear))

    script = """require ["fileinto","imap4flags", "regex"];
if address :regex "to" [%s]
{
    setflag "\\\\Seen";
    fileinto "Junk";
}"""
    return script % (adrs)

def generateBanFileScript(banFile, domain):
    adrs = genBanFileAdrs(banFile, domain)

    script = """

if address :is "to" [%s]
{
    setflag "\\\\Seen";
    fileinto "Junk";
}"""
    return script % (adrs)

def genBanFileAdrs(banFile, domain):
    #banFileAdrs = parseFile(banFile)
    lines = []
    with open(banFile) as f:
        lines = [line.rstrip() for line in f]

    lines = map(lambda x: "\"%s@%s\"" % (x, domain), lines)

    return ", \n".join(lines)

def generateScripts(domain, banFile, startYear):
    s = generateCalendarScript(domain, startYear)
    if (banFile is not None):
        s = s + generateBanFileScript(banFile, domain)
    return s

parser = ArgumentParser()
parser.add_argument("-d", dest="domain", help="domain name", required=True)
parser.add_argument("-f", dest="banFile", help="explicit ban file")
parser.add_argument("-u", dest="usr", required=True)
parser.add_argument("-p", dest="pwd", required=True)

args = parser.parse_args()


print(generateScripts(args.domain, args.banFile, 2016))
setScript(args.usr, args.pwd, generateScripts(args.domain, args.banFile, 2016))
