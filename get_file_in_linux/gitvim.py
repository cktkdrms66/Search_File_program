#!/usr/bin/env python
import re
import subprocess
import sys
import os

#global value----------------------------------------------
input_data = ""
startPoint = 0
endPoint = 0
wantArr = []
reArr = [".", "^", "$", "*", "+", "?", "{", "}", "[", "]", "\\", "|", "(", ")"]
numArr = ["1","2","3","4","5","6","7","8","9","10"]
#----------------------------------------------------------





#function----------------------------------------------------
		
#wantArr fill
def wantArrFill(isRe, select, allArr):
	global wantArr
	for i in allArr:
		if isRe == True:
			m = select.search(os.path.basename(i))
			if m:
				wantArr.append(i)
		else:
			if select in os.path.basename(i):
				wantArr.append(i)
			

#printData------------------------------------------------------
def printData(isRe, start, select, arr):
	global originalDir
	inArr = []
	num = 0
	print("----------------------")
	for i in arr[start:]:
		if isRe == True:
			m = select.search(os.path.basename(i))
			if m:
				inArr.append(i)
				num = num + 1
				filename = os.path.relpath(i, originalDir)
				print(filename+  "   (" + str(num) + ")")
		else:
			if select in os.path.basename(i):
				inArr.append(i)
				num = num + 1
				filename = os.path.relpath(i, originalDir)
				print(filename + "   (" + str(num) + ")")
		if num == 10:
			printAndSelect(isRe, True, select, inArr)
	printAndSelect(isRe, False, select, inArr) 
			


#-----------------------------------------------------------------------



#print------------------------------------------------------
def printAndSelect(isRe, more, select, inArr):
	global startPoint
	
	print("Enter file shortcut (shown on the righ) or keyword to further refine the search:")
	if more == True:print("If you want to look next files, press \'>\' and Enter.")
	if startPoint != 0: print("If you want to look previous files, press \'<\' and Enter.")
	print("If you want to exit, press \'<<\' and Enter.")
	
	
	while True:
		you_input = raw_input()
	
		if you_input == ">":
			if more == False: 
				print("there are less than 10 files")
				continue
			startPoint = startPoint + 10
			printData(isRe, startPoint, select, wantArr)
		elif you_input == "<":
			if startPoint == 0:
				print("there are no previous files")
				continue
			startPoint = startPoint - 10
			printData(isRe, startPoint, select, wantArr)
		elif you_input == "<<": sys.exit()
		
		for i in numArr[0:len(inArr)]:
			if you_input == i:
				goFile(False, you_input, True, inArr)
		
		isRe = False
		for i in you_input:
			if i in reArr:
				try:
					isRe = True
					you_input = re.compile(you_input)
					break
				except re.error:
					print("the regular expression that you write is wrong!")
					sys.exit()	

		goFile(isRe, you_input, False, inArr)
		return


#gofile--------------------------------------------------------
def goFile(isRe, select, isNum, inArr):
	num = 0
	arr = []
	if isNum == True:
		command = 'vim ' + inArr[int(select) -1]
		subprocess.call(command, shell=True)
		sys.exit()
	else:
		for i in inArr:
			if isRe == True:
				m = select.search(os.path.basename(i))
				if m:
					arr.append(i)
					num = num + 1
			else:
				if select in os.path.basename(i):
					arr.append(i)	
					num = num + 1		
		
		if num == 0:
			print("there is no file or command that you want")
			sys.exit()
		elif num == 1:
			command = 'vim ' + arr[0]
			subprocess.call(command, shell=True)
			sys.exit()
		elif num > 1:
			global startPoint
			global endPoint
			global wantArr
			startPoint = 0;
			endPoint = len(arr)
			wantArr = arr[:]
			printData(isRe, startPoint, select, wantArr)		
		

#------------------------------------------------------------------------
input_data = sys.argv[1]
isRe = False
for i in input_data:
	if i in reArr:
		try:
			input_data = re.compile(input_data)		
			isRe = True
			break
		except re.error:
			print("the regular expression that you write is wrong!")
			sys.exit()

topDir = subprocess.check_output('git rev-parse --show-toplevel',shell=True)
preDir = subprocess.check_output('pwd', shell=True)
originalDir = subprocess.check_output('pwd', shell=True)
while topDir != preDir:
	os.path.abspath(os.curdir)
	os.chdir("..")
	preDir = subprocess.check_output('pwd', shell=True)

result = subprocess.check_output('git ls-files', shell=True)
allArr = result.split("\n")

wantArrFill(isRe, input_data, allArr)
endPoint = len(wantArr)
if endPoint == 0:
	print("there is no file or command that you want")
	sys.exit()
printData(isRe, 0, input_data, wantArr)
#-----------------------------------------------------------------
