#!/usr/bin/env python
import requests
import argparse
import sys
import hashlib

baseurl = "https://www.speedtest.net/api"
headers = {
    'User-Agent': 'DrWhat Speedtest',
    'Origin': 'https://c.speedtest.net',
    'Referer': 'https://c.speedtest.net/flash/speedtest.swf'
}
payload = {
    'startmode': 'recommendedselect',
    'promo': '',
    'accuracy': '8'
}

print >>sys.stderr, "Fakespeed v1.0 by ShotokanZH"
parser = argparse.ArgumentParser()
parser.add_argument('up',help="Upload speed in kbps",type=int)
parser.add_argument('down',help="Download speed in kbps",type=int)
parser.add_argument('ping',help="Ping RTT in ms",type=int)
parser.add_argument('--server',help="ID of server used for testing (defaults to nearest)",metavar='SERVER_ID',type=int,default=0)

args = parser.parse_args()

server = args.server
if server <= 0:
    print >>sys.stderr, "Retrieving nearest server.."
    r = requests.get("{b}/js/servers?engine=js&https_functional=1".format(b=baseurl), headers=headers)
    if r.status_code != 200:
        print >>sys.stderr, "Something went wrong while retrieving the nearest server!"
        exit(1)
    s = r.json()
    server = s[0]['id']
    print >>sys.stderr
    print >>sys.stderr, "ID:      {i}".format(i=s[0]['id'])
    print >>sys.stderr, "Country: {c}".format(c=s[0]['country'])
    print >>sys.stderr, "Name:    {n}".format(n=s[0]['name'])
    print >>sys.stderr, "Sponsor: {s}".format(s=s[0]['sponsor'])
    print >>sys.stderr

payload['serverid'] = server
payload['recommendedserverid'] = server
payload['upload'] = args.up
payload['download'] = args.down
payload['ping'] = args.ping
h = hashlib.md5()
h.update("{ping}-{up}-{down}-297aae72".format(ping=args.ping,up=args.up,down=args.down))
payload['hash'] = h.hexdigest()

r = requests.post('{b}/api.php'.format(b=baseurl),data=payload,headers=headers)
resultid = r.text.split('&')[0].split('=')[1]

print "https://www.speedtest.net/my-result/{r}".format(r=resultid)
