from pyspark import SparkContext, SparkConf
from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as psql
from pyspark.sql.functions import desc
import glob, os
import json
import sys
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("SimpleApp")
sc = SparkContext(conf=conf)

os.chdir("/home/ec2-user/spark/csv_files")
curr_dir = os.getcwd()

keywords_lines = []
all_lines = []

search_string = sys.argv[1]
count = 0
'''
print(curr_dir)
for file_dir in glob.glob("*.csv"):
	in_dir = curr_dir + "/" + file_dir
	dir_str = in_dir + "/"
	dir_list = os.listdir(dir_str)
	num_files = len(dir_list)
	if num_files == 0:
		continue
	dir_str = dir_str + "*"
	print(dir_str)
	textFile = sc.textFile(dir_str)
	words = textFile.flatMap(lambda line: line.split("\n"))

	lwords = words.collect()
	all_lines = all_lines + lwords

	search_lines = words.filter(lambda line: search_string in line)

	llines = search_lines.collect()

	keywords_lines = keywords_lines + llines

	count = count + 1

	if count == 100:
		break
'''
spark = SparkSession(sc)
sqlContext = SQLContext(sc)

dir_str = curr_dir + '/*/*'
print(dir_str)

textFile = sc.textFile(dir_str)
words = textFile.flatMap(lambda line: line.split("\n"))

search_lines = words.filter(lambda line: search_string in line)
search_lines.take(5)
print("Search done")

search_df = spark.createDataFrame(search_lines.map(lambda w: (w.split(','))))

search_df = search_df.rdd.map(lambda x: (x[0], x[1])).toDF(['rating', 'tweet'])
print("creating data frame done")

search_df.createOrReplaceTempView("Sentiments")
print("Created Gobal view")

#spark.sql("SELECT count(*) from Sentiments").show(10)

search_df_new = search_df.where(search_df['rating'] > 0)
search_df_new.show(10)

search_df_new.orderBy(desc('rating')).show(5)
print(sum)

exit()

search_df_new.createOrReplaceTempView("SearchRes")
print("Created Gobal view")

spark.sql("SELECT * from SearchRes").show()

#pos_count = search_df_new.count()
#print(pos_count)

#search_lines = search_df_new.collect()
#print("collect done")

#neg_count = spark.sql("select * from global_temp.Setiments where 'rating' > 0").count()
#print(neg_count)

neg_count = search_df.filter(psql.col('rating') < 0).count()
print("negative count")

pos_count = search_df.filter(psql.col('rating') > 0).count()
print("positive count")

eq_count = search_df.filter(psql.col('rating') == 0).count()
print("zero count")

os.chdir("/home/ec2-user/spark")
result_file = open('results.json', 'w')

dict = {}

dict[search_string] = pos_count, neg_count, eq_count

print(dict)

json_str_keyword = json.dumps(dict)

trends_file = open('trends.txt', 'r')
trends_str = trends_file.readline()
trends_file.close()

print(trends_str)

trends_list = trends_str.strip('][').split(', ')

trend_dict = {}
for trend in trends_list:
	trend_str = str(trend.strip('\''))
	search_lines_trend = words.filter(lambda line: trend_str in line)

	if search_lines_trend.isEmpty():
		continue

	search_df_trend = spark.createDataFrame(search_lines_trend.map(lambda w: (w.split(','))))
	search_df_trend = search_df_trend.rdd.map(lambda x: (x[0], x[1])).toDF(['rating', 'tweet'])

	neg_count = search_df_trend.filter(psql.col('rating') < 0).count()
	pos_count = search_df_trend.filter(psql.col('rating') > 0).count()
	eq_count = search_df_trend.filter(psql.col('rating') == 0).count()

	trend_dict[trend_str] = pos_count, neg_count, eq_count

json_str_trend = json.dumps(trend_dict)

print(trend_dict)
print(dict)

result_file.write(json_str_trend)
result_file.write(json_str_keyword)

'''
llines = search_lines.collect()
print("Search collect done")
keywords_lines = keywords_lines + llines
'''
'''
os.chdir("/Users/phani/code/spark")
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
			rating = str_line[str_len-15:str_len-13]
			if rating[0] == '-':
				rating = str_line[str_len-15:str_len-13]
			else:
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
for line in keywords_lines:
	str_line = str(line)
	str_len = len(str_line)
	tweet = str_line[0:str_len-15]
	rating = str_line[str_len-15:str_len-13]
	if rating[0] == '-':
		rating = str_line[str_len-15:str_len-13]
	else:
		rating = str_line[str_len-14:str_len-13]
	rating = int(rating)

	if rating < 0:
		rating_n = rating_n + 1
	elif rating > 0:
		rating_p = rating_p + 1
	elif rating == 0:
		rating_e = rating_e + 1

dict = {}

dict[search_string] = rating_p, rating_n, rating_e

values = [rating_p, rating_n, rating_e]

print(dict)

json_str = json.dumps(dict)
result_file.write(json_str)

print(json_str)

'''
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
