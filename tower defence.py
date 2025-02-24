# tital and top labels 

from tkinter import Tk,Canvas,Label, Button
import time, random, array
window=Tk()
window.title("Tower Defence game")

window.config(background='grey')




# canvas create
CANVAS_WIDTH = 500

CANVAS_HEIGHT = 400

TRACK_GERTH = 10

TRACKX = [ 30.0,80.0,250.0,300.0,335.0,335.0,280.0,300.0,450.0,470.0,500.0]
TRACKY = [  0.0,50.0, 50.0,100.0,100.0,145.0,200.0,220.0,370.0,370.0,400.0]
#             50.0   170   50    35   45    65     20   150    



game_state = 0 

canvas=Canvas(window,width=CANVAS_WIDTH,height=CANVAS_HEIGHT,bd=0,highlightthickness=0)
canvas.grid(row=1,column=0,columnspan=2)

i=1
while i < len(TRACKX) :
    throwaway_track = canvas.create_line(TRACKX[i-1],TRACKY[i-1],TRACKX[i],TRACKY[i],width=TRACK_GERTH) 
    i=i+1
    



# auto round timer/ what happenes every round


# balloon variable code
BALLOON_SIZE = 25
BALLOON_INITIAL_HEALTH = 5
BWS_IN_ROUND = 2
BWS_SPAWNING = 3
BWS_BETWEEN_ROUND = 4
BALLOON_SPAWN_FREQUENCY = 15

balloon_wave_state = BWS_BETWEEN_ROUND

balloon_wave_ticks = 0

round_number = 0

balloonx = list()
balloony = list()
balloon_track = list()
balloon_img = list()
balloon_health = list()


def spawn_balloon():
    balloon_track.append(0)
    balloonx.append(TRACKX[balloon_track[0]])
    balloony.append(TRACKY[balloon_track[0]])
    
    balloon_img.append( canvas.create_oval(0,0,BALLOON_SIZE,BALLOON_SIZE,fill="green"))
    balloon_health.append(BALLOON_INITIAL_HEALTH)

#
# ball = canvas.create_oval(-BALLOON_SIZE/2,-BALLOON_SIZE/2,BALLOON_SIZE/2,BALLOON_SIZE/2,fill="green")




# baloon function code



# tower buy code

def start_tower_place():
    global placing_tower
    global towerx 
    global towery 
    global tower_img 
    global tower_state 
    global tower_state_ticks 
    
    if placing_tower >= 0 :
        delete_tower(placing_tower)
        
        placing_tower = -1
        return
    TOWER_MAX = 10
    if len(towerx) >= TOWER_MAX:
        delete_tower(0)

   
    towerx.append(-10000)
    towery.append(-10000)
    
    tower_img.append( canvas.create_rectangle(0,0,TOWER_SIZE,TOWER_SIZE,fill="red"))

    tower_state.append(TS_PLACING)
    tower_state_ticks.append(0)
    tower_target.append(-1)
    

    placing_tower = len(towerx)-1

def mouse_click(event):
    global towerx 
    global towery 
    global tower_img 
    global tower_state 
    global tower_state_ticks 
    global placing_tower
    global TS_SEARCHING

    if placing_tower >= 0 :
        towerx[placing_tower] = event.x
        towery[placing_tower] = event.y
        tower_state[placing_tower] = TS_SEARCHING
        tower_state_ticks[placing_tower]=0
        placing_tower = -1

    
def set_color_by_number(canvas, item_id, color_number):
    """Sets the color of a canvas item using a color number."""
    hex_color = '#{:02x}{:02x}{:02x}'.format((color_number >> 16) & 0xFF, (color_number >> 8) & 0xFF, color_number & 0xFF)
    canvas.itemconfig(item_id, fill=hex_color)
    
def mouse_move(event):
    global towerx 
    global towery 
    global tower_img 
    global tower_state 
    global tower_state_ticks 

    if placing_tower >= 0:
        towerx[placing_tower] = event.x
        towery[placing_tower] = event.y

# tower generate code
TOWER_SIZE = 30
TS_PLACING = 0
TS_SEARCHING = 1
TS_SHOOT = 2
TS_RELOAD = 3



towerx = list()
towery = list()
tower_img = list()
tower_state = list()
tower_state_ticks = list()
tower_target = list()

