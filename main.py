import sys 
import Image
import ImageDraw
import ImageOps
import os
from os import listdir
from os.path import isfile,join
import ImageFont
import serial
from EPD import EPD


WHITE = 1
BLACK = 0
select=0
confirm=False
back = False
first =True
firstComms=True
firstInfo=True
firstSelect=True
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
possible_fonts = ['/usr/share/fonts/truetype/freefont/FreeMono.ttf']  

NumLines=-1
FirstCut=True
    
FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

epd = EPD()
image=Image.new('1',epd.size, WHITE)    
draw=ImageDraw.Draw(image)

def main(argv):    
    print('panel={p:s}{w:d}x{h:d} version={v:s} COG{g:d}' .format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog))
    epd.clear()
    header()
    selection()
    
def header():
    global draw
    global epd
    global image
    imageTemp=Image.open("./WistImages/SSL_Logo_REV.jpg")
    imageTemp = ImageOps.grayscale(imageTemp)
    imageTemp = ImageOps.equalize(imageTemp)
    draw.rectangle((0,0,264,176),fill=WHITE,outline=WHITE)
    grey = imageTemp.convert("1", dither=Image.FLOYDSTEINBERG)
    image.paste(grey,(8,0))
    draw.rectangle((0,17,264,16),fill=WHITE,outline=WHITE)    
    draw.line([(0,7),(6,7)], fill=BLACK)
    draw.line([(76,7),(270,7)], fill=BLACK)
def display():
    global draw
    global image
    global epd
    epd.display(image)
    epd.update()
def selection():
    global draw
    global image
    global epd
    
    FONT_SIZE = 20
    font=ImageFont.truetype(FONT_FILE, FONT_SIZE)
    draw.rectangle((0,19,264,176),fill=WHITE,outline=WHITE)
    
    global confirm
    global select
    global firstSelect
    global firstComms    
    global firstInfo
    if firstSelect==True :
        select=0
        firstSelect=False
        firstComms=True
        firstInfo=True
        confirm=False
    if select == 0:
         draw.text((0,21),'[ ] COMMS',fill=BLACK,font=font)
         draw.text((0,42),'[ ] MAP',fill=BLACK,font=font)
         draw.text((0,63),'[ ] INFO',fill=BLACK,font=font)
         display()
         buttonPress(3)
         selection()
    elif select == 1:
         draw.text((0,21),'[X] COMMS',fill=BLACK,font=font)
         draw.text((0,42),'[ ] MAP',fill=BLACK,font=font)
         draw.text((0,63),'[ ] INFO',fill=BLACK,font=font)
         if confirm==True:
             confirm=False
             comms()
         else:
             epd.display(image)
             epd.update()
             buttonPress(3)
             selection()
    elif select == 2:
         draw.text((0,21),'[ ] COMMS',fill=BLACK,font=font)
         draw.text((0,42),'[X] MAP',fill=BLACK,font=font)
         draw.text((0,63),'[ ] INFO',fill=BLACK,font=font)
         if confirm==True:
             confirm=False
             maps()
         else:
             epd.display(image)
             epd.update()
             buttonPress(3)
             selection()
    elif select == 3:
         draw.text((0,21),'[ ] COMMS',fill=BLACK,font=font)
         draw.text((0,42),'[ ] MAP',fill=BLACK,font=font)
         draw.text((0,63),'[X] INFO',fill=BLACK,font=font)
         if confirm==True:
             confirm=False
             info()
         else:
             epd.display(image)
             epd.update()
             buttonPress(3)
             selection()
             
   
    
def buttonPress(maxNum):  
    global confirm
    global back
    global first
    global select
    global ser
    sleepCounter=0
    if first==True:
        first=False
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
    x= True

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
            if select>0:            
                select = select -1
            x=False
        elif (line2 == 2): 
            print "plummit"
            if select<maxNum:            
                select = select +1
            x=False 
        elif (line2 == 8):
            confirm = True
            print "confirmed"
            x=False
        elif (line2 == 9):
            back = True
            print "back"
            x=False
        elif (line2==0):
            sleepCounter=sleepCounter+1
            if sleepCounter>600 :
                x=False                
                sleep()  

   
                
def comms():
    global select
    global back
    global confirm
    global firstComms
    global firstSelect
    global epd
    
    
    FONT_SIZE = 20
    FONT_SIZE2 = 14
    font=ImageFont.truetype(FONT_FILE, FONT_SIZE)
    draw.rectangle((0,19,264,176),fill=WHITE,outline=WHITE)
    if firstComms==True:
        print "comms"
        firstComms=False
        back=False
        firstSelect=True
        confirm=False
        select =0  
    
    font2=ImageFont.truetype(FONT_FILE, FONT_SIZE2)
    draw.text((200,19),'COMMS',fill=BLACK,font=font2)
    
       
    if back==True:
        back==False
        selection()
    if select == 0:
         draw.text((0,21),'[ ] MESSAGES',fill=BLACK,font=font)           
         epd.display(image)
         epd.update()         
         buttonPress(1)
         comms()
    elif select == 1:
         draw.text((0,21),'[X] MESSAGES',fill=BLACK,font=font)
         if confirm==True:
             confirm=False            
         else:
             epd.display(image)
             epd.update()              
             buttonPress(1)
             comms()

    
def maps():
    USA="./WistImages/U.S.topoBW.jpg"
    displayGraphic(USA)
    while back==False:
        buttonPress(1)
        selection()
    
    
    
