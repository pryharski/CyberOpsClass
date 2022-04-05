
import glob
import os
import hashlib
import io

#https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
#https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
#https://www.programiz.com/python-programming/examples/hash-file


#Change this option here to choose what path the program should run on
#lookPaths = ["bin", "etc", "lib32", "opt", "run", "sys", "boot", "lib64", "media", "sbin", "var", "home", "lib", "libx32", "mnt", "root", "srv"]
#lookPaths = ["Test"]

#Create working dictionary
dataDict = {}

#Open and read data frame file
dataFile = open("Data.txt", "r+")
dataLines = dataFile.readlines()
fileList = []

#Add data from file into dictionary
for line in dataLines:
	data = line.split(",")
	#print(data)
	dataDict[data[0]] = [data[1], data[2][:-1]]
	fileList.append(data[0])
	#print(line)
	
#for key in dataDict:
#	print(key, dataDict[key])

#Paths where the program will run
changeList = []
accessList = []
newList = []
readList = []
index = 0
for path in lookPaths:
	os.chdir("/home/kali/Desktop")
	os.chdir(path)
	#Prints working directory
	print(os.getcwd())
	
	#Looks through all folders recursively
	for filepath in glob.iglob("**/*", recursive=True):
		
		#If it is a file, it will process it
		if os.path.isfile(filepath):
		
			#Opens the file as bytes
			fileOpen = open(filepath, "rb")
			fileRead = fileOpen.read()
			
			#Computes the hash and access time
			shaHash = hashlib.sha256(fileRead)
			shaOut = shaHash.hexdigest()
			timeAccess = os.path.getatime(filepath)
			
			#Temp list of values
			tempList = [filepath, shaOut, timeAccess]
			readList.append(filepath)
			
			#Checks to see if file new, changed, or accessed
			if filepath in dataDict:
				if shaOut != dataDict[filepath][0]:
					changeList.append(tempList)
					dataDict[filepath][0] = shaOut
				if str(timeAccess) != dataDict[filepath][1]:
					accessList.append(tempList)
					dataDict[filepath][1] = str(timeAccess)
			elif filepath not in dataDict:
				newList.append(tempList)
				dataDict[filepath] = [shaOut, timeAccess]
			
			
#Checks to see if file have been deleted
deleteList = []
for item in fileList:
	if item not in readList:
		deleteList.append(item)
		
#Prints any files that are new, changed, or accessed
print("\n")
eventValue = False
if len(changeList) > 0:
	print("Changed files:")
	for item in changeList:
		print(item)
	print("\n")
	eventValue = True
if len(accessList) > 0:
	print("Accessed files:")
	for item in accessList:
		print(item)
	print("\n")
	eventValue = True
if len(newList) > 0:
	print("New Files:")
	for item in newList:
		print(item)
	print("\n")
	eventValue = True
if len(deleteList) > 0:
	print("Deleted Files:")
	for item in deleteList:
		print(item)
		del dataDict[item]
	print("\n")
	eventValue = True

#Null case for when no events were detected
if not eventValue:
	print("No events occured")

#Cuts all old information from data file and resets cursor to the start to write new data
dataFile.truncate(0)
dataFile.seek(0)
for key in dataDict:
	dataFile.write(key + "," + dataDict[key][0] + "," + str(dataDict[key][1]) + "\n")
dataFile.close()










