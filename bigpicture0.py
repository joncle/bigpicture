# -*- coding: utf-8 -*- 

# 
# Si texte vide, détruire l'objet
# Zoom Plus / Moins : centrer sur l'objet qui a focus
# Pouvoir supprimer / redimensionner / déplacer le texte
# Sauver sur le disque
# Barre comme GoogleMaps
# Remplacer Entry par Text + auto redimensionner 

from Tkinter import *

currentx=0.
currenty=0.
currentzoom=1.
X=1000.
Y=500.

L=[]

class Texte:
    def __init__(self, event):
        self.entry = Entry(root,bd=0,font=("Purisa",int(15)))
        self.size = 15 * currentzoom
        self.x = currentx + event.x / X * currentzoom
        self.y = currenty + event.y / Y * currentzoom
        self.entry.focus_force()
        self.entry.bind("<Return>", lambda e: root.focus_force() )
        #self.entry.bind("<Control-1>", test)
        self.draw()
        
    def draw(self):
        self.entry.place(x=int((self.x-currentx)/currentzoom*X),y=int((self.y-currenty)/currentzoom*Y))
        displaysize = int(self.size/currentzoom)
        if displaysize < 1:
          displaysize = 1
        self.entry.config(font=("Purisa",displaysize))
  
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
    middlex = currentx + currentzoom / 2
    middley = currenty + currentzoom / 2
    
    a = root.focus_get().winfo_x()
    b = root.focus_get().winfo_y()
    if a > 0 and b > 0:
      middlex = currentx + a / X * currentzoom
      middley = currentx + b / Y * currentzoom
    
    currentzoom /= 2
    currentx = middlex - currentzoom /2
    currenty = middley - currentzoom /2
    redraw()

    
def leftb():
    global currentx
    currentx -= 0.1 * currentzoom
    redraw()

def rightb():
    global currentx
    currentx += 0.1 * currentzoom
    redraw()
    
def upb():
    global currenty
    currenty -= 0.1 * currentzoom
    redraw()
    
def downb():
    global currenty
    currenty += 0.1 * currentzoom
    redraw()

#def test(event):
#    event.widget.place(x= event.x, y= event.y)

def b1down(event):
    L.append(Texte(event))
    
def zoompluss(event):
    zoomplus()
    
def zoomminuss(event):
    zoomminus()

root = Tk()
root.geometry("1000x500")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
c = Canvas(root)
Button(c, text = "Zoom -",command=zoomminus).place(x=10,y=10)
Button(c, text = "Zoom +",command=zoomplus).place(x=10,y=40)
Button(c, text = "Left",command=leftb).place(x=10,y=70)
Button(c, text = "Right",command=rightb).place(x=10,y=100)
Button(c, text = "Up",command=upb).place(x=10,y=130)
Button(c, text = "Bottom",command=downb).place(x=10,y=160)

c.configure(background='white')
c.grid(sticky=N+E+S+W)
c.bind("<ButtonPress-1>", b1down)
root.bind('<Control-=>', zoompluss)   # CTRL + PLUS on my french keyboard
root.bind('<Control-minus>', zoomminuss)       # CTRL + MINUS on my french keyboard 
root.mainloop()