def displayGraphic(file_name):
    """
    File location is fed in, and the file is opened as a new local image
    a scaling factor is calculated and it is resized in order to fit on the 
    2.7" display. The graphic is then converted to greyscale, equalized
    and converted to the appropriate moode. it is then copied onto the main
    display image and outputed
    """
    header()
    imageLocal = Image.open(file_name)
    size=list(imageLocal.size)
    xScale=float(263.0/float(size[0]))
    yScale=float(160.0/float(size[1]))
    if xScale*size[1]<160:
        xResize=(int(size[0]*xScale))
        yResize=(int(size[1]*xScale))
    else:
        xResize=(int(size[0]*yScale))
        yResize=(int(size[1]*yScale))
    imageLocal=imageLocal.resize((xResize,yResize))
    imageLocal = ImageOps.grayscale(imageLocal)
    imageLocal = ImageOps.equalize(imageLocal)
    bw = imageLocal.convert("1", dither=Image.FLOYDSTEINBERG)
    image.paste(bw,((264-xResize)//2,16+(160-yResize)))
    
    epd.display(image)
    epd.update()
    
def info():
    global select
    global confirm
    global firstInfo
    global firstSelect
    global epd
    global back
    
    FONT_SIZE = 20
    FONT_SIZE2 = 14
    font=ImageFont.truetype(FONT_FILE, FONT_SIZE)
    draw.rectangle((0,19,264,176),fill=WHITE,outline=WHITE)
    if firstInfo==True:
        print "info"
        firstInfo=False
        firstSelect=True
        back = False
        confirm=False
        select =0  
    
    font2=ImageFont.truetype(FONT_FILE, FONT_SIZE2)
    draw.text((200,19),'INFO',fill=BLACK,font=font2)
     
       
    if back==True:
        back==False
        selection()
    if select == 0:
         draw.text((0,FONT_SIZE),'[ ] STATUS',fill=BLACK,font=font)         
         draw.text((0,FONT_SIZE*2),'[ ] DOCUMENTS',fill=BLACK,font=font)      
         draw.text((0,FONT_SIZE*3),'[ ] SETTINGS',fill=BLACK,font=font)   
         epd.display(image)
         epd.update()         
         buttonPress(3)
         info()
    elif select == 1:
         draw.text((0,FONT_SIZE),'[X] STATUS',fill=BLACK,font=font)         
         draw.text((0,FONT_SIZE*2),'[ ] DOCUMENTS',fill=BLACK,font=font)      
         draw.text((0,FONT_SIZE*3),'[ ] SETTINGS',fill=BLACK,font=font)   
         epd.display(image)
         epd.update()              
         buttonPress(3)
         info()
    elif select == 2:
         draw.text((0,FONT_SIZE),'[ ] STATUS',fill=BLACK,font=font)         
         draw.text((0,FONT_SIZE*2),'[X] DOCUMENTS',fill=BLACK,font=font)      
         draw.text((0,FONT_SIZE*3),'[ ] SETTINGS',fill=BLACK,font=font)   
         if confirm==True:
             confirm=False            
             documents()
         else:
             epd.display(image)
             epd.update()              
             buttonPress(3)
             info()
    elif select == 3:
         draw.text((0,FONT_SIZE),'[ ] STATUS',fill=BLACK,font=font)         
         draw.text((0,FONT_SIZE*2),'[ ] DOCUMENTS',fill=BLACK,font=font)      
         draw.text((0,FONT_SIZE*3),'[X] SETTINGS',fill=BLACK,font=font)   
         if confirm==True:
             confirm=False            
         else:
             epd.display(image)
             epd.update()              
             buttonPress(3)
             info()
def documents():
    global select
    global confirm
    global back
    global firstComms
    global firstSelect
    global epd
    
    confirm=False
    back = False
    FONT_SIZE = 20
    startPosition =20
    font=ImageFont.truetype(FONT_FILE, FONT_SIZE)
    linePosition=startPosition
    draw.rectangle((0,19,264,176),fill=WHITE,outline=WHITE)
    fileLocation='/home/pi/Desktop/shine/WistDocuments'
    FileList=[f for f in listdir(fileLocation) if isfile(join(fileLocation,f))]
    select =0
    draw.rectangle((0,18,264,176),fill=WHITE,outline=WHITE)   
    
    for k in range (0, len(FileList)):
        draw.text((0,linePosition),'[ ] '+ FileList[k].rstrip('.txt'),fill=BLACK,font=font)
        linePosition+=FONT_SIZE
    epd.display(image)
    epd.update()     
    linePosition=startPosition
    while confirm!=True:
        buttonPress(len(FileList))  
        if back==True:
            back = False
            info()
        linePosition=startPosition
        draw.rectangle((0,19,25,176),fill=WHITE,outline=WHITE)
        for k in range (0, len(FileList)):
            draw.text((0,linePosition),'[ ] ',fill=BLACK,font=font)           
            if k+1==select:
                draw.text((0,linePosition),'[X] ',fill=BLACK,font=font)  
                if confirm==True:
                    confirm==False
                    print "RUN OTHER FILE"
                    startReader("./WistDocuments/"+FileList[k])
                    documents()
            linePosition+=FONT_SIZE
        epd.display(image)
        epd.update()     
        
def startReader(file_name):
    print file_name
    header()
    reFormat(file_name)
    DisplayText()
    
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
    
    
def sleep():
    global draw
    global epd
    global image
    FONT_SIZE = 30
    font=ImageFont.truetype(FONT_FILE, FONT_SIZE)
    header()
    draw.text((0,40),'LEAVE ME ALONE IM SLEEPING',fill=BLACK,font=font)
    buttonPress(1)
    
if "__main__" == __name__:
    if len(sys.argv)<1:
        sys.exit('usage: {p:s}' .format(p=sys.argv[0]))
    main(sys.argv[1:])


