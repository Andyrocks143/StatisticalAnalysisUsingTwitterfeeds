import argparse
import oauth2 as oauth
import urllib.request as urllib
import json
import sys
import csv

# See Assignment 1 instructions for how to get these credentials
access_token_key = "18024285-Mf6K8h0TStbEiQkvWdBWl1vUzl1cYDbOZ1xWBdHhE"
access_token_secret = "8P6wuF2LUX4jboCIpVJSY8v3Yogvd5eD4IcfaSZzhTzIC"

consumer_key = "mKQgxQZlFwlOmeDZ4XlvCJJQB"
consumer_secret = "DRe6HR5Ue3uayRJ3AFZK2cXc1XqVY6oHvtFcpVZ8R1dfrqkMAK"
_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def fetch_samples():
    url = "https://stream.twitter.com/1.1/statuses/sample.json?language=en"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        #Here, json.loads is used to make each tweet object into a json object to be accessed later in the term-frequency question.
        print (line.strip().decode('utf-8'))

def fetch_by_terms(term):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    parameters = [("q", term),('count',100)]
    response = twitterreq(url, "GET", parameters)
    print (response.readline())

def fetch_by_user_names(user_name_file):
    #TODO: Fetch the tweets by the list of usernames and write them to stdout in the CSV format
    #CSV writer object.
    writer = csv.writer(sys.stdout) 
    #CSV file header
    header = ["user_name","Tweet"]
    #Writing the header to the csv file.
    writer.writerow(header)
    data=[]
    names = []
    #URL for fetching user tweets.
    myUrl = "https://api.twitter.com/1.1/statuses/user_timeline.json?language=en"
    user_name_file = "data/"+user_name_file
    sn_file = open(user_name_file)
    for line in sn_file:
        names.append(line)
    for name in names:
        #Passing the required parameters.
        myParameters = [('screen_name',name),('count',100)]
        result = twitterreq(myUrl,"GET",myParameters)    
        #Reading the result returned by the api.
        stringr=(result.read().decode('utf-8'))
        jsresult=json.loads(stringr)
        for j in jsresult:
            if isinstance(j,dict):
                data=[name,j['text']]
                writer.writerow(data)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required=True, help='Enter the command')
    parser.add_argument('-term', help='Enter the search term')
    parser.add_argument('-file', help='Enter the user name file')
    opts = parser.parse_args()
    if opts.c == "fetch_samples":
        fetch_samples()
    elif opts.c == "fetch_by_terms":
        term = opts.term
        print (term)
        fetch_by_terms(term)
    elif opts.c == "fetch_by_user_names":
        user_name_file = opts.file
        fetch_by_user_names(user_name_file)
    else:
        raise Exception("Unrecognized command")
