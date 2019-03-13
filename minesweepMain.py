from Tkinter import *
from time import sleep
from random import randint
global SCALE
# Level         X   Y   MINES
# Beginner      9   9   10
# Intermediate  16  16  40
# Advanced      30  16  99

SCALE = 20
X =     30
Y =     16
MINES = 99
Tex_Folder = "Texture/"
########## Make Window ##########
root = Tk()
root.config(bg = "#CCCCCC")
root.minsize(X*SCALE+10,(Y+2)*SCALE)
root.maxsize(X*SCALE+10,(Y+2)*SCALE)
can = Canvas(root,height = (Y+2)*SCALE,width = X*SCALE,bg = "#CCCCCC")
can.pack(expand = YES)

########## Images for boxes ##########
global numimg
numimg = [PhotoImage(file = Tex_Folder+"/Num/0.gif"),\
          PhotoImage(file = Tex_Folder+"Num/1.gif"),\
          PhotoImage(file = Tex_Folder+"Num/2.gif"),\
          PhotoImage(file = Tex_Folder+"Num/3.gif"),\
          PhotoImage(file = Tex_Folder+"Num/4.gif"),\
          PhotoImage(file = Tex_Folder+"Num/5.gif"),\
          PhotoImage(file = Tex_Folder+"Num/6.gif"),\
          PhotoImage(file = Tex_Folder+"Num/7.gif"),\
          PhotoImage(file = Tex_Folder+"Num/8.gif"),]


global boximg,flagimg,quesimg,boxclickimg
boximg      = PhotoImage(file = Tex_Folder+"Box/box.gif")
flagimg     = PhotoImage(file = Tex_Folder+"Box/flag.gif")
quesimg     = PhotoImage(file = Tex_Folder+"Box/ques.gif")
boxclickimg = PhotoImage(file = Tex_Folder+"Box/boxclick.gif")

global mineimg,clickmineimg,nomineimg
mineimg         = PhotoImage(file = Tex_Folder+"Mine/mine.gif")
clickmineimg    = PhotoImage(file = Tex_Folder+"Mine/clickmine.gif")
nomineimg       = PhotoImage(file = Tex_Folder+"Mine/nomine.gif")

global face,faceSmile,faceClicking,faceDead,faceCool,faceNew
faceSmile       = PhotoImage(file = Tex_Folder+"Face/smile.gif")
faceClicking    = PhotoImage(file = Tex_Folder+"Face/clicking.gif")
faceDead        = PhotoImage(file = Tex_Folder+"Face/dead.gif")
faceCool        = PhotoImage(file = Tex_Folder+"Face/won.gif")
faceNew         = PhotoImage(file = Tex_Folder+"Face/newsmile.gif")
face = can.create_image(SCALE*X/2+3,13,image = faceSmile)

########## Main function ##########
def main():
    global box1,mineloc,face

    can.delete(ALL)
    face = can.create_image(SCALE*X/2+3,13,image = faceSmile)
    box1 = []
    for x1 in range(X+2):
        box2 = []
        for y1 in range (Y+2):
            box2 += [Box(x1,y1)]
        box1.append(box2)
    box1.append
    global mineloc
    mineloc = []
    for i in range(MINES):
        while True:
            tempmine = (randint(1,X),randint(1,Y))
            if not (tempmine in mineloc):
                break
        mineloc.append(tempmine)
    for i in mineloc:
        box1[i[0]][i[1]].setAsMine()
    for k in box1[1:-1]:
        for i in k[1:-1]:
            totmines = 0
            tx = i.x
            ty = i.y
            adj = [box1[tx][ty-1],box1[tx+1][ty-1],box1[tx+1][ty],box1[tx+1][ty+1],\
                   box1[tx][ty+1],box1[tx-1][ty+1],box1[tx-1][ty],box1[tx-1][ty-1]]
            for j in adj:
                if j.mine:
                    totmines += 1
            i.num = totmines
    for i in box1[0]:
        i.clicked = True
        i.num = 9
    for i in box1[-1]:
        i.clicked = True
        i.num = 9
    for i in box1[1:-1]:
        i[0].clicked = True
        i[0].num = 9
        i[-1].clicked = True
        i[-1].num = 9

    root.bind("<Button-1>",Lclick)
    root.bind("<ButtonRelease-1>",Lclickrelease)
    root.bind("<ButtonRelease-2>",Rclickrelease)

    can.pack()
    root.mainloop()
    
########## Get Box Cords ##########
def getBox(x,y=None):
    if y == None:
        y = x[1]
        x = x[0]
    
    if 4 <= x <= X*SCALE+3 and 32 <= y <= (Y+2)*SCALE-9:
        x1 = (x-4+SCALE)/SCALE
        y1 = (y-32+SCALE)/SCALE
        return (x1,y1)
    else:
        return None


########## Clicking Functions ##########

def Lclick(e):
    global face,tp,tb
    can.delete(face)
    face = can.create_image(SCALE*X/2+3,13,image = faceClicking)
    tp = getBox(e.x,e.y) # tp = Temporary Position
    if tp!=None:
        tb = box1[tp[0]][tp[1]]
        if tb.flagged or tb.ques or tb.clicked:
            tp = None
    if tp != None:
        tb.beingClicked()
    
    
