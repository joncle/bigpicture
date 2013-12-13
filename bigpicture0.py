# -*- coding: utf-8 -*-

"""
DONE :
 * (LEFT) CLICK on background : create a new textbox
 * CTRL + click down and motion :  easy move (like in Google Maps) 
 * CTRL + = : ZOOM
 * CTRL + ) or  CTRL + - : ZOOM -   
 * CTRL + à  : ZOOM on widget   
 * ALT + RIGHT click on a Textbox : DELETE it   
 * Save/read to/from XML 
 * If Entry has no text, destroy it from the Entry list   

TODO :
 * Add a "Redimension / move"  Entry feature   
 * GoogleMaps-like  Zoom + / -  and N, S, E, W arrows
 * Replace "Entry" widget by "Text" widget (multiline)  => needs to auto-dimension the widget while typing text => needs proper counting of lines
 * Replace X, Y by root.winfo_width(),  but then initialization of the widgets must be done ONCE mainloop has started 
 * Unicode support 
""" 

import Tkinter as Tk
from PIL import Image, ImageTk
from xml.dom import minidom

coef = 1.732    # sqrt(3)
currentx=0.
currenty=0.
currentzoom=1.
b1pressed = False
xold = 0
yold = 0

class Texte(Tk.Entry):        #subclass of Entry
    def __init__(self, event=None, x=None, y=None, size=None, txt=None, *args, **kwargs):
        Tk.Entry.__init__(self, master=c, bd=0, *args, **kwargs)
        if event != None:
            self.x = currentx + event.x / X * currentzoom
            self.y = currenty + event.y / Y * currentzoom
            self.size = 20 * currentzoom
        else:
            self.x = x
            self.y = y
            self.size = size
            self.insert(0, txt) 
        self.focus_force()
        self.bind("<Return>", lambda e: root.focus_force() )
        self.bind("<Alt-Button-3>", lambda event: self.destroy())
        self.bind("<FocusOut>", lambda event: self.destroyifempty())
        self.draw()
        
    def destroyifempty(self):
        if self.get() == '':
            self.destroy()
        
    def draw(self):
        newx = int((self.x-currentx)/currentzoom*X)
        newy = int((self.y-currenty)/currentzoom*Y)
        displaysize = int(self.size/currentzoom)
        if newx > 2*X or newx < - 2*X or newy > 2*Y or newy < - 2*Y:  # out of the display window, ideally we should hide these widgets! 
           displaysize = 1                 
           self.place(x=2*X,y=2*Y)
        else:
           self.place(x=newx,y=newy)
        
        if displaysize < 1:
          displaysize = 1
        self.config(font=("Helvetica Neue LT Com 55 Roman",displaysize))
  
# Redraw all textboxes
def redraw():
    for e in c.children.values():
        e.draw()
        
def writexml():
    doc = minidom.Document()
    base = doc.createElement('BigPicture')
    doc.appendChild(base)
    general = doc.createElement('General'); base.appendChild(general)
    gx = doc.createElement('Currentx'); general.appendChild(gx); gx.appendChild(doc.createTextNode(str(currentx)))
    gy = doc.createElement('Currenty'); general.appendChild(gy); gy.appendChild(doc.createTextNode(str(currenty)))
    gz = doc.createElement('Currentzoom'); general.appendChild(gz); gz.appendChild(doc.createTextNode(str(currentzoom)))
    for e in c.children.values():
        item = doc.createElement('Item'); base.appendChild(item)
        text = doc.createElement('Text'); item.appendChild(text); text.appendChild(doc.createTextNode(e.get()))
        x = doc.createElement('x'); item.appendChild(x); x.appendChild(doc.createTextNode(str(e.x)))
        y = doc.createElement('y'); item.appendChild(y); y.appendChild(doc.createTextNode(str(e.y)))
        size = doc.createElement('size'); item.appendChild(size); size.appendChild(doc.createTextNode(str(e.size)))
    doc.writexml( open('data.xml', 'w'), indent="", addindent="  ", newl='\n')
    doc.unlink()
    
