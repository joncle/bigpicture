# -*- coding: utf-8 -*-

import Tkinter as Tk
from PIL import Image, ImageTk
from xml.dom import minidom
import tkFont

#########################################
# TEXTE
#########################################
class Texte(Tk.Text):        #subclass of Text
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
            
        self.config(undo=True)
        
        self.focus_force()
        
        self.bind("<Alt-Button-3>", lambda event: self.destroy())
        self.bind("<FocusOut>", lambda event: self.destroyifempty())
        self.bind("<Control-B1-Motion>", motion)
        self.bind("<Control-ButtonPress-1>", ctrlb1down)
        self.bind("<MouseWheel>", scrollwheel)

        #self.bind("<Alt-ButtonPress-1>", lambda event: altb1down(event,self))
        #self.bind("<ButtonRelease-1>", b1up)
        #self.bind("<Motion>", lambda event: motion(event))
        
        bindtags = list(self.bindtags())
        bindtags.insert(2, "custom")
        self.bindtags(tuple(bindtags))
        self.bind_class("custom", "<Key>", self.resizebox)
        
        self.draw()
        self.resizebox(None)
        
    def destroyifempty(self):
        if self.get(1.0, "end-1c") == '':
            self.destroy()
            
    def resizebox(self, event=None):
        if event:                 # sinon self peut etre n importe quoi!
            self = event.widget
            if event.keycode in [16,17,18]:     # ctrl, maj, alt => don't redraw
                return
        width=0
        lines=0
        for line in self.get(1.0, "end-1c").split("\n"):
            width=max(width,self.font.measure(line))
            lines += 1
        self.config(height=lines)
        self.place(width=width+10)
        
    def draw(self, event=None):
        if event:                 # sinon self peut etre n importe quoi!
            self = event.widget
            
        #position   
        self.displaysize = int(self.size/currentzoom)
        newx = int((self.x-currentx)/currentzoom*X())
        newy = int((self.y-currenty)/currentzoom*Y())
        if newx > 2*X() or newx < - 2*X() or newy > 2*Y() or newy < - 2*Y():  # out of the display window, ideally we should hide these widgets! 
           self.displaysize = 1        
           newx, newy=2*X(), 2*Y()
        self.place(x=newx, y=newy)
        
        #font           
        if self.displaysize < 1:
          self.displaysize = 1
        self.font = tkFont.Font(family="Helvetica Neue LT Com 55 Roman",size=self.displaysize)
        self.config(font=self.font)
        
# Redraw all textboxes
def redraw(resize=False):
    for e in c.children.values():
        e.draw()
        if resize:
            e.resizebox()

#########################################
# XML
#########################################
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
    except:
        return
        
    generallist=xmldoc.getElementsByTagName('General')
    for g in generallist:
        currentx=float(g.getElementsByTagName('Currentx')[0].firstChild.nodeValue)
        currenty=float(g.getElementsByTagName('Currenty')[0].firstChild.nodeValue)
        currentzoom=float(g.getElementsByTagName('Currentzoom')[0].firstChild.nodeValue)
    
    itemlist = xmldoc.getElementsByTagName('Item') 
    for s in itemlist:
          try:
              x=float(s.getElementsByTagName('x')[0].firstChild.nodeValue)
              y=float(s.getElementsByTagName('y')[0].firstChild.nodeValue)
              size=float(s.getElementsByTagName('size')[0].firstChild.nodeValue)
              text=s.getElementsByTagName('Text')[0].firstChild.nodeValue
              Texte(x=x,y=y,size=size,txt=text)
              i+=1
          except:
              pass
        
def quit():
    writexml()
    root.destroy() 
        
#########################################
# ZOOM
#########################################
def zoomcoef(coef=1, xfact=1/2, yfact=1/2):
    global currentzoom, currentx, currenty
    middlex = currentx + currentzoom / 2
    middley = currenty + currentzoom / 2
    currentzoom *= coef
    currentx = middlex - currentzoom / 2
    currenty = middley - currentzoom / 2
    redraw(resize=True)
    
def zoomminus():
    zoomcoef(1.732)               # sqrt(3)
    
def zoomplus():
    zoomcoef(1/1.732)
     
def zoomonwidget():
    global currentzoom, currentx, currenty
    a = c.focus_get().winfo_x()
    b = c.focus_get().winfo_y() 
    middlex = currentx + a / X() * currentzoom
    middley = currenty + b / Y() * currentzoom
    currentzoom /= 1.732
    currentx = middlex - currentzoom / 2
    currenty = middley - currentzoom / 2
    redraw(resize=True)
    
def zoombuttonsclick(event):  
    x=event.x
    y=event.y
    if 21 < x < 21+24 and 12 < y < 12+12:  moveup()
    elif 21 < x < 21+24 and 45 < y < 45+12:  movedown()
    elif 44 < x < 44+12 and 22 < y < 22+24:  moveright()
    elif 10 < x < 10+12 and 22 < y < 22+24:  moveleft()
    elif 23 < x < 42 and 68 < y < 86: zoomplus()
    elif 23 < x < 42 and 88 < y < 107: zoomminus()
    
def scrollwheel(event):
    if event.delta > 0:
        zoomplus()
    else:
        zoomminus()

#########################################
# MOVE
#########################################
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
  
def ctrlb1down(event):
    global xold, yold
    xold, yold = event.x, event.y
   
#def altb1down(event, e):
#    global xold, yold, movingtexte
#    xold, yold = event.x, event.y
#    movingtexte = e
    
def motion(event):
    global currentzoom, currentx, currenty, xold, yold
    currentx += (xold - event.x) / X() * currentzoom
    currenty += (yold - event.y) / Y() * currentzoom
    xold, yold = event.x, event.y
    redraw()
      
#########################################
# MAIN
#########################################
root = Tk.Tk()
root.title("BigPicture")
root.geometry("1100x600+100+50")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
c = Tk.Frame(root)
c.configure(background='white')
c.grid(sticky='NESW')
X = lambda: float(root.winfo_width())
Y = lambda: float(root.winfo_height())
currentx=0.
currenty=0.
currentzoom=1.
xold = 0
yold = 0

# Navigation buttons
image_file = Image.open("buttons.png")
PIL_image = ImageTk.PhotoImage(image_file.convert("RGBA"))
canvas = Tk.Canvas(root, width = image_file.size[0], height = image_file.size[1])
canvas.place(x=10,y=10)
canvas.configure(background='white', bd=0)
canvas_img = canvas.create_image(0,0,anchor=Tk.NW, image=PIL_image)

# Keyboard and mouse event bindings
canvas.bind("<Button-1>", zoombuttonsclick)
c.bind("<ButtonPress-1>", lambda e: Texte(event=e))
c.bind("<MouseWheel>", scrollwheel)       
root.bind('<Control-=>', lambda e: zoomplus())
root.bind('<Control-)>', lambda e: zoomminus())            
root.bind('<Control-minus>', lambda e: zoomminus())
try:              # may not be handled on all keyboards (it works for french keyboards)
    root.bind('<Control-à>', lambda e: zoomonwidget())
except:
    pass
c.bind("<Control-B1-Motion>", motion)
c.bind("<Control-ButtonPress-1>", ctrlb1down)
root.protocol("WM_DELETE_WINDOW", quit)
root.after(10, readxml)  # done only 10ms after mainloop() has started, prevents problem with X(), Y() = 1.0 before mainloop()

# Main loop 
root.mainloop()