# tital and top labels 

from tkinter import Tk,Canvas,Label, Button
from tkinter.ttk import Progressbar
import time, random, array
window=Tk()
window.title("Tower Defence game")

window.config(background='grey')

user_health = 50

user_health_progressbar = Progressbar(window,length=100,mode="determinate",max=50)
user_health_progressbar.grid(row=0,column=2)
user_health_progressbar["value"] = user_health



# canvas create
CANVAS_WIDTH = 500

CANVAS_HEIGHT = 400

TRACK_GERTH = 10

TRACKX = [ 30.0,80.0,250.0,300.0,335.0,335.0,280.0,300.0,450.0,470.0,500.0]
TRACKY = [  0.0,50.0, 50.0,100.0,100.0,145.0,200.0,220.0,370.0,370.0,400.0]
#             50.0   170   50    35   45    65     20   150    
game_state = 0 

canvas=Canvas(window,width=CANVAS_WIDTH,height=CANVAS_HEIGHT,bd=0,highlightthickness=0)
canvas.grid(row=1,column=1,columnspan=3,rowspan=4)

i=1
while i < len(TRACKX) :
    throwaway_track = canvas.create_line(TRACKX[i-1],TRACKY[i-1],TRACKX[i],TRACKY[i],width=TRACK_GERTH) 
    i=i+1
    



# auto round timer/ what happenes every round
def game_starter():
    # global start_game
    # start_game = True
    global balloon_wave_state
    if balloon_wave_state == BWS_NOT_IN_GAME:
        balloon_wave_state=BWS_START_GAME

# balloon variable code
BALLOON_SIZE = 25
BALLOON_INITIAL_HEALTH = 6
BWS_NOT_IN_GAME =1
BWS_IN_ROUND = 2
BWS_SPAWNING = 3
BWS_BETWEEN_ROUND = 4
BWS_START_GAME = 5
BALLOON_SPAWN_FREQUENCY = 15
BETWEEN_ROUND_TICKS = 200

balloon_wave_state = BWS_NOT_IN_GAME

balloon_wave_ticks = 0

round_number = 0

start_game = False

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

    balloon_amount_tracker.config(text=len(balloonx))

def damage_balloon(b,damage):
    balloon_health[b] = balloon_health[b]-damage
    set_color_by_number(canvas,balloon_img[b],(int)(balloon_health[b]/BALLOON_INITIAL_HEALTH*255)<<16)
    if balloon_health[b]<=0:
        balloon_health[b] = 0
        delete_balloon(b)

def delete_balloon(balloon):
    global tower_target
    global tower_state
    global tower_state_ticks
    t = 0
    while t < len(tower_state):
        if tower_target[t] == balloon:
            tower_state[t] = TS_SEARCHING
            tower_state_ticks[t] = 0
            tower_target[t] = -1
        t=t+1

    canvas.delete(balloon_img[balloon])
    balloonx.pop(balloon)
    balloony.pop(balloon)
    balloon_track.pop(balloon)
    balloon_img.pop(balloon)
    balloon_health.pop(balloon)
    balloon_amount_tracker.config(text=len(balloonx))

def delete_all_balloon():
    i=len(balloonx)-1
    while i>=0:
        delete_balloon(i)
        i=i-1
# ball = canvas.create_oval(-BALLOON_SIZE/2,-BALLOON_SIZE/2,BALLOON_SIZE/2,BALLOON_SIZE/2,fill="green")

spikex = list()
spikey = list()
spike_img = list()
spike_endx = list()
spike_endy = list()
spike_steps = list()
SPIKE_SIZE = 20
SPIKE_DAMAGE = 3
def spawn_spikes(startx,starty,endx,endy,steps):
    spikex.append(startx)
    spikey.append(starty)
    spike_img.append(canvas.create_oval(0,0,SPIKE_SIZE/2,SPIKE_SIZE/2,fill="orange"))
    spike_endx.append(endx)
    spike_endy.append(endy)
    spike_steps.append(steps)
    print("a spike has spawned at "+str(startx)+", "+str(starty) +" going to "+str(endx)+", "+str(endy))

    
