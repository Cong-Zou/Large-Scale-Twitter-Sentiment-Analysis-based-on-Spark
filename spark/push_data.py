import sys
import socket

file = sys.argv[1]
host = sys.argv[2]
port = sys.argv[3]
port = int(port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

f = open(file, 'r')
lines = f.readlines()

count = 0

while True:
	conn, addr = s.accept()
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
	conn.close()
