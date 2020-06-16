import tweepy
import json
import sys
from datetime import date
import time
import socket
import re

# API credentials here
consumer_key = 'jp7svmBA1OJkvNpiAmP1A2lju'
consumer_secret = 'x8BkvQXMqHP1Ddgilu1ZM1Mq3ZVA3fNiaHCjCbongKIylrSA3f'
access_token = '831144404274524162-k1Jo8ee9o5wZ7rSoDLModMoDVsMzVwE'
access_token_secret = 'byZSUiQo3s7iWSR1G2U8JapGjDiI8LMGnikJyUh8GbdiJ'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

host = 'localhost'
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		count_str = "This is junk. Please ignore"
		date_str = str(date.today())
		if hasattr(status, 'retweeted_status'):
			try:
				text = status.retweeted_status.extended_tweet["full_text"]
			except:
				text = status.retweeted_status.text
		else:
			try:
				text = status.extended_tweet["full_text"]
			except AttributeError:
				text = status.text
		
		text = str(text)
		text = text.replace('\n', ' ')
		text=text.encode("ascii", "ignore").decode("ascii")

		str_to_send = count_str + "\t" + text + "\t" + date_str + "\n"

		byte_code = str_to_send.encode()
		conn.send(byte_code)
		

# Where On Earth ID for Brazil is 23424768.
ID = 2352824
 
trends_temp = api.trends_place(ID)

trends_temp = json.loads(json.dumps(trends_temp, indent=1))

trends = []
count = 1;

for trend in trends_temp[0]["trends"]:
	trends.append(trend['name'])
	count = count + 1
	if count == 10:
		break

#print(trends)
f_trends = open('trends.txt', 'w')
trends_str = str(trends).encode("ascii", "ignore").decode("ascii")
f_trends.write(trends_str)
f_trends.close

print("Waiting for stream to connect\n")
conn, addr = s.accept()

print("Stream connected\n")
'''
f = open('tweet_com', 'r')
lines = f.readlines()

count = 0

for line in lines:
	str_line = str(line)
	len_str = len(str_line)
	str_to_send = "jfndjndjn \t" + str_line[0:len_str-1] + "\t ksndjcndsj\n"
	print(str_to_send)
	byte_code = str_to_send.encode()
	conn.sendall(byte_code)
	if count == 5:
		break
	count = count + 1
'''
print("Starting tweepy stream\n")

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode = 'extended')

myStream.filter(languages=['en'], track=trends, is_async=True)

#myStream.filter(follow=["2211149702"])


"""
searchString = "Coronavirus"

cursor = tweepy.Cursor(api.search, q=searchString, count=20, lang="en", tweet_mode='extended')

maxCount = 3
count = 0
for tweet in cursor.items():
    print()
    print("Tweet Information")
    print("================================")
    print("Text: ", tweet.full_text)
    print("Geo: ", tweet.geo)
    print("Coordinates: ", tweet.coordinates)
    print("Place: ", tweet.place)
    print()

    print("User Information")
    print("================================")
    print("Location: ", tweet.user.location)
    print("Geo Enabled? ", tweet.user.geo_enabled)

    count = count + 1
    if count == maxCount:
        break
"""