def spike_check():

    s=0
    while s< len(spike_img):

        if spike_steps[s] == 0:
            b = find_closest_balloon(spikex[s],spikey[s])
            if b>=0:
                deltax = balloonx[b] - spikex[s]
                deltay = balloony[b] - spikey[s]
                square_distance = deltax*deltax + deltay * deltay
                if square_distance<(BALLOON_SIZE*BALLOON_SIZE/4):
                    damage_balloon(b,SPIKE_DAMAGE)
                    delete_spike(s)
                    s=s-1
        elif spike_steps[s] > 0:
            movex = (spikex[s]-spike_endx[s])/spike_steps[s]
            movey = (spikey[s]-spike_endy[s])/spike_steps[s]
            spikex[s] = spikex[s]-movex
            spikey[s] = spikey[s]-movey
            spike_steps[s] = spike_steps[s]-1

        s=s+1

def delete_spike(s):
    canvas.delete(spike_img[s])
    spikex.pop(s)
    spikey.pop(s)
    spike_img.pop(s)
    spike_endx.pop(s)
    spike_endy.pop(s)
    spike_steps.pop(s)
def delete_all_spikes():
    i=len(spikex)-1
    while i>=0:
        delete_spike(i)
        i=i-1
# baloon function code



# tower buy code
next_tower_type = 0

def dummy_img(canvas):
    return canvas.create_rectangle(-2,-2,-1,-1)

def start_tower_place():
    global placing_tower
    global towerx 
    global towery 
    global tower_img 
    global tower_state 
    global tower_state_ticks 
    global tower_target
    global tower_type
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
    tower_type.append(next_tower_type)
    tower_shoot_animation.append(dummy_img(canvas))
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

TT_SPIKE = 1
TT_SNIPER = 2

towerx = list()
towery = list()
tower_img = list()
tower_state = list()
tower_state_ticks = list()
tower_target = list()
tower_type = list()
tower_shoot_animation = list()



placing_tower = -1



def delete_tower(tower):
    canvas.delete(tower_img[tower])
    canvas.delete(tower_shoot_animation[tower])
    towerx.pop(tower)
    towery.pop(tower)
    tower_state.pop(tower)
    tower_state_ticks.pop(tower)
    tower_img.pop(tower)
    tower_target.pop(tower)
    tower_type.pop(tower)
    tower_shoot_animation.pop(tower)
def delete_all_towers():
    i=len(towerx)-1
    while i>=0:
        delete_tower(i)
        i=i-1
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
                balloon_health[i] = 0
                delete_balloon(i)
                global user_health
                user_health = user_health -10
                user_health_progressbar["value"] = user_health
                i=i-1
            else:
                balloony[i] = TRACKY[balloon_track[i]]
                balloonx[i] = TRACKX[balloon_track[i]]
        i = i+1

    global balloon_wave_ticks
    global balloon_wave_state
    balloon_wave_ticks = balloon_wave_ticks+1
    old_state = balloon_wave_state
    new_state = old_state
    global round_number
    global start_game

    if old_state == BWS_START_GAME:
            new_state = BWS_SPAWNING
            delete_all_balloon()
            delete_all_spikes()
            delete_all_towers()
            round_number = 1
            user_health = 50
            user_health_progressbar["value"]=user_health

    if old_state == BWS_BETWEEN_ROUND:
        if balloon_wave_ticks> BETWEEN_ROUND_TICKS:
            round_number = round_number + 1
            new_state = BWS_SPAWNING
            
    elif old_state == BWS_IN_ROUND:
        if len(balloonx) == 0:
            new_state = BWS_BETWEEN_ROUND

    elif old_state == BWS_SPAWNING:
        randint = random.randint(0,999)
        random_number = random.randint(1,round_number)

        if randint < BALLOON_SPAWN_FREQUENCY:
            spawn_balloon()
            
            print(round_number)

            if len(balloonx) >= random_number:
                new_state = BWS_IN_ROUND

    if new_state != BWS_NOT_IN_GAME and user_health<=0:
        start_game = False
        new_state = BWS_NOT_IN_GAME
        print("game over")

    if old_state!= new_state :
            balloon_wave_state = new_state
            balloon_wave_ticks = 0

            
        