placing_tower = -1

def delete_balloon(balloon):
    canvas.delete(balloon_img[balloon])
    balloonx.pop(balloon)
    balloony.pop(balloon)
    balloon_track.pop(balloon)
    balloon_img.pop(balloon)
    balloon_health.pop(balloon)

def delete_tower(tower):
    canvas.delete(tower_img[tower])
    towerx.pop(tower)
    towery.pop(tower)
    tower_state.pop(tower)
    tower_state_ticks.pop(tower)
    tower_img.pop(tower)
    tower_target.pop(tower)

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
                balloon_track[i] = 0  # TODO:deleteballons instead
            balloony[i] = TRACKY[balloon_track[i]]
            balloonx[i] = TRACKX[balloon_track[i]]
        i = i+1

    global balloon_wave_ticks
    global balloon_wave_state
    balloon_wave_ticks = balloon_wave_ticks+1
    old_state = balloon_wave_state
    new_state = old_state
    global round_number
    
    if old_state == BWS_BETWEEN_ROUND:
        if balloon_wave_ticks> BWS_BETWEEN_ROUND:
            new_state = BWS_SPAWNING
            round_number = round_number + 1
    elif old_state == BWS_IN_ROUND:
        if len(balloonx) == 0:
            new_state = BWS_BETWEEN_ROUND

    elif old_state == BWS_SPAWNING:
        randint = balloon_wave_ticks%1000 #random(0,999)
        if randint < BALLOON_SPAWN_FREQUENCY:
            if len(balloonx)<round_number*1: #random
                spawn_balloon()
    if old_state!= new_state :
            balloon_wave_state = new_state
            balloon_wave_ticks = 0

def find_closest_balloon(tower):
    return tower

def tower_update():
    global towerx 
    global towery 
    global tower_img 
    global tower_state 
    global tower_state_ticks 
    global tower_target
    RELOAD_TICKS = 100
    t=0
    while t < len(tower_state):
        tower_state_ticks[t] = tower_state_ticks [t]+1
        old_state = tower_state[t]
        new_state = old_state
        
        # if state == TS_PLACING:
        
        if old_state == TS_RELOAD:
            canvas.itemconfig(tower_img[t], fill = "blue")
            if tower_state_ticks[t] > RELOAD_TICKS:
                new_state=TS_SEARCHING

        elif old_state == TS_SEARCHING:
            canvas.itemconfig(tower_img[t], fill = "pink")

            if tower_state_ticks[t] > RELOAD_TICKS:
                tower_target[t] = find_closest_balloon(t)
                new_state=TS_SHOOT

        elif old_state == TS_SHOOT:
            canvas.itemconfig(tower_img[t], fill = "black")
            if tower_state_ticks[t] > RELOAD_TICKS:
                balloon_health[tower_target[t]] = balloon_health[tower_target[t]] - 1
                set_color_by_number(canvas,balloon_img[tower_target[t]],(int)(balloon_health[tower_target[t]]/BALLOON_INITIAL_HEALTH*255)<<16)
                if balloon_health[tower_target[t]]<=0:
                    balloon_health[tower_target[t]] = 0
                    delete_balloon(tower_target[t])
                    # need to chekc other tower targets
                
                new_state=TS_RELOAD
        if old_state!= new_state :
            tower_state[t] = new_state
            tower_state_ticks[t] = 0
        t=t+1




def draw():
    i=0
    while i < len(balloonx):
        canvas.moveto(balloon_img[i],balloonx[i]-BALLOON_SIZE/2,balloony[i]-BALLOON_SIZE/2)
        i=i+1
    t=0
    while t<len(towerx):
        canvas.moveto(tower_img[t],towerx[t]-TOWER_SIZE/2,towery[t]-TOWER_SIZE/2)
        t=t+1

    


def master_timer():
    move_balloons()
    tower_update()
    draw()
    
    window.update_idletasks()
    window.update()

    window.after(TIMER_MILISECANTS,master_timer)

canvas.bind("<Motion>",mouse_move)

canvas.bind("<Button>",mouse_click)

tower_spawn_button = Button(window,text="click to spawn tower",command=start_tower_place)
tower_spawn_button.grid(row= 1,column=3)
master_timer()
window.mainloop()