def readxml():
    global currentx, currenty, currentzoom
    for e in c.children.values():
        e.destroy()
    try:
        xmldoc = minidom.parse('data.xml')
        generallist=xmldoc.getElementsByTagName('General')
        for g in generallist:
            currentx=float(g.getElementsByTagName('Currentx')[0].firstChild.nodeValue)
            currenty=float(g.getElementsByTagName('Currenty')[0].firstChild.nodeValue)
            currentzoom=float(g.getElementsByTagName('Currentzoom')[0].firstChild.nodeValue)
        
        itemlist = xmldoc.getElementsByTagName('Item') 
        for s in itemlist:
            try:
              text=s.getElementsByTagName('Text')[0].firstChild.nodeValue
              x=float(s.getElementsByTagName('x')[0].firstChild.nodeValue)
              y=float(s.getElementsByTagName('y')[0].firstChild.nodeValue)
              size=float(s.getElementsByTagName('size')[0].firstChild.nodeValue)
              Texte(x=x,y=y,size=size,txt=text)
            except:
              pass
    except:
        pass
              
def zoomminus():
    global currentzoom, currentx, currenty
    middlex = currentx + currentzoom / 2
    middley = currenty + currentzoom / 2
    currentzoom *= coef
    currentx = middlex - currentzoom / 2
    currenty = middley - currentzoom / 2
    redraw()
   
def zoomplus():     
    global currentzoom, currentx, currenty
    middlex = currentx + currentzoom / 2
    middley = currenty + currentzoom / 2
    currentzoom /= coef
    currentx = middlex - currentzoom / 2
    currenty = middley - currentzoom / 2
    redraw()
    
def zoomonwidget():
    global currentzoom, currentx, currenty
    a = c.focus_get().winfo_x()
    b = c.focus_get().winfo_y()
    middlex = currentx + a / X * currentzoom
    middley = currenty + b / Y * currentzoom
    currentzoom /= coef
    currentx = middlex - currentzoom / 2
    currenty = middley - currentzoom / 2
    redraw()

def moveleft():
    global currentx
    currentx -= 0.1 * currentzoom
    redraw()

def moveright():
    global currentx
    currentx += 0.1 * currentzoom
    redraw()
    
def moveup():
    global currenty
    currenty -= 0.1 * currentzoom
    redraw()
    
def movedown():
    global currenty
    currenty += 0.1 * currentzoom
    redraw()
  
# CTRL + click + move allows moving N, S, E, W  (easier than using arrows)    
def ctrlb1down(event):
    global b1pressed, xold, yold
    b1pressed, xold, yold = True, event.x, event.y
    
def ctrlb1up(event):
    global b1pressed
    b1pressed = False
   
def motion(event):
    global currentzoom, currentx, currenty, xold, yold
    if b1pressed:
        currentx += (xold - event.x) / X * currentzoom
        currenty += (yold - event.y) / Y * currentzoom
        xold, yold = event.x, event.y
        redraw() 
    
# Main
root = Tk.Tk()
root.title("BigPicture v0.1")
root.geometry("1100x600+100+50")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
c = Tk.Frame(root)
c.configure(background='white')
c.grid(sticky='NESW')

X=1100.  # default window width,  another solution : X = lambda: 1100. #float(root.winfo_width()) but this is not accessible before mainloop  
Y=600.   # default window height, another solution : Y = lambda: 600. #float(root.winfo_height())    => objects creation should not be done *before mainloop*

canvas = Tk.Canvas(root)
canvas.place(x=0,y=0)
canvas.configure(background='white')
width = 40
height = 40
image_file = Image.open("buttons.png")
PIL_image = ImageTk.PhotoImage(image_file.convert("RGBA"))
canvas_img = canvas.create_image(width,height,image=PIL_image)
def callback(event):  
    x=event.x
    y=event.y
    if width-9 < x < width+9 and height-24 < y < height-12:
        moveup()
    elif width-9 < x < width+9 and height+12 < y < height+24:
        movedown()
    elif width+12 < x < width+25 and height-8 < y < height+8:
        moveright()
    elif width-25 < x < width-12 and height-8 < y < height+8:
        moveleft()
canvas.bind("<Button-1>", callback)

# Navigation buttons
Tk.Button(root, text = "Zoom -",command=zoomminus).place(x=10,y=110)
Tk.Button(root, text = "Zoom +",command=zoomplus).place(x=10,y=140)

def quit():
    writexml()
    root.destroy()

# Keyboard and mouse event bindings
c.bind("<ButtonPress-1>", lambda e: Texte(event=e))       
root.bind('<Control-=>', lambda e: zoomplus())
root.bind('<Control-)>', lambda e: zoomminus())            
root.bind('<Control-minus>', lambda e: zoomminus())
root.bind('<Control-à>', lambda e: zoomonwidget())
c.bind("<Motion>", motion)
c.bind("<Control-ButtonPress-1>", ctrlb1down)
c.bind("<Control-ButtonRelease-1>", ctrlb1up)
root.protocol("WM_DELETE_WINDOW", quit)
readxml()

# Main loop 
root.mainloop()
