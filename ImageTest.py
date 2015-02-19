import sys
import os
import Image
import ImageDraw
import ImageOps

from EPD import EPD

WHITE = 1
BLACK = 0

epd = EPD()
image=Image.new("1",epd.size, WHITE)
draw=ImageDraw.Draw(image)

def main(argv):
    """main program - display list of images"""

    

    epd.clear()
    file1=["./shineImages/U.S.topoBW.jpg"]
    print('panel = {p:s} {w:d} x {h:d}  version={v:s}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version))
    for file_name in file1:
        if not os.path.exists(file_name):
            sys.exit('error: image file{f:s} does not exist'.format(f=file_name))
            print('display: {f:s}'.format(f=file_name))
    
    
    displayGraphic(epd,file_name)
    
    

def displayGraphic(epd,file_name):
    """
    File location is fed in, and the file is opened as a new local image
    a scaling factor is calculated and it is resized in order to fit on the 
    2.7" display. The graphic is then converted to greyscale, equalized
    and converted to the appropriate moode. it is then copied onto the main
    display image and outputed
    """
    print file_name
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
    
def header():
    global epd
    imageTemp=Image.open("./shineImages/SSL_Logo_REV.jpg")
    imageTemp = ImageOps.grayscale(imageTemp)
    imageTemp = ImageOps.equalize(imageTemp)
    draw.rectangle((0,0,264,176),fill=WHITE,outline=WHITE)
    grey = imageTemp.convert("1", dither=Image.FLOYDSTEINBERG)
    image.paste(grey,(8,0))
    draw.rectangle((0,17,264,16),fill=WHITE,outline=WHITE)    
    draw.line([(0,7),(6,7)], fill=BLACK)
    draw.line([(76,7),(270,7)], fill=BLACK)

# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s} image-file'.format(p=sys.argv[0]))
    main(sys.argv[1:])


