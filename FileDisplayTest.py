import sys 
import Image
import os
from os import listdir
from os.path import isfile,join
import ImageFont
import ImageDraw
from EPD import EPD
import serial


def main(argv): 
    fileLocation='/home/pi/Desktop/shine/shineDocuments'
    FileList=[f for f in listdir(fileLocation) if isfile(join(fileLocation,f))]
    print FileList
    
if "__main__" == __name__:
    if len(sys.argv)<1:
        sys.exit('usage: {p:s}' .format(p=sys.argv[0]))
    main(sys.argv[1:])
