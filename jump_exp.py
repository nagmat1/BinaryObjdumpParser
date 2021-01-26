from subprocess import * 
import os 
import csv 


hex16 = {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}
#Global variables 
PrC = 0
offsetNo = 0
spisok = []


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
	
def getFunc(addr):
	esasy = ""
	gecir = 0
	print("getFunc addr = ",addr.__str__())
	for line in c_out.splitlines():
		if addr in line :
			gecir =1
		if gecir == 1 :
			esasy += line + '\n'
			if "ret" in line or "nop" in line:
				print(esasy)
				return esasy
	

def addrtohex(addr):
	addr = addr.__str__()
	baddr = ""
	for i in addr : 
		if i in hex16 : 
			baddr = baddr + i
	san16da = int(baddr.__str__(),16)
	return san16da 
		

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
	
	
	 
def funcAdytap(setir):
	print(setir)
	gecir = 0
	iber =""
	for harp in setir.__str__():
		if ">" in harp:
			return iber
		if gecir == 1 :
			iber += harp
		if '<' in harp : 
			gecir=1
		

def parse(progr):
	global PrC
	global offsetNo
	global spisok
	for cmd in progr.splitlines():
		opcode = cmd.split('\t')[2:3];
		#print(opcode);
		if 'jal' in opcode and 'jalr' not in opcode :
			gitmeli_addr = cmd.split('\t')[0:1]
			san16 = addrtohex(gitmeli_addr)
			PrC = hex(int(PrC.__str__(),16)+san16-offsetNo)
			print("New PrC = ",int(PrC,16),"san16=",san16,cmd)
			func_ady=funcAdytap(cmd.split('\t')[3:4])
			print("funk ady =",func_ady)
			spisok.append(func_ady)
			print(spisok)

			if PrC not in h :
				h[PrC] = spisok.__str__()
				writer.writerow([int(PrC,16)]+[spisok])
			taze_func = getFunc(adrestap(cmd.split('\t')[3:4]))
			parse(taze_func)
			spisok.pop()
			PrC = hex(int(PrC.__str__(),16)-san16+offsetNo)
			print("Returned parse1 PrC = ",PrC)	

def getOffset(c_out):
	for cmd in c_out.splitlines():
		if "PROCEDURE_LINKAGE_TABLE" in cmd:
			return addrtohex(cmd.split(' ')[0:1])-114 
			
			 

if __name__ == '__main__':
 	spisok = []	
	h = {}
	f = open("output.txt","w")
	writer = csv.writer(f,delimiter='\t')
	try : 
		c_out = Popen(["toolchain/bin/riscv64-unknown-linux-gnu-objdump",'-d','jump_exm'],stdout=PIPE).communicate()[0] 
		#print(c_out)
		offsetNo = getOffset(c_out)
		print("Offset No = ", offsetNo)
		_main = getMain(c_out)
		parse(_main)
	
	except Exception as e:
		print('Error:',e)

	print("hash table = ",h)
