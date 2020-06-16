#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
import pyspark.sql.functions as f
from pyspark.sql.functions import udf
from pyspark.sql.types import *

def getSparkSessionInstance(sparkConf):
	if ('sparkSessionSingletonInstance' not in globals()):
		globals()['sparkSessionSingletonInstance'] = SparkSession\
			.builder\
		.config(conf=sparkConf)\
		.getOrCreate()
	return globals()['sparkSessionSingletonInstance']

afinn_file_name = '/Users/phani/code/spark/AFINN-111.txt'
afinn = dict(map(lambda w_s: (w_s[0], int(w_s[1])), [
			ws.strip().split('\t') for ws in open(afinn_file_name) ]))
#afinn = {"Mohammed" :100, "Sameer":50}

if __name__ == "__main__":
	sc = SparkContext(appName="SentiTweetApp")
	lines = sc.textFile("tweet_com")

    # Convert RDDs of the words DStream to DataFrame and run SQL query
	def process(time, rdd):
		print("========= %s =========" % str(time))

		try:
			# Get the singleton instance of SparkSession
			spark = getSparkSessionInstance(rdd.context.getConf())

			# Convert RDD[String] to RDD[Row] to DataFrame
			rowRdd = rdd.map(lambda w: Row(word=w))
			wordsDataFrame = spark.createDataFrame(rowRdd)
			my = spark.createDataFrame(rdd.map(lambda w: (w.split('\t'))))
			def my_udf_1(a):
				word_list = a.split()
				freq = []
				for w in word_list:
					freq.append(word_list.count(w))
				score = 0.0
				for elem in list(zip(word_list, freq)):
					score += afinn.get(elem[0],0)*elem[1]
				return score

			spark.udf.register("my_udf_1",my_udf_1, FloatType())
			my = my.rdd.map(lambda x: (x[0], x[1], my_udf_1(x[1]), x[2])).toDF(['A','B','C', 'D'])
			my.show()
			my.write.csv('/Users/phani/code/spark/Tweets.'+str(time)+'.csv')
			return;
			#my = my.withColumn("x7", my["_2"])
			my_func = udf(lambda x : x.flatMap(lambda x: x).map(lambda z: (z,1).reduceByKey(lambda x,y: x+y)))
			my = my.withColumn('wordcount', my_func(f.col('_2')))
			#dy = my.select('_2').rdd.map(lambda row: tuple(row.split(' '))).map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)
			#print(dy.take(2))
			my.show()
            
			# Creates a temporary view using the DataFrame.
			wordsDataFrame.createOrReplaceTempView("words")
            
			# Do word count on table using SQL and print it
			wordCountsDataFrame = \
					spark.sql("select word, count(*) as total from words group by word")
			wordCountsDataFrame.show()
		except Exception as e:
			print(e)
			pass
    
	lines.foreachRDD(process)
