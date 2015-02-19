import sys 
import Image
import os
import ImageFont
import ImageDraw
from EPD import EPD
import serial

WHITE = 1
BLACK = 0

""" READER GLOBAL VARIABLES"""

NumLines=-1
FirstCut=True


select=0
confirm=False
first =True
firstComms=True
firstSelect=True
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
possible_fonts = ['/usr/share/fonts/truetype/freefont/FreeMono.ttf']  
FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break
epd = EPD()
image=Image.new('1',epd.size, WHITE)    
draw=ImageDraw.Draw(image)

def main(file1):    
    
    print('panel={p:s}{w:d}x{h:d} version={v:s} COG{g:d}' .format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog))
    epd.clear()
    
    for file_name in file1:
        if not os.path.exists(file_name):
            sys.exit('error: image file{f:s} does not exist'.format(f=file_name))
            print('display: {f:s}'.format(f=file_name))
    header()
    reFormat(file_name)
    DisplayText()
    
def header():
    global draw
    global epd
    global image
    draw.rectangle((0,0,264,176),fill=WHITE,outline=WHITE)
    FONT_SIZE =16
    font=ImageFont.truetype(FONT_FILE, FONT_SIZE)

    draw.rectangle((10,0,264,16),fill=WHITE,outline=WHITE)    
    
    draw.text((10,0),'SSL', fill=BLACK,font=font)
    draw.line([(0,8),(8,8)], fill=BLACK)
    draw.line([(40,8),(270,8)], fill=BLACK)


def DisplayText():
    startingPosition=18
    FONT_SIZE = 14
    lineAllotment = 12
    
    bottom=0
    top=0
    startWrite=0
    stopWrite=lineAllotment
    linePosition=startingPosition
    font=ImageFont.truetype(FONT_FILE, FONT_SIZE)
    tempDocument=open("temp.txt",'r')
    lines=tempDocument.readlines()
    for k in range (0,lineAllotment):
        lines[k]=lines[k].rstrip('\n')
        draw.text((0,linePosition),lines[k],fill=BLACK,font=font)
        linePosition=linePosition+FONT_SIZE
        bottom+=1
    linePosition=startingPosition
    epd.display(image)
    epd.update()  
    pressed=ScrollButtonPress()
    while pressed!=3:
        if pressed==1:
            print "scroll down"
            if stopWrite+lineAllotment<=len(lines):
                stopWrite+=lineAllotment
                startWrite+=lineAllotment
            else:
                stopWrite=len(lines)
            if bottom <=len(lines):
                draw.rectangle((0,startingPosition,264,176),fill=WHITE,outline=WHITE)
                for k in range (startWrite,stopWrite):
                    lines[k]=lines[k].rstrip('\n')
                    draw.text((0,linePosition),lines[k],fill=BLACK,font=font)
                    linePosition=linePosition+FONT_SIZE
                    bottom+=1
                    top+=1
                epd.display(image)
                epd.update() 
                    
        elif pressed==2:
            print "scroll up"
            if startWrite-lineAllotment>0:
                startWrite-=lineAllotment
                stopWrite-=lineAllotment
            else:
                startWrite=0
            
            if top>0:
                draw.rectangle((0,startingPosition,264,176),fill=WHITE,outline=WHITE)
                for k in range (startWrite,stopWrite):
                    lines[k]=lines[k].rstrip('\n')
                    draw.text((0,linePosition),lines[k],fill=BLACK,font=font)
                    linePosition=linePosition+FONT_SIZE
                    bottom-=1
                    top-=1
                epd.display(image)
                epd.update() 
        pressed=ScrollButtonPress()
        print pressed
        linePosition=startingPosition
    
                   
    os.remove("temp.txt")
def cut(cAllotment,OldLine):
    global NumLines
    global FirstCut
    spaceCounter=0
    NumLines=NumLines+1
    i=-1
    lineLength=0
    line2=""
    templine=""
    if FirstCut==True:
        FirstCut=False
        NewLine=[[]]*((len(OldLine) // cAllotment)+2)

    else:
        
        NewLine=OldLine
        OldLine=NewLine[NumLines]
        NewLine[NumLines]=""
        
    line=OldLine.split(' ')
    
    while i<len(line):
        i=i+1
        if line[i]!="":
               if lineLength + len(line[i])+spaceCounter <cAllotment:
                   lineLength=lineLength+len(line[i])
                   spaceCounter+=1
                   templine=templine+line[i]+" "
                   NewLine[NumLines]=templine
               else:                       
                   while i<len(line):
                       line2=line2+line[i]+" "
                       i=i+1
                   NewLine[NumLines+1]=line2
                   if i>=len(line)-1:
                       tempString=cut(cAllotment,NewLine)
                       NewLine[NumLines]=tempString[NumLines]
        else:
            break
    return NewLine
    
def reFormat(file_name):
    global NumLines
    global FirstCut
    j=0
    line3=""
    xx=True
    document=open(file_name,'r')
    tempDocument=open("temp.txt",'w')
    while xx==True:
       j=0
       line=document.readline()
       if line=="":
           xx=False
       line=line.rstrip('\n')
       if len(line) < 30:
            tempDocument.write(line +'\n')
       else:
           line3=cut(30,line)
           FirstCut=True
           NumLines=-1
           while j<len(line3):
               if not line3[j]:
                   break
               tempDocument.write(line3[j] +'\n')
               j=j+1
    tempDocument.close()
    
def ScrollButtonPress():  
    global first
    global select
    global ser
    if first==True:
        first=False
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
    x= True
    pressed=0

    while x==True:
        line2=ser.readline().rstrip()
        print line2    
        
        try:
            line2=int(float(line2))
        except ValueError:
            print "NOBODY LIKES YOU"
            print type(line2)
                        
        if (line2 == 1):     
            print "going up"
            pressed=2
            x=False
        elif (line2 == 2): 
            print "plummit"      
            pressed=1
            x=False 
        elif (line2 == 9):
            pressed=3
            print "EXIT"
            x=False
    return pressed       
             
    
if "__main__" == __name__:
    if len(sys.argv)<1:
        sys.exit('usage: {p:s}' .format(p=sys.argv[0]))
    main(sys.argv[1:])

