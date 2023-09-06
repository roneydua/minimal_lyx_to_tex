#!/usr/bin/ python3
# -*- encoding: utf-8 -*-
'''
@File    :   updateMathSymbols.py
@Time    :   2022/11/18 16:12:32
@Author  :   Roney D. Silva
@Contact :   roneyddasilva@gmail.com
'''

import re
import shutil





def addSiglas(fileSiglas, outFile):
    for k in fileSiglas:
        f = open(k, 'r')
        print("update siglas files on ", k)
        for i in f:
            # find the entry name
            if i.find(r"newglossaryentry") > 0:
                entryname = re.split("{|}", i)[1]
            # find math symbol
            elif i.find("name=") > -1:
                # NOTE: \sc command cause conflicts with standart commands of latex
                if entryname != "sc":
                    entrysymbol = re.split(",", re.split("=|{ },", i)[1])[0][1:-1]
                    # print(entrysymbol)
                    # break
                    # print(entrysymbol, re.split("=| ,",i)[1])
                    outFile.write(r"\newcommand{" + "\\" + entryname + "}{" +
                                  entrysymbol +
                                  "}\n")

    outFile.close()

# Tex files
file = ["glossario/"+ i for i in ["comum.tex","atuadores.tex","parametros.tex","electromagnetic.tex","opticalCircuit.tex"]]
outFile = open("glossario/mathSymbols.tex",'w')


#%% update Latex main glossary

for k in file:
    f = open(k,'r')
    print("update files on ",k)
    for i in f:
        # find the entry name
        if i.find(r"newglossaryentry")>0:
            entryname = re.split("{|}",i)[1]
        # find math symbol
        elif i.find("symbol = ")>-1:
            entrysymbol = re.split("=| ,",i)[1]
            # print(entrysymbol, re.split("=| ,",i)[1])
            outFile.write(r"\newcommand{"+"\\"+entryname+"}{\glssymbol{"+entryname+"}}\n")

# Add "Siglas" to mathSymbols.tex
outFile = open("glossario/mathSymbols.tex", '+a')

fileSiglas = ["glossario/"+ i for i in ["siglas.tex"]]

addSiglas(fileSiglas=fileSiglas, outFile=outFile)
#%% Qtikz files
fileSymbols = ["glossario/"+ i for i in ["comum.tex","atuadores.tex","parametros.tex","electromagnetic.tex", "opticalCircuit.tex"]]
outFile = open("glossario/mathSymbolsQtikz.tex",'w')
# Lyx files

for k in fileSymbols:
    f = open(k,'r')
    print("update files on ",k)
    for i in f:
        # find the entry name
        if i.find(r"newglossaryentry")>0:
            entryname = re.split("{|}",i)[1]
        # find math symbol
        elif i.find("symbol = ")>-1:
            entrysymbol = re.split(",",re.split("=| ,",i)[1])[0]
            # break
            outFile.write(r"\newcommand{" +"\\" +entryname +"}{" +
                entrysymbol +
                "}\n")
outFile.close()
# Add "Siglas" to mathSymbolsQtikz
outFile = open("glossario/mathSymbolsQtikz.tex", '+a')

fileSiglas = ["glossario/"+ i for i in ["siglas.tex"]]

addSiglas(fileSiglas=fileSiglas, outFile=outFile)



#%% Lyx files
# update Lyx glossary

shutil.copyfile("glossario/mathSymbolsLyx.lyx", "glossario/mathSymbolsLyxOld.lyx")
outFileLyxOld = open("glossario/mathSymbolsLyxOld.lyx",'r')
outFileLyx = open("glossario/mathSymbolsLyx.lyx",'w')


for lin in outFileLyxOld:
    outFileLyx.write(lin)
    if lin.find(r"end_header") > 0:
        print("achei o header")
        break

outFileLyx.write("\n"+ r"\begin_body"+"\n")


for k in fileSymbols:
    f = open(k,'r')
    print("update files on ",k)
    for i in f:
        # find the entry name
        if i.find(r"newglossaryentry")>0:
            entryname = re.split("{|}",i)[1]
        # find math symbol 
        elif i.find(r"symbol = ")>-1:
            entrySymbol = re.split("=| ,",i)[1][1:-2]
            # print(entrysymbol, re.split("=| ,",i)[1])
            
            outFileLyx.write(r"\begin_layout Standard")
            outFileLyx.write("\n"+ r"\begin_inset FormulaMacro"+"\n" )
            outFileLyx.write(r"\newcommand{"+"\\"+entryname+"}{\glssymbol{"+entryname+"}}\n")
            outFileLyx.write("{"+entrySymbol+"}\n")
            outFileLyx.write(r"\end_inset"+"\n")
            outFileLyx.write("\n"+r"\end_layout"+"\n\n")
            
outFileLyx.write(r"\end_body"+"\n"+r"\end_document")
outFileLyx.close()