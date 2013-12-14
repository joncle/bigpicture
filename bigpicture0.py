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
 * GoogleMaps-like  Zoom + / -  and N, S, E, W arrows
 * Unicode encoding in writexml()
 * Entry() replaced by Text() -> multiline!      

TODO :
 * Add a "Redimension / move"  Entry feature   
""" 

import Tkinter as Tk
from PIL import Image, ImageTk
from xml.dom import minidom
import tkFont

coef = 1.732    # sqrt(3)
currentx=0.
currenty=0.
currentzoom=1.
b1pressed = False
xold = 0
yold = 0

class Texte(Tk.Text):        #subclass of Entry
    def __init__(self, event=None, x=None, y=None, size=None, txt=None, *args, **kwargs):
        Tk.Text.__init__(self, master=c, bd=0, *args, **kwargs)
        if event != None:
            self.x = currentx + event.x / X() * currentzoom
            self.y = currenty + event.y / Y() * currentzoom
            self.size = 20 * currentzoom
        else:
            self.x = x
            self.y = y
            self.size = size
            self.insert(Tk.INSERT, txt) 
        
        self.focus_force()
        
        self.bind("<Alt-Button-3>", lambda event: self.destroy())
        self.bind("<FocusOut>", lambda event: self.destroyifempty())
        
        bindtags = list(self.bindtags())
        bindtags.insert(2, "custom")
        self.bindtags(tuple(bindtags))
        self.bind_class("custom", "<Key>", self.draw)
        
        self.draw()
        
    def destroyifempty(self):
        if self.get(1.0, "end-1c") == '':
            self.destroy()
        
    def draw(self, event=None):
        if event:                 # sinon self peut etre n importe quoi!
            self = event.widget
            if event.keycode in [16,17,18]:     # ctrl, maj, alt => don't redraw
                return
        #font
        displaysize = int(self.size/currentzoom)
        if displaysize < 1:
          displaysize = 1
        self.font = tkFont.Font(family="Helvetica Neue LT Com 55 Roman",size=displaysize)

        #position
        newx = int((self.x-currentx)/currentzoom*X())
        newy = int((self.y-currenty)/currentzoom*Y())
        if newx > 2*X() or newx < - 2*X() or newy > 2*Y() or newy < - 2*Y():  # out of the display window, ideally we should hide these widgets! 
           displaysize = 1        
           newx, newy=2*X(), 2*Y()         
        
        #size
        width=0
        lines=0
        for line in self.get(1.0, "end-1c").split("\n"):
            width=max(width,self.font.measure(line))
            lines += 1
       
        #place
        self.config(height=lines, font=self.font)
        self.place(x=newx, y=newy, width=width+10)
        
  
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
        text = doc.createElement('Text'); item.appendChild(text); text.appendChild(doc.createTextNode(e.get(1.0, "end-1c").rstrip("\n ").encode('utf-8')))   # enlever les espaces et newlines, encoder en utf8 (regle les problemes accents)
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
              text=s.getElementsByTagName('Text')[0].firstChild.nodeValue
              x=float(s.getElementsByTagName('x')[0].firstChild.nodeValue)
              y=float(s.getElementsByTagName('y')[0].firstChild.nodeValue)
              size=float(s.getElementsByTagName('size')[0].firstChild.nodeValue)
              Texte(x=x,y=y,size=size,txt=text)
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
    middlex = currentx + a / X() * currentzoom
    middley = currenty + b / Y() * currentzoom
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
    
def b1up(event):
    global b1pressed
    b1pressed = False
   
def motion(event):
    global currentzoom, currentx, currenty, xold, yold
    if b1pressed:
        currentx += (xold - event.x) / X() * currentzoom
        currenty += (yold - event.y) / Y() * currentzoom
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
X = lambda: float(root.winfo_width())
Y = lambda: float(root.winfo_height())

# Navigation buttons
image_file = Image.open("buttons.png")
PIL_image = ImageTk.PhotoImage(image_file.convert("RGBA"))
canvas = Tk.Canvas(root, width = image_file.size[0], height = image_file.size[1])
canvas.place(x=10,y=10)
canvas.configure(background='white', bd=0)
canvas_img = canvas.create_image(0,0,anchor=Tk.NW, image=PIL_image)
def callback(event):  
    x=event.x
    y=event.y
    if 21 < x < 21+24 and 12 < y < 12+12:  moveup()
    elif 21 < x < 21+24 and 45 < y < 45+12:  movedown()
    elif 44 < x < 44+12 and 22 < y < 22+24:  moveright()
    elif 10 < x < 10+12 and 22 < y < 22+24:  moveleft()
    elif 23 < x < 42 and 68 < y < 86: zoomplus()
    elif 23 < x < 42 and 88 < y < 107: zoomminus()
canvas.bind("<Button-1>", callback)

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
c.bind("<ButtonRelease-1>", b1up)
root.protocol("WM_DELETE_WINDOW", quit)
root.bind("<Configure>", lambda e: redraw())  #window resize

root.after(10,readxml)  # done only 10ms after mainloop() has started, prevents problem with X(), Y() = 1.0 before mainloop()

# Main loop 
root.mainloop()
