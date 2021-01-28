#!/usr/bin/python 
#
# jump_exp.py : Parses C binary files compiled on riscv architecture and structs the call graph of functions 
# where each path is shown by PrC(Program Context) values. 
# 
# Copyright (c) 2021(January) Nagmat Nazarov, Davinci.snu.ac.kr CARES(Computer Architecture and Embedded Systems Lab) 
#
# Python tool to compute PrC(Program Context) values of function calls(jal) for riscv binary files. 
# 
# Usage #python 
# 
# Usage : #python jump_exp.py binary_prog 
#


from subprocess import * 
import os 
import csv 
import sys 
import argparse 
from argparse import ArgumentParser

hex16 = {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}
#Global variables 
PrC = 0 # Program Context Variable
offsetNo = 0 # offset, 
spisok = [] # list for keeping names of functions 
gozleg_funct = ""


#returns range of main function as string
def getMain(c_out):
	esasy = ""
	gecir = 0
	for line in c_out.splitlines():
		if "<main>:" in line : 
			gecir =1
		if gecir == 1 :
			esasy += line + '\n'	
		if gecir == 1 and "ret" in line: 
			return esasy	


# returns range of a function to analize it later.	
def getFunc(addr):
	esasy = ""
	gecir = 0
	#print("getFunc addr = ",addr.__str__())
	for line in c_out.splitlines():
		if addr in line :
			gecir =1
		if gecir == 1 :
			esasy += line + '\n'
			if "ret" in line or "nop" in line:
				#print(esasy)
				return esasy
	

# parses exact address from given string and converts it to hexadecimal 
def addrtohex(addr):
	addr = addr.__str__()
	baddr = ""
	for i in addr : 
		if i in hex16 : 
			baddr = baddr + i
	san16da = int(baddr.__str__(),16)
	return san16da 
		

# parses address of instruction from a given string
def adrestap(addr):
	gecir = 0
	iber = ""  
	for harp in addr.__str__():
		if gecir == 1:
			if ' ' in harp : 
				return iber
			iber = iber + harp
		if ',' in harp: 
			gecir = 1
	
	
# Returns function name from a string, function name between brackets "<>"	 
def funcAdytap(setir):
	gecir = 0
	iber =""
	for harp in setir.__str__():
		if ">" in harp:
			return iber
		if gecir == 1 :
			iber += harp
		if '<' in harp : 
			gecir=1
	
	
#Recursive function which parses the functions and compute PrC(Program Context)
def parse(progr):
	global PrC
	global offsetNo
	global spisok
	global gozleg_funct
	for cmd in progr.splitlines():
		opcode = cmd.split('\t')[2:3];
		#print(opcode);
		if 'jal' in opcode and 'jalr' not in opcode :
			gitmeli_addr = cmd.split('\t')[0:1]
			san16 = addrtohex(gitmeli_addr)
			PrC = hex(int(PrC.__str__(),16)+san16-offsetNo)
			#print("New PrC = ",int(PrC,16),"san16=",san16,cmd)
			func_ady=funcAdytap(cmd.split('\t')[3:4])
			#print("funk ady =",func_ady)
			spisok.append(func_ady)
			#print(spisok)

			if PrC not in h and gozleg_funct in func_ady:
				h[PrC] = spisok.__str__()
				writer.writerow([int(PrC,16)]+[spisok])
			taze_func = getFunc(adrestap(cmd.split('\t')[3:4]))
			parse(taze_func)
			spisok.pop()
			PrC = hex(int(PrC.__str__(),16)-san16+offsetNo)
			#print("Returned parse1 PrC = ",PrC)	


# Getting offset after executing readelf -l binary_prog 
def getOffset(bin_file):
	islet = Popen(["readelf",'-l',str(bin_file)],stdout=PIPE).communicate()[0]
	for cmd in islet.splitlines():
		if "LOAD" in cmd:
			iber = cmd.split(' ')[14:15]
			return addrtohex(iber)-4 
			
			 
#Main program 
if __name__ == '__main__':
	
	#Parsing segment 
	parser = argparse.ArgumentParser(description='PrC Parser')
	parser.add_argument('-f','-funct', dest= "funct", help='identify exact function to trace',required=False)
	parser.add_argument("-b","--binary",dest="filename",required=True, help='enter the name of binary file',metavar="FILE")
	args = parser.parse_args()
	binary_file = args.filename
	gozleg_funct = args.funct
	print("args = ", binary_file )
	print("Gozleg funct = ",gozleg_funct)

 	spisok = []	
	h = {}
	f = open("output.txt","w")
	writer = csv.writer(f,delimiter='\t')
	try : 
		#Execute subroutine to get objdump results 
		c_out = Popen(["toolchain/bin/riscv64-unknown-linux-gnu-objdump",'-d',binary_file],stdout=PIPE).communicate()[0] 
		offsetNo = getOffset(binary_file)
		print("Offset No = {} \n".format(hex(offsetNo+4)))
		_main = getMain(c_out)
		parse(_main)
	
	except Exception as e:
		print('Error:',e)
	print("Listing PrC values and corresponding function chain :")
	for key,value in h.items() :
		print("PrC={}, {}".format(key,value))
