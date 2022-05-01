import argparse
import re
import os
from termcolor import colored

def r(string):
    return colored(string, 'red')
def b(string):
    return colored(string, 'blue')
def y(string):
    return colored(string, 'yellow')

banner = r(f'''
 ___      ___       __       _______       _______        ____  ____  ___      ___  ___       
|"  \    /"  |     /""\     /"     "|     /"     "\      ("  _||_ " ||"  \    /"  ||"  |      
 \   \  //   |    /    \   (: ______)    (__/\    :)     |   (  ) : | \   \  //   |||  |      
 /\\  \/.    |   /' /\  \   \/    |          / ___/      (:  |  | . ) /\\  \/.    ||:  |      
|: \.        |  //  __'  \  // ___)_        // \___       \\ \__/ // |: \.        | \  |___   
|.  \    /:  | /   /  \\  \(:      "|      (:  /  "\      /\\ __ //\ |.  \    /:  |( \_|:  \  
|___|\__/|___|(___/    \___)\_______)       \_______)    (__________)|___|\__/|___| \_______) 
                                                                                              
''')+'''MAE 2 UML is a tool that take a text file containing a State Machine as parameter and creates the corresponding UML file.\n'''\
+"The delimitation of the state machie must be like :\n\n"\
+y(f'''//startMAE\n''')+"\
[S_IDLE][E_EXAMPLE1]    = {S_RUNNING,	A_EXAMPLE1_FROM_IDLE},\n\
[S_RUNNING][E_EXAMPLE1] = {S_RUNNING, A_EXAMPLE1_FROM_RUNNING},\n\
[S_RUNNING][E_EXAMPLE2] = {S_IDLE, A_EXAMPLE2}\n"\
+y(f'''//endMAE\n''')\
+b("\nVersion 0.5 by Clément Le Goffic")


def getMAE():
    array = []
    datadict = {}
    lineformat = re.compile(r"\[(?P<state>[A-Z]\w+)\]\[(?P<event>[A-Z]\w+)\]\=\{(?P<goState>[A-Z]\w+)\,(?P<action>[A-Z]\w+)\}", re.IGNORECASE)

    parser = argparse.ArgumentParser(prog='mae.py', 
                                    description= 'MAE to UML is a tool that take as argument a c file and that generate the UML diagram associate to the MAE in the file')
    parser.add_argument('filename', help='c file as input file', type=str)
    args = parser.parse_args()
    with open(args.filename) as infile, open('temp.txt', 'w') as outfile:
        copy = False
        for line in infile:
            #if line.strip() == "//startMAE":
            if line.strip() == "static Transition stateMachine[NB_STATE][NB_EVENT] = {":
                copy = True
                continue
            #elif line.strip() == "//endMAE":
            elif line.strip() == "};":
                copy = False
                continue
            elif copy:
                outfile.write(line)
    with open('temp.txt', 'r') as f:
        txt = f.read().replace(' ','')
        txt = txt.replace(',\n','\n')
        txt = txt.replace('\t','')
    with open('temp.txt', 'w') as f:
        f.write(txt)
        
    with open('temp.txt', 'r') as f:
        for l in f.readlines():
            data = re.search(lineformat, l)
            if data :
                datadict = data.groupdict()
                array.append(datadict)
    os.remove('temp.txt')
    return array

def writeUML(thelist):
    with open("mae.plantuml", 'w') as f:
        f.write("@startuml\n")
        f.write("[*] -->"+thelist[1]['state']+"\n")
        for line in thelist:
            f.write(line['state']+" --> "+line['goState']+" : "+line['event']+" / "+line['action']+"\n")
        f.write("@enduml")
if __name__ == "__main__":
    print(banner)
    mae = getMAE()
    writeUML(mae)
    print(r("\nUML generated !\n"))