def Lclickrelease(e):
    global face,tp,tb
    can.delete(face)
    face = can.create_image(SCALE*X/2+3,13,image = faceSmile)
    if tp != None:
        tb.doneClick()

def Rclickrelease(e):
    tp = getBox(e.x,e.y)
    if tp != None:
        box1[tp[0]][tp[1]].rClicked()
        
########## Game Over functions ##########

def gameoverLclick(e):
    global face,curclick
    curclick = e
    if (SCALE*X)/2-6 <= e.x <= (SCALE*X)/2+13 and\
       5 <= e.y <= 24:
        can.delete(face)
        face = can.create_image(SCALE*X/2+3,13,image = faceNew)
def gameoverLclickrelease(e):
    global face,curclick
    e = curclick
    if (SCALE*X)/2-6 <= e.x <= (SCALE*X)/2+13 and\
       5 <= e.y <= 24:
        can.delete(face)
        face = can.create_image(SCALE*X/2+3,13,image = faceSmile)
        main()
def checkGameOver():
    global face
    allmines = MINES
    allflagged = 0
    for x in box1:
        for y in x:
            if y.flagged and y.mine:
                allmines -= 1
            if y.flagged and not y.mine:
                allflagged += 1
    if allmines == 0 and allflagged == 0:
        can.delete(face)
        face = can.create_image(SCALE*X/2+3,13,image = faceCool)
        root.unbind(ALL)
        root.bind("<Button-1>",gameoverLclick)
        root.bind("<ButtonRelease-1>",gameoverLclickrelease)
def GameOver():
    global mineloc,face
    for x in box1:
        for y in x:
            y.showMine()
#    for i in mineloc:
#        if not box1[i[0]][i[1]].clicked:
#            box1[i[0]][i[1]].showMine()
    can.delete(face)
    face = can.create_image(SCALE*X/2+3,13,image = faceDead)
    root.unbind(ALL)
    root.bind("<Button-1>",gameoverLclick)
    root.bind("<ButtonRelease-1>",gameoverLclickrelease)
    
########## Class for Box ##########
class Box:
    def __init__(self,xBox,yBox,mine = False,clicked = False,num = 0):
        self.x = xBox
        self.y = yBox
        self.loc = (xBox,yBox)
        self.mine = mine
        self.num = num
        self.flagged = False
        self.ques = False
        self.clicked = False
        self.BBox = (xBox*SCALE-7,yBox*SCALE+20)
        if 0 < self.x < X+1 and 0 < self.y < Y+1:
            self.img = can.create_image(self.BBox, image = boximg)
    def setAsMine(self):
        self.mine = True
    def rClicked(self):
        ##### If flagged #####
        if self.flagged:
            self.flagged = False
            self.ques = True
            can.delete(self.img)
            self.img = can.create_image(self.BBox, image = quesimg)
        ##### If question marked #####
        elif self.ques:
            self.clicked = False
            self.ques = False
            can.delete(self.img)
            self.img = can.create_image(self.BBox, image = boximg)
        ##### If uncovered #####
        elif self.clicked:
            
            self.revealAdjecent()
        else:
            self.flagged = True
            can.delete(self.img)
            self.img = can.create_image(self.BBox, image = flagimg)
            checkGameOver()
    def setNum(self,number):
        self.num = number
        self.underimgfile = bombimg[self.num]
        self.underimage = can.create_image(self.BBox, image = self.underimgfile)
    def beingClicked(self):
        self.tempimg = can.create_image(self.BBox, image = boxclickimg)
    def doneClick(self):
        can.delete(self.tempimg)
        if not (self.flagged or self.ques):
            self.clicked = True
            if self.mine:
                self.img = can.create_image(self.BBox, image = clickmineimg)
                GameOver()
            else:
                self.search()
                
    def showMine(self):
        if self.clicked and self.mine and not self.flagged:
            pass
        elif self.mine and not self.flagged:
            self.img = can.create_image(self.BBox, image = mineimg)
        elif self.flagged and not self.mine:
            self.img = can.create_image(self.BBox, image = nomineimg)
    def revealAdjecent(self):
        adj = [box1[self.x][self.y-1],\
               box1[self.x+1][self.y-1],\
               box1[self.x+1][self.y],\
               box1[self.x+1][self.y+1],\
               box1[self.x][self.y+1],\
               box1[self.x-1][self.y+1],\
               box1[self.x-1][self.y],\
               box1[self.x-1][self.y-1]]
        adjecentFlagged = 0
        for i in adj:
            if (i.flagged):
                adjecentFlagged+=1
        if self.num==adjecentFlagged:
            for i in adj:
                if not (i.flagged or i.ques or i.clicked):
                    i.beingClicked()
                    i.doneClick()
    def search(self):
        
        self.img = can.create_image(self.BBox, image = numimg[self.num])
        if self.num == 0:
            adj = [box1[self.x][self.y-1],\
                   box1[self.x+1][self.y-1],\
                   box1[self.x+1][self.y],\
                   box1[self.x+1][self.y+1],\
                   box1[self.x][self.y+1],\
                   box1[self.x-1][self.y+1],\
                   box1[self.x-1][self.y],\
                   box1[self.x-1][self.y-1]]
            for i in adj:
                if not (i.flagged or i.ques or i.clicked):
                    i.clicked = True
                    i.search()
                
main()        

