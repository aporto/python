#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      aporto
#
# Created:     07/06/2015
# Copyright:   (c) aporto 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from random import randint

oldFile = open("logo_original_400.html", "r")
oldLogo = oldFile.readlines()
newFile = open("logo_changed.html", "w")
newFile.write('<head>\n\r <style>\n\r body { color: #00bb00; background-color:#001100;	}\n\r </style>\n\r </head>\n\r')
newFile.write('<pre style="font: 10px/5px monospace;">                                                                                                                                                                                                        \r\n')

with open ("input_code.cpp", "r") as myfile:
    inputData = myfile.read().replace('\n', '')

inputIndex = 0
color = ""
newColor = "#002200"
newFile.write('<font>');
for oldLine in oldLogo:
    newLine = "";
    for c in oldLine:
        if ord(c) < 33 :
            newColor = "#005500"
            if newColor != color:
                color = newColor;
                newLine = newLine + '</font><font color="' + color + '">'
            if ((ord(c) == 32)):# and (randint(0, 100) > 101)):
                #newLine = newLine + '.'
                nc = randint(65, 127)
                nc = ord(inputData[inputIndex])
                inputIndex = inputIndex + 1
                if inputIndex >= len(inputData):
                    inputIndex = 0
                newLine = newLine + chr(nc)
            else:
                newLine = newLine + c
        else:
            newColor = "#00bb00"
            if newColor != color:
                color = newColor;
                newLine = newLine + '</font><font color="' + color + '">'
            nc = randint(65, 127)
            nc = ord(inputData[inputIndex])
            inputIndex = inputIndex + 1
            if inputIndex >= len(inputData):
                inputIndex = 0
            newLine = newLine + chr(nc)
    newFile.write("%s" % newLine)
newFile.write('</font>');
newFile.write('</br></br>root@terminal:~$ su ./mariamole\n\r')
newFile.write('</pre>')
newFile.close()