def find_closest_balloon(x,y):

    global balloonx
    global balloony
    
    target_balloon = -1
    tower_target_distance = CANVAS_WIDTH*CANVAS_WIDTH + CANVAS_HEIGHT*CANVAS_HEIGHT
    b = 0

    while b < len(balloonx) :
        deltax = balloonx[b] - x
        deltay = balloony[b] - y
        square_distance = deltax*deltax + deltay * deltay
        
        if square_distance < tower_target_distance:
            tower_target_distance = square_distance
            target_balloon = b
        
        b = b + 1
    return target_balloon



def tower_update():
    global towerx 
    global towery 
    global tower_img 
    global tower_state 
    global tower_state_ticks 
    global tower_target
    global tower_type
    RELOAD_TICKS = 100
    SHOOTING_TICKS = 10
    SEARCHING_TICKS = 50
    t=0
    while t < len(tower_state):
        tower_state_ticks[t] = tower_state_ticks [t]+1
        old_state = tower_state[t]
        new_state = old_state
        
        if old_state == TS_RELOAD:
            canvas.itemconfig(tower_img[t], fill = "blue")
            if tower_state_ticks[t] > RELOAD_TICKS:
                new_state=TS_SEARCHING

        elif old_state == TS_SEARCHING:
            canvas.itemconfig(tower_img[t], fill = "pink")
            if tower_state_ticks[t] > RELOAD_TICKS:
                tower_target[t] = find_closest_balloon(towerx[t],towery[t])
                if tower_target[t] >= 0:
                    new_state=TS_SHOOT 
        elif old_state == TS_SHOOT:
            canvas.itemconfig(tower_img[t], fill = "black")

            if tower_type[t] == TT_SNIPER:
                canvas.delete(tower_shoot_animation[t])
                if tower_state_ticks[t]%2==0:
                    tower_shoot_animation[t] = canvas.create_line(towerx[t],towery[t],balloonx[tower_target[t]],balloony[tower_target[t]],width=5)
                else:
                    tower_shoot_animation[t]=dummy_img(canvas)
                if tower_state_ticks[t] > SHOOTING_TICKS:
                    if tower_target[t]>=0 and tower_target[t]< len(balloon_img):
                        damage_balloon(tower_target[t],1)
                    
                    
                    new_state=TS_RELOAD
            elif tower_type[t] == TT_SPIKE:
                if tower_state_ticks[t]==1:
                    track = random.randint(0,len(TRACKX)-2)
                    percent_on_track = random.randint(0,99)
                    x= TRACKX[track]+percent_on_track*(TRACKX[track+1]-TRACKX[track])/100.0
                    y= TRACKY[track]+percent_on_track*(TRACKY[track+1]-TRACKY[track])/100.0
                    spawn_spikes(towerx[t],towery[t],x,y,SHOOTING_TICKS*10)
                elif tower_state_ticks[t] > SHOOTING_TICKS:
                    new_state = TS_RELOAD
                
        if old_state!= new_state :
            tower_state[t] = new_state
            
            tower_state_ticks[t] = 0
        t=t+1



def draw():

    s = 0
    while s < len(spikex):
        canvas.moveto(spike_img[s],spikex[s]-SPIKE_SIZE/2,spikey[s]-SPIKE_SIZE/2)
        s=s+1
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
    spike_check()
    tower_update()
    draw()
    window.update_idletasks()
    window.update()

    window.after(TIMER_MILISECANTS,master_timer)
    

canvas.bind("<Motion>",mouse_move)

canvas.bind("<Button>",mouse_click)

def tower_type_labler1():
    global next_tower_type
    next_tower_type = 1
    start_tower_place()
def tower_type_labler2():
    global next_tower_type
    next_tower_type = 2
    start_tower_place()

tower_spawn_button = Button(window,text="click to spawn spiker",command=tower_type_labler1,)
tower_spawn_button.grid(row= 1,column=4)

tower_spawn_button = Button(window,text="click to spawn sniper",command=tower_type_labler2,)
tower_spawn_button.grid(row= 3,column=4)

balloon_amount_tracker = Label(window,text=len(balloonx))
balloon_amount_tracker.grid(column=2,row=5)

game_start_button = Button(window,text="click to start game",command=game_starter)
game_start_button.grid(row=0,column=3)

def tower_type_labler1():
    global next_tower_type
    next_tower_type = 1
def tower_type_labler2():
    global next_tower_type
    next_tower_type = 2
master_timer()
window.mainloop()