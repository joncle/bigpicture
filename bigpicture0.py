# -*- coding: utf-8 -*-

"""
USAGE :
 * (LEFT) CLICK on background : create a new textbox
 * CTRL + click down and motion :  easy move (like in Google Maps) 
 * CTRL + = : ZOOM +  / CTRL + - : ZOOM -
 * ALT + RIGHT click on a Textbox : DELETE it   
 * Save to XML, and ability to recover after app restart 

TODO :
 * Slow when too much zooming : redraw() should only draw visible text (Hide the rest? Or move after the windows) 
 * If Entry has no text, destroy it from the Entry list 
 * Add a "Redimension / move"  Entry feature   
 * GoogleMaps-like  Zoom + / -  and N, S, E, W arrows
 * Replace "Entry" widget by "Text" widget (multiline)  => needs to auto-dimension the widget while typing text
 * Unicode support 
""" 

import Tkinter as Tk
from xml.dom import minidom

coef = 1.732    # sqrt(3)
currentx=0.
currenty=0.
currentzoom=1.
X=1100.  # default window width
Y=600.   # default window height
b1pressed = False
xold = 0
yold = 0

class Texte(Tk.Entry):
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
        self.draw()
        
    def draw(self):
        self.place(x=int((self.x-currentx)/currentzoom*X),y=int((self.y-currenty)/currentzoom*Y))
        displaysize = int(self.size/currentzoom)
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
    try:
        for e in c.children.values():
            e.destroy()
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
    a = c.focus_get().winfo_x()
    b = c.focus_get().winfo_y()
    # here test if an entry has focus or not , doesn't work after one entry has been deleted
    # if some widget has focus, we zoom so that this widget is the "centre" of the new zoomed window 
    if a > 0 and b > 0:         
        middlex = currentx + a / X * currentzoom
        middley = currenty + b / Y * currentzoom
    else:
        middlex = currentx + currentzoom / 2
        middley = currenty + currentzoom / 2
    
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

# Navigation buttons
Tk.Button(root, text = "Zoom -",command=zoomminus).place(x=10,y=10)
Tk.Button(root, text = "Zoom +",command=zoomplus).place(x=10,y=40)
Tk.Button(root, text = "Left",command=moveleft).place(x=10,y=70)
Tk.Button(root, text = "Right",command=moveright).place(x=10,y=100)
Tk.Button(root, text = "Up",command=moveup).place(x=10,y=130)
Tk.Button(root, text = "Down",command=movedown).place(x=10,y=160)
Tk.Button(root, text = "Save file",command=writexml).place(x=10,y=190)
Tk.Button(root, text = "Read file",command=readxml).place(x=10,y=220)

def quit():
    writexml()
    root.destroy()

# Keyboard and mouse event bindings
c.bind("<ButtonPress-1>", lambda e: Texte(event=e))       # CLICK => new Entry
root.bind('<Control-=>', lambda e: zoomplus())            # CTRL + PLUS on my french keyboard
root.bind('<Control-minus>', lambda e: zoomminus())       # CTRL + MINUS on my french keyboard
c.bind("<Motion>", motion)
c.bind("<Control-ButtonPress-1>", ctrlb1down)
c.bind("<Control-ButtonRelease-1>", ctrlb1up)
root.protocol("WM_DELETE_WINDOW", quit)
readxml()

# Main loop 
root.mainloop()
