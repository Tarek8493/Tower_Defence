# tital and top labels 

from tkinter import Tk,Canvas,Label
import time, random, array
window=Tk()
window.title("Tower Defence game")

window.config(background='grey')

# canvas create
CANVAS_WIDTH = 500

CANVAS_HEIGHT = 400

TRACKX = [ 30.0,80.0,250.0,300.0,335.0,335.0,280.0,300.0,450.0,470.0,500.0]
TRACKY = [  0.0,50.0, 50.0,100.0,100.0,145.0,200.0,220.0,370.0,370.0,400.0]
#             50.0   170   50    35   45    65     20   150    


canvas=Canvas(window,width=CANVAS_WIDTH,height=CANVAS_HEIGHT,bd=0,highlightthickness=0)
canvas.grid(row=1,column=0,columnspan=2)

i=1
while i < len(TRACKX) :
    throwaway_track = canvas.create_line(TRACKX[i-1],TRACKY[i-1],TRACKX[i],TRACKY[i]) 
    i=i+1



# auto round timer/ what happenes every round


# balloon variable code
BALLOON_SIZE = 25


balloonx = list()
balloony = list()
balloon_track = list()
balloon_img = list()
i=0
while i <  len(TRACKX)-1:
    balloon_track.append(i)
    balloonx.append(TRACKX[balloon_track[i]])
    balloony.append(TRACKY[balloon_track[i]])
    balloon_img.append( canvas.create_oval(0,0,BALLOON_SIZE,BALLOON_SIZE,fill="green"))
    i=i+1

#
# ball = canvas.create_oval(-BALLOON_SIZE/2,-BALLOON_SIZE/2,BALLOON_SIZE/2,BALLOON_SIZE/2,fill="green")




# baloon function code



# tower buy code



# tower generate code

# timers
TIMER_MILISECANTS = 10
BALLOON_SPEED = 1
def move_balloons():
    global BALLOON_SPEED
    global balloon_track
    global balloonx
    global balloony
    i=0
    # i represents balloon
    
    while i < len(balloonx) :
        new_track = False
        track = balloon_track[i]
        if TRACKX[track] > TRACKX[track+1]:
            balloonx[i] = balloonx[i] - BALLOON_SPEED
            if balloonx[i]<TRACKX[track+1]:
                new_track = True

        elif TRACKX[track]<TRACKX[track+1]:
            balloonx[i] = balloonx[i] +BALLOON_SPEED
            if balloonx[i]>TRACKX[track+1]:
                new_track = True

        if TRACKY[track] > TRACKY[track+1]:
            balloony[i] = balloony[i] - BALLOON_SPEED
            if balloony[i]<TRACKY[track+1]:
                new_track = True

        elif TRACKY[track]<TRACKY[track+1]:
            balloony[i] = balloony[i] +BALLOON_SPEED
            if balloony[i]>TRACKY[track+1]:
                new_track = True

        if new_track:
            balloon_track[i]=balloon_track[i]+1
            if balloon_track[i]> len(TRACKX)-2:
                balloon_track[i] = 0
            balloony[i] = TRACKY[balloon_track[i]]
            balloonx[i] = TRACKX[balloon_track[i]]
        i = i+1
        

        
def draw():
    i=0
    while i < len(balloonx):
        canvas.moveto(balloon_img[i],balloonx[i]-BALLOON_SIZE/2,balloony[i]-BALLOON_SIZE/2)
        i=i+1

    


def master_timer():
    move_balloons()
    draw()
    
    window.update_idletasks()
    window.update()

    window.after(TIMER_MILISECANTS,master_timer)

master_timer()
window.mainloop()