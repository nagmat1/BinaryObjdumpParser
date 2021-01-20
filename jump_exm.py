
m subprocess import *
import os

# global variable

def getMain(c_out):
        esasy = ""
        opcodes = []
        gecir = 0
        count=0;
        for line in c_out.splitlines():
                #print(line.strip())
                count +=1
                if "<main>:" in line :
                        gecir =1
                if gecir == 1 :
                        #print(line) 
                        esasy += line + '\n'
                if gecir == 1 and "ret" in line:
                        gecir =0
                opcode=[]
        print("Total number of lines: ",count)
        return esasy


def parse(progr):
        PrC = 0
        print("Goodbye")
        opcodes = []
        for cmd in progr.splitlines():
                opcode = cmd.split('\t')[2:3];
                print(opcode);
                if 'jal' in opcode :
                        print('Salam')
                        PrC = PrC + 1
                        addr  = cmd.split('\t')[0:1]
                        print(addr[0:2])
                        print(PrC)


def getOpcodes(esasy):
        for x in esasy.split('\t')[0:]:
                if x :
                        opcode.append(x)
                else :
                        opcodes.append(opcode)
                        break

if __name__ == '__main__':
        try :
                parser = Popen(["toolchain/bin/riscv64-unknown-linux-gnu-objdump",'-d','jump_exm'],stdout=PIPE).communicate()[0]
                #print(parser)
                _main = getMain(parser)
                print(_main)
                parse(_main)

        except Exception as e:
                print('Error:',e)

