import csv
import json
import subprocess
import sys
#base_path = '/home/ec2-user/search/'
base_path = './'
top5_tweets = 'top5'
bottom5_tweets = 'bottom5'
resultsFile = 'results'
outputfile = 'outfile'
script_file = '/home/ec2-user/spark/search_bash'

subprocess.call([script_file, str(sys.argv[1])])

f = open(base_path + top5_tweets)
result_json = dict()
data = []
for line in f:
    data_line = line.rstrip().split(',')
    data.append(data_line)

#print data
result_json['top5'] = data;
f.close()


f = open(base_path + bottom5_tweets)
data = []
for line in f:
    data_line = line.rstrip().split(',')
    data.append(data_line)

#print data
result_json['bottom5'] = data;
f.close()


f = open(base_path + resultsFile)
data = []
for line in f:
    #data_line = line.rstrip().split(',')
    data.append(line.rstrip())

data.append(float(data[0])/float(data[1]));
result_json['stats'] = data;
f.close()

with open(outputfile, 'w') as f:
    json.dump(result_json, f)





#print json.dumps(result_json)
