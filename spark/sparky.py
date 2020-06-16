from pyspark import SparkContext, SparkConf
from pyspark import SparkConf
from pyspark.sql import SparkSession

conf = SparkConf().setAppName("SimpleApp")
sc = SparkContext(conf=conf)

textFile = sc.textFile("tweet_com")

words = textFile.flatMap(lambda line: line.split("\n"))

lwords = words.collect()

afinn_file_name = 'AFINN-111.txt'
afinn = dict(map(lambda w_s: (w_s[0], int(w_s[1])), [ 
            ws.strip().split('\t') for ws in open(afinn_file_name) ]))

print("****************************")
for word in lwords:
	print(word)
print("****************************")
