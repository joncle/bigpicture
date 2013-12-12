# -*- coding: utf-8 -*-

# USAGE :
# * CLICK on background : create a new textbox
# * CTRL + click down and motion :  easy move (like in Google Maps) 
# * CTRL + = : ZOOM +  / CTRL + - : ZOOM -  

# TODO :
# 1/ If Entry has no text, destroy it from the Entry list 
# 2/ Add a "Delete / Redimension / move"  Entry feature   
# 3/ Save to JSON / XML ? And be able to recover after app restart
# 4/ GoogleMaps-like  Zoom + / -  and N, S, E, W arrows
# 5/ Replace "Entry" widget by "Text" widget (multiline)  => needs to auto-dimension the widget while typing text

import Tkinter as Tk
import time 
from xml.dom import minidom

currentx=0.
currenty=0.
currentzoom=1.
X=1000.  # default window width
Y=500.   # default window height
L=[]     # list containing entries (called "Texte" object)
b1pressed = False
xold = 0
yold = 0

class Texte:
    def __init__(self, event=None, x=None, y=None, size=None, txt=None):
        self.entry = Tk.Entry(root, bd=0)
        if event != None:
            self.x = currentx + event.x / X * currentzoom
            self.y = currenty + event.y / Y * currentzoom
            self.size = 20 * currentzoom
        else:
            self.x = x
            self.y = y
            self.size = size
            self.entry.insert(0, txt) 
        
        self.entry.focus_force()
        self.entry.bind("<Return>", lambda e: root.focus_force() )
        self.entry.bind("<Alt-Button-3>", lambda e: self.entry.destroy() )
        self.draw()
        
    def draw(self):
        self.entry.place(x=int((self.x-currentx)/currentzoom*X),y=int((self.y-currenty)/currentzoom*Y))
        displaysize = int(self.size/currentzoom)
        if displaysize < 1:
          displaysize = 1
        self.entry.config(font=("Arial",displaysize))
        
    def delete(self):
        self.entry.destroy()
  
# Redraw all textboxes
def redraw():
    for e in L:
        e.draw()
        
def writexml():
    doc = minidom.Document()
    base = doc.createElement('BigPicture')
    doc.appendChild(base)
    general = doc.createElement('General'); base.appendChild(general)
    gx = doc.createElement('Currentx'); general.appendChild(gx); gx.appendChild(doc.createTextNode(str(currentx)))
    gy = doc.createElement('Currenty'); general.appendChild(gy); gy.appendChild(doc.createTextNode(str(currenty)))
    gz = doc.createElement('Currentzoom'); general.appendChild(gz); gz.appendChild(doc.createTextNode(str(currentzoom)))
    for e in L:
        item = doc.createElement('Item'); base.appendChild(item)
        text = doc.createElement('Text'); item.appendChild(text); text.appendChild(doc.createTextNode(e.entry.get()))
        x = doc.createElement('x'); item.appendChild(x); x.appendChild(doc.createTextNode(str(e.x)))
        y = doc.createElement('y'); item.appendChild(y); y.appendChild(doc.createTextNode(str(e.y)))
        size = doc.createElement('size'); item.appendChild(size); size.appendChild(doc.createTextNode(str(e.size)))
    doc.writexml( open('data.xml', 'w'), indent="", addindent="  ", newl='\n')
    doc.unlink()
    
def readxml():
    global currentx, currenty, currentzoom
    global L
    if L:
      for e in L:
        e.delete()
    L=[]
       
    xmldoc = minidom.parse('data.xml')
    
    generallist=xmldoc.getElementsByTagName('General')
    for g in generallist:
        currentx=float(g.getElementsByTagName('Currentx')[0].firstChild.nodeValue)
        currenty=float(g.getElementsByTagName('Currenty')[0].firstChild.nodeValue)
        currentzoom=float(g.getElementsByTagName('Currentzoom')[0].firstChild.nodeValue)
    
    itemlist = xmldoc.getElementsByTagName('Item') 
    for s in itemlist:
        text=s.getElementsByTagName('Text')[0].firstChild.nodeValue
        x=float(s.getElementsByTagName('x')[0].firstChild.nodeValue)
        y=float(s.getElementsByTagName('y')[0].firstChild.nodeValue)
        size=float(s.getElementsByTagName('size')[0].firstChild.nodeValue)
        L.append(Texte(x=x,y=y,size=size,txt=text))
        
def zoomminus():
    global currentzoom, currentx, currenty
    middlex = currentx + currentzoom / 2
    middley = currenty + currentzoom / 2
    currentzoom *= 1.414
    currentx = middlex - currentzoom / 2
    currenty = middley - currentzoom / 2
    redraw()
   
def zoomplus():     
    global currentzoom, currentx, currenty
    a = root.focus_get().winfo_x()
    b = root.focus_get().winfo_y()

    # if some widget has focus, we zoom so that this widget is the "centre" of the new zoomed window 
    if a > 0 and b > 0:         
        middlex = currentx + a / X * currentzoom
        middley = currenty + b / Y * currentzoom
    else:
        middlex = currentx + currentzoom / 2
        middley = currenty + currentzoom / 2
    
    currentzoom /= 1.414
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

# Create a new text entry
def b1down(event):
    L.append(Texte(event=event))
    
    
# CTRL + click + move allows moving N, S, E, W  (easier than using arrows)    
def ctrlb1down(event):
    global b1pressed, xold, yold
    b1pressed = True
    xold = event.x
    yold = event.y
    
def ctrlb1up(event):
    global b1pressed
    b1pressed = False
    
def motion(event):
    global currentzoom, currentx, currenty, xold, yold
    if b1pressed:
        currentx += (xold - event.x) / X * currentzoom
        currenty += (yold - event.y) / Y * currentzoom
        xold = event.x
        yold = event.y
        redraw() 
    
# Main
root = Tk.Tk()
root.title("BigPicture v0.1")
root.geometry("1000x500")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
c = Tk.Canvas(root)
c.configure(background='white')
c.grid(sticky='NESW')


# Navigation buttons
Tk.Button(c, text = "Zoom -",command=zoomminus).place(x=10,y=10)
Tk.Button(c, text = "Zoom +",command=zoomplus).place(x=10,y=40)
Tk.Button(c, text = "Left",command=moveleft).place(x=10,y=70)
Tk.Button(c, text = "Right",command=moveright).place(x=10,y=100)
Tk.Button(c, text = "Up",command=moveup).place(x=10,y=130)
Tk.Button(c, text = "Down",command=movedown).place(x=10,y=160)
Tk.Button(c, text = "Save file",command=writexml).place(x=10,y=190)
Tk.Button(c, text = "Read file",command=readxml).place(x=10,y=220)

# Keyboard and mouse event bindings
c.bind("<ButtonPress-1>", b1down)
root.bind('<Control-=>', lambda e: zoomplus())   # CTRL + PLUS on my french keyboard
root.bind('<Control-minus>', lambda e: zoomminus())       # CTRL + MINUS on my french keyboard
c.bind("<Motion>", motion)
c.bind("<Control-ButtonPress-1>", ctrlb1down)
c.bind("<Control-ButtonRelease-1>", ctrlb1up)

# Main loop 
root.mainloop()

