from tkinter import*
from random import*
from csv import*

def valider():
    global pseudo
    pseudo=pseudoSaisie.get()
    if len(pseudo)!=0:
        pseudonyme.destroy()
        boutonCommencer.config(state=NORMAL)
        
def commencer():
    global xn,yn,nourriture,x,y,snake,objets,delai,perdu,score
    can.delete(ALL)
    can.config(bg="#000")
    can.focus_set()
    labelScore.config(text="Score : 0")
    boutonCommencer.config(state=DISABLED)
    
    snake=[]
    objets=[]
    delai=400
    perdu=False
    score=0
    deplacement="Left"
    x=250
    y=250

    objet=can.create_oval(x-10,y-10,x+10,y+10,fill="green")
    snake.append([x,y])
    objets.append(objet)

    xn=randrange(10,500,20)
    yn=randrange(10,500,20)

    nourriture=can.create_image(xn,yn,image=photo)
    deplacer()

def afficherScore():
    global fen_score
    fen_score.destroy()
    fen_score=Frame(fen)
    try:
        Label(fen_score,text="Name").grid(row=1,column=0)
        Label(fen_score,text="Score").grid(row=1,column=1)
        i=2
        with open('scores.csv',newline='') as csvfile:
            reader=DictReader(csvfile)
            for joueur in reader:
                if i<12:
                    Label(fen_score,text=joueur["pseudo"]).grid(row=i,column=0)
                    Label(fen_score,text=joueur["score"]).grid(row=i,column=1)
                i+=1
    except:
        lab=Label(fen_score,text="No score")
        lab.pack()
    fen_score.grid(row=0,column=1,rowspan=3,sticky="N")

def sauvegarder(score):
    global pseudo
    try:
        listeScores=[]
        with open('scores.csv',newline='') as csvfile:
            reader=DictReader(csvfile)
            for row in reader:
                listeScores.append(row)
        i=0
        while score<float(listeScores[i]["score"]) and i<len(listeScores)-1:
            i=i+1
    except:
        listeScores=[]
        i=0
    listeScores.insert(i,{'pseudo':pseudo,'score':str(score)})

    with open('scores.csv','w',newline='') as csvfile:
        champs=['pseudo','score']
        writer=DictWriter(csvfile,fieldnames=champs)
        writer.writeheader()
        for row in listeScores:
            writer.writerow(row)
    afficherScore()   

def effacerScores():
    csvfile=open('scores.csv','w')
    csvfile.write("")
    csvfile.close()
    afficherScore()

def contact(snake,element):
    cont=False
    for i in range(len(snake)):
        if snake[i][0]==element[0] and snake[i][1]==element[1]:
            cont=True
    return cont

def modifierDirection(event):
    global deplacement
    if event.keysym=="Up":
        deplacement="Up"
    elif event.keysym=="Right":
        deplacement="Right"
    elif event.keysym=="Down":
        deplacement="Down"
    elif event.keysym=="Left":
        deplacement="Left"

def deplacer():
    global x,y,deplacement,perdu,snake,objets,nourriture,xn,yn,delai,score

    if deplacement=="Up":
        if y>20:
            y=y-20
        else:
            perdu=True        

    elif deplacement=="Left":
        if x>20:
            x=x-20
        else:
            perdu=True

    elif deplacement=="Down":
        if y<480:
            y=y+20
        else:
            perdu=True

    elif deplacement=="Right":
        if x<480:
            x=x+20
        else:
            perdu=True

    if not perdu:
        if contact(snake,[x,y]):
            perdu=True

    if not perdu:
        if not contact(snake,[xn,yn]):
            can.delete(objets[0])
            del snake[0]
            del objets[0]

        else:
            xn=randrange(10,500,20)
            yn=randrange(10,500,20)
            while contact(snake,[xn,yn]):
                xn=randrange(10,500,20)
                yn=randrange(10,500,20)
            can.coords(nourriture,xn,yn)
            if delai>100:
                delai-=20
            score+=1
            labelScore.config(text="Score : "+str(score))

        snake.append([x,y])
        tete=can.create_oval(x-10,y-10,x+10,y+10,fill="green")

        if len(objets)!=0:
            can.itemconfigure(objets[len(objets)-1],fill="palegreen")
        objets.append(tete)
        can.after(delai,deplacer)

    else:
        can.config(bg="blue")
        can.create_text(250,250,text="GAME OVER !",fill="red",font=("Arial",30))
        sauvegarder(score)
        boutonCommencer.config(state=NORMAL,text="Retry")

perdu=False
deplacement="Up"
nourriture=""
snake=[]
objets=[]
delai=500
score=0 
pseudo=""
xn=0 
yn=0
x=0
y=0

fen=Tk()
fen.tk.call('tk', 'scaling', 2.0)
fen.title("Snake")
fen.iconbitmap('icon.ico')
fen.resizable(False, False)

labelScore=Label(text="Score : 0",font="size 12",fg="green")
labelScore.grid(row=0,column=0)

can=Canvas(height=500,width=500)
can.grid(row=1,column=0)

photo=PhotoImage(file="pomme.png")
pseudonyme=Frame(fen)
Label(pseudonyme,text="Enter a name",font="size 12").pack()

pseudoSaisie=Entry(pseudonyme,width=25,font="size 12")
pseudoSaisie.pack()

Button(pseudonyme,text="OK",font="size 12",bg='#50CC20',width=8,command=valider).pack()
pseudonyme.grid(row=1,column=0)

boutonCommencer=Button(text="Start",font="size 12",bg='#50CC20',width=10,state=DISABLED,command=commencer)
boutonCommencer.grid(row=2,column=0)

fen_score=Frame(fen)
afficherScore()

labelCopyright=Label(text="PouletEnSlip © 2022",font="size 7")
labelCopyright.grid(row=3,column=1)

boutonEffacer=Button(text="Clear scores",font="size 12",bg='#CC2050',width=12,command=effacerScores)
boutonEffacer.grid(row=2,column=1)

can.bind("<Key>",modifierDirection)

fen.mainloop()