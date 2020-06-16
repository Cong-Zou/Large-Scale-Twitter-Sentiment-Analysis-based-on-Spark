from pyspark import SparkContext, SparkConf
from pyspark import SparkConf
from pyspark.sql import SparkSession
import glob, os
import json
import sys

conf = SparkConf().setAppName("SimpleApp")
sc = SparkContext(conf=conf)

os.chdir("/home/ec2-user/spark/csv_files")
curr_dir = os.getcwd()

keywords_lines = []
all_lines = []

search_string = sys.argv[1]

print(curr_dir)
for file_dir in glob.glob("*.csv"):
	in_dir = curr_dir + "/" + file_dir
	dir_str = in_dir + "/*" 
	print(dir_str)
	textFile = sc.textFile(dir_str)
	words = textFile.flatMap(lambda line: line.split("\n"))

	lwords = words.collect()
	all_lines = all_lines + lwords

	search_lines = words.filter(lambda line: search_string in line)

	llines = search_lines.collect()

	keywords_lines = keywords_lines + llines

os.chdir("/home/ec2-user/spark/")
trends_file = open('trends.txt', 'r')
trends_str = trends_file.readline()
trends_file.close()

print(trends_str)

trends_list = trends_str.strip('][').split(', ')

trend_dict = {}
for trend in trends_list:
	trend_str = str(trend.strip('\''))

	rating_p = 0
	rating_n = 0
	rating_e = 0
	
	for line in all_lines:
		str_line = str(line)

		if trend_str in str_line:
			str_len = len(str_line)
			rating = str_line[str_len-14:str_len-13]
			rating = int(rating)

			if rating < 0:
				rating_n = rating_n + 1
			elif rating > 0:
				rating_p = rating_p + 1
			elif rating == 0:
				rating_e = rating_e + 1
	
	trend_dict[trend_str] = rating_p, rating_n, rating_e


json_str = json.dumps(trend_dict)
print(trend_dict)
print(json_str)

result_file = open('results.json', 'w')
result_file.write(json_str)

rating_p = 0
rating_n = 0
rating_e = 0

h_rating_p = 0
h_rating_n = 0

h_rating_p_teeet = ''
h_rating_n_tweet = ''

for line in keywords_lines:
	str_line = str(line)
	str_len = len(str_line)
	tweet = str_line[28:str_len-15]
	rating = str_line[str_len-14:str_len-13]
	rating = int(rating)

	if rating < 0:
		rating_n = rating_n + 1
		if rating < h_rating_n:
			h_rating_n_tweet = tweet
	elif rating > 0:
		rating_p = rating_p + 1
		if rating > h_rating_p:
			h_rating_p_tweet = tweet
	elif rating == 0:
		rating_e = rating_e + 1

dict = {}

dict[search_string] = rating_p, rating_n, rating_e

values = [rating_p, rating_n, rating_e]

print(dict)

json_str = json.dumps(dict)
result_file.write(json_str)

print(json_str)

json_str = json.dumps(h_rating_n_tweet)
result_file.write(json_str)

json_str = json.dumps(h_rating_p_tweet)
result_file.write(json_str)

'''

try:
	words = textFile.flatMap(lambda line: line.split("\n"))

	lwords = words.collect()
except Exception as e:
	print(e)

print("****************************")
for word in lwords:
	word = word.encode('ascii', 'ignore')
	print(word)
print("****************************")
'''
