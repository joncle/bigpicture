# -*- coding: utf-8 -*- 

# TODO :
# 1/ If Entry has no text, destroy it from the Entry list 
# 2/ Add a "Delete / Redimension / move"  Entry feature   
# 3/ Save to JSON / XML ? And be able to recover after app restart
# 4/ GoogleMaps-like  Zoom + / -  and N, S, E, W arrows
# 5/ Replace "Entry" widget by "Text" widget (multiline)  => needs to auto-dimension the widget while typing text

import Tkinter as Tk 

currentx=0.
currenty=0.
currentzoom=1.
X=1000.  # default window width
Y=500.   # default window height

L=[]     # list containing entries (called "Texte" object)

class Texte:
    def __init__(self, event):
        self.entry = Tk.Entry(root,bd=0,font=("Purisa",int(15)))
        self.size = 15 * currentzoom
        self.x = currentx + event.x / X * currentzoom
        self.y = currenty + event.y / Y * currentzoom
        self.entry.focus_force()
        self.entry.bind("<Return>", lambda e: root.focus_force() )
        self.draw()
        
    def draw(self):
        self.entry.place(x=int((self.x-currentx)/currentzoom*X),y=int((self.y-currenty)/currentzoom*Y))
        displaysize = int(self.size/currentzoom)
        if displaysize < 1:
          displaysize = 1
        self.entry.config(font=("Purisa",displaysize))
  
# Redraw all textboxes
def redraw():
    for e in L:
        e.draw()
        
def zoomminus():
    global currentzoom, currentx, currenty
    middlex = currentx + currentzoom / 2
    middley = currenty + currentzoom / 2
    currentzoom *= 2
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
    
    currentzoom /= 2
    currentx = middlex - currentzoom /2
    currenty = middley - currentzoom /2
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
    L.append(Texte(event))
    
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

# Keyboard and mouse event bindings
c.bind("<ButtonPress-1>", b1down)
root.bind('<Control-=>', lambda e: zoomplus())   # CTRL + PLUS on my french keyboard
root.bind('<Control-minus>', lambda e: zoomminus())       # CTRL + MINUS on my french keyboard

# Main loop 
root.mainloop()
