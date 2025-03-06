# tital and top labels 

from tkinter import Tk,Canvas,Label, Button
from tkinter.ttk import Progressbar
import time, random, array
window=Tk()
window.title("Tower Defence game")

window.config(background='dark grey')

window.resizable(False,False)

user_health = 50

user_health_progressbar = Progressbar(window,length=100,mode="determinate",max=50)
user_health_progressbar.grid(row=0,column=2)
user_health_progressbar["value"] = user_health

INITIAL_INCOME = 250
income = INITIAL_INCOME

money_amount = 0

money_amount_tracker = Label(window,text="you have $"+str(money_amount))
money_amount_tracker.grid(column=4,row=0)
income_amount_tracker = Label(window,text="you are gaining "+str(income)+" per round")
income_amount_tracker.grid(column=3,row=5)




# canvas create
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 400
canvas=Canvas(window,width=CANVAS_WIDTH,height=CANVAS_HEIGHT,bd=0,highlightthickness=0,background="sky blue")
canvas.grid(row=1,column=1,columnspan=3,rowspan=4)

# general functions
def set_color_by_number(canvas, item_id, color_number):
    """Sets the color of a canvas item using a color number."""
    hex_color = '#{:02x}{:02x}{:02x}'.format((color_number >> 16) & 0xFF, (color_number >> 8) & 0xFF, color_number & 0xFF)
    canvas.itemconfig(item_id, fill=hex_color)
    
def dummy_img(canvas):
    return canvas.create_rectangle(-2,-2,-1,-1)


# ----------------- TRACK SECTION -----------------
# track table
TRACK_WIDTH = 10
TRACKX = [ 30.0,80.0,250.0,300.0,335.0,335.0,280.0,300.0,450.0,470.0,500.0]
TRACKY = [  0.0,50.0, 50.0,100.0,100.0,145.0,200.0,220.0,370.0,370.0,400.0]
#             50.0   170   50    35   45    65     20   150    
i=1
while i < len(TRACKX) :
    throwaway_track = canvas.create_line(TRACKX[i-1],TRACKY[i-1],TRACKX[i],TRACKY[i],width=TRACK_WIDTH) 
    i=i+1

# ----------------- BALLOON SECTION -----------------

# Balloon color table
BALLOON_COLOR_UPPER = [  7, 14, 21, 28]
BALLOON_COLOR_RED =   [255,  0,  0,255]
BALLOON_COLOR_GREEN = [  0,  0,255,255]
BALLOON_COLOR_BLUE =  [  0,255,  0,255]

# Balloon constants
BALLOON_SIZE = 25
BALLOON_INITIAL_HEALTH = 2

# Balloon table
balloonx = list()
balloony = list()
balloon_track = list()
balloon_img = list()
balloon_health = list()

def spawn_balloon(health_multiplier):
    balloon_health_calc = BALLOON_INITIAL_HEALTH + health_multiplier
    if balloon_health_calc>BALLOON_COLOR_UPPER[len(BALLOON_COLOR_UPPER)-1]:
        balloon_health_calc=BALLOON_COLOR_UPPER[len(BALLOON_COLOR_UPPER)-1]

    balloon_track.append(0)
    balloonx.append(TRACKX[balloon_track[0]])
    balloony.append(TRACKY[balloon_track[0]])
    balloon_img.append( canvas.create_oval(0,0,BALLOON_SIZE,BALLOON_SIZE))
    balloon_health.append(balloon_health_calc)
    color_balloon(len(balloonx)-1)
    balloon_amount_tracker.config(text="there are "+str(len(balloonx))+" balloons")

def color_balloon(b):
    red = 0
    blue = 0
    green = 0
    last_upper = 0
    h = 0
    while h<len(BALLOON_COLOR_UPPER):
        if balloon_health[b] <= BALLOON_COLOR_UPPER[h]:
            p = (balloon_health[b]-last_upper)/float(BALLOON_COLOR_UPPER[h]-last_upper)
            p = p/2.0 + 0.5
            red = int(p*BALLOON_COLOR_RED[h])
            blue = int(p*BALLOON_COLOR_BLUE[h])
            green = int(p*BALLOON_COLOR_GREEN[h])
            print("bc "+str(h)+" "+str(p)+" "+str(red)+" "+str(blue)+" "+str(green)+" "+str(balloon_health[b]))
            
            h=len(BALLOON_COLOR_UPPER)
        else:
            last_upper=BALLOON_COLOR_UPPER[h]
            h = h+1
    color_number = (red<<16) + (green<<8) + blue
    print("bc2 "+str(color_number)+" "+str(p)+" "+str(red)+" "+str(blue)+" "+str(green)+" "+str(balloon_health[b]))
    set_color_by_number(canvas,balloon_img[b],color_number)

def damage_balloon(b,damage):
    balloon_health[b] = balloon_health[b]-damage
    
    color_balloon(b)
    if balloon_health[b]<=0:
        balloon_health[b] = 0
        delete_balloon(b,10)

def delete_balloon(balloon,balloon_kill_money_add):
    global tower_target
    global tower_state
    global tower_state_ticks
    global tower_shoot_animation
    global money_amount
    t = 0
    while t < len(tower_state):
        if tower_target[t] == balloon:
            tower_state[t] = TS_SEARCHING
            tower_state_ticks[t] = 0
            tower_target[t] = -1
            canvas.delete(tower_shoot_animation[t])
        t=t+1
    money_amount = money_amount+balloon_kill_money_add
    money_amount_tracker.config(text="you have $"+str(money_amount))
    canvas.delete(balloon_img[balloon])
    balloonx.pop(balloon)
    balloony.pop(balloon)
    balloon_track.pop(balloon)
    balloon_img.pop(balloon)
    balloon_health.pop(balloon)
    balloon_amount_tracker.config(text="there are "+str(len(balloonx))+" balloons")

def delete_all_balloon():
    i=len(balloonx)-1
    while i>=0:
        delete_balloon(i,0)
        i=i-1

def move_balloons():
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
                delete_balloon(i,0)
                global user_health
                user_health = user_health -10
                user_health_progressbar["value"] = user_health
                i=i-1
            else:
                balloony[i] = TRACKY[balloon_track[i]]
                balloonx[i] = TRACKX[balloon_track[i]]
        i = i+1

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

# ----------------- BWS SECTION -----------------
BALLOON_SPAWN_FREQUENCY = 15
BALLOON_BETWEEN_ROUND_TICKS = 200
BALLOON_SPEED = 1

# Balloon wave states
BWS_NOT_IN_GAME =1
BWS_IN_ROUND = 2
BWS_SPAWNING = 3
BWS_BETWEEN_ROUND = 4
BWS_START_GAME = 5

# Balloon variables
balloon_wave_state = BWS_NOT_IN_GAME
balloon_wave_ticks = 0
spawned_balloons = 0
round_number = 0

def game_starter():
    global balloon_wave_state
    if balloon_wave_state == BWS_NOT_IN_GAME:
        balloon_wave_state=BWS_START_GAME

# ----------------- SPIKE SECTION -----------------
SPIKE_SIZE = 20
SPIKE_INITIAL_DAMAGE = 3
SPIKE_MAX = 30
SPIKE_UPGRADE_INITIAL_COST = 500

spikex = list()
spikey = list()
spike_img = list()
spike_endx = list()
spike_endy = list()
spike_steps = list()

spike_damage = SPIKE_INITIAL_DAMAGE
spike_tower_upgrade_cost = SPIKE_UPGRADE_INITIAL_COST

def spawn_spikes(startx,starty,endx,endy,steps):
    global spike_amount
    spikex.append(startx)
    spikey.append(starty)
    spike_img.append(canvas.create_oval(0,0,SPIKE_SIZE/2,SPIKE_SIZE/2,fill="orange"))
    spike_endx.append(endx)
    spike_endy.append(endy)
    spike_steps.append(steps)
    spike_amount = len(spike_img)
    if len(spike_img) >= SPIKE_MAX:
        delete_spike(0)
    print("a spike has spawned at "+str(startx)+", "+str(starty) +" going to "+str(endx)+", "+str(endy))

def spike_check():
    global spike_amount
    global spike_damage
    s=0
    while s< len(spike_img):

        if spike_steps[s] == 0:
            b = find_closest_balloon(spikex[s],spikey[s])
            if b>=0:
                deltax = balloonx[b] - spikex[s]
                deltay = balloony[b] - spikey[s]
                square_distance = deltax*deltax + deltay * deltay
                if square_distance<(BALLOON_SIZE*BALLOON_SIZE/4):
                    damage_balloon(b,spike_damage)
                    delete_spike(s)
                    spike_amount = len(spike_img)
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

# ----------------- TOWER SECTION -----------------
TT_SPIKE = 1
TT_SNIPER = 2
TOWER_SIZE = 30
TS_PLACING = 0
TS_SEARCHING = 1
TS_SHOOT = 2
TS_RELOAD = 3
INITIAL_SNIPER_DAMAGE = 2
INITIAL_SNIPER_UPGRADE_COST = 500

RELOAD_TICKS = 100
SHOOTING_TICKS = 10
SEARCHING_TICKS = 50
TOWER_MAX = 10

next_tower_type = 0
placing_tower = -1

towerx = list()
towery = list()
tower_img = list()
tower_state = list()
tower_state_ticks = list()
tower_target = list()
tower_type = list()
tower_shoot_animation = list()

sniper_tower_upgrade_cost = INITIAL_SNIPER_UPGRADE_COST

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
    tower_amount_stat.config(text="there are: "+ str(len(towerx))+" towers")

def delete_all_towers():
    i=len(towerx)-1
    while i>=0:
        delete_tower(i)
        i=i-1

def start_tower_place():
    global placing_tower
    if placing_tower >= 0 :
        delete_tower(placing_tower)
        
        placing_tower = -1
        return
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
    tower_amount_stat.config(text="there are: "+ str(len(towerx))+" towers")

def mouse_click(event):
    global placing_tower
    if placing_tower >= 0 :
        towerx[placing_tower] = event.x
        towery[placing_tower] = event.y
        tower_state[placing_tower] = TS_SEARCHING
        tower_state_ticks[placing_tower]=0
        placing_tower = -1

def mouse_move(event):
    if placing_tower >= 0:
        towerx[placing_tower] = event.x
        towery[placing_tower] = event.y

TIMER_MILISECONDS = 10# MOVE ME

def update_balloon_state():
    global balloon_wave_ticks
    global balloon_wave_state
    balloon_wave_ticks = balloon_wave_ticks+1
    old_state = balloon_wave_state
    new_state = old_state
    global round_number
    global money_amount
    global income
    global sniper_tower_damage
    global spawned_balloons
    global spike_tower_upgrade_cost
    global sniper_tower_upgrade_cost
    global user_health

    if old_state == BWS_START_GAME:
        spike_tower_upgrade_cost = SPIKE_UPGRADE_INITIAL_COST
        sniper_tower_upgrade_cost = INITIAL_SNIPER_UPGRADE_COST
        new_state = BWS_SPAWNING
        delete_all_balloon()
        delete_all_spikes()
        delete_all_towers()
        round_number = 1
        round_number_stat.config(text="it is round: "+str(round_number))
        user_health = 50
        income = INITIAL_INCOME
        income_amount_tracker.config(text="you are gaining "+str(income)+" per round")
        user_health_progressbar["value"]=user_health
        money_amount = 800
        money_amount_tracker.config(text="you have $"+str(money_amount))
        sniper_tower_damage = INITIAL_SNIPER_DAMAGE

    if old_state == BWS_BETWEEN_ROUND:
        if balloon_wave_ticks> BALLOON_BETWEEN_ROUND_TICKS:
            round_number = round_number + 1
            round_number_stat.config(text="it is round: "+str(round_number))
            money_amount = income + money_amount
            money_amount_tracker.config(text="you have $"+str(money_amount))
            
            new_state = BWS_SPAWNING

            
    elif old_state == BWS_IN_ROUND:
        if len(balloonx) == 0:
            new_state = BWS_BETWEEN_ROUND

    elif old_state == BWS_SPAWNING:
        randint = random.randint(0,999)
        min_balloon_amount = 1
        if round_number > 5:
            min_balloon_amount = round_number-2
        random_number = random.randint(min_balloon_amount,round_number)

        if randint < BALLOON_SPAWN_FREQUENCY:
            spawn_balloon(round_number)
            
            print(round_number)
            spawned_balloons = spawned_balloons + 1
            if spawned_balloons >= random_number:
                new_state = BWS_IN_ROUND
                spawned_balloons = 0

    if new_state != BWS_NOT_IN_GAME and user_health<=0:
        new_state = BWS_NOT_IN_GAME
        delete_all_balloon()
        print("game over")

    if old_state!= new_state :
            balloon_wave_state = new_state
            balloon_wave_ticks = 0

def tower_update():
    t=0
    while t < len(tower_state):
        tower_state_ticks[t] = tower_state_ticks [t]+1
        old_state = tower_state[t]
        new_state = old_state
        
        if old_state == TS_RELOAD:
            if tower_type[t] == TT_SNIPER:
                canvas.itemconfig(tower_img[t], fill = "blue")
            elif tower_type[t] == TT_SPIKE:
                 canvas.itemconfig(tower_img[t], fill = "grey")
           
            if tower_state_ticks[t] > RELOAD_TICKS:
                new_state=TS_SEARCHING

        elif old_state == TS_SEARCHING:
            if tower_type[t] == TT_SNIPER:
                canvas.itemconfig(tower_img[t], fill = "pink")
            elif tower_type[t] == TT_SPIKE:
                 canvas.itemconfig(tower_img[t], fill ="slate blue")
            if tower_state_ticks[t] > SEARCHING_TICKS:
                tower_target[t] = find_closest_balloon(towerx[t],towery[t])
                if tower_target[t] >= 0:
                    new_state=TS_SHOOT 
        elif old_state == TS_SHOOT:
            tower_target[t] = find_closest_balloon(towerx[t],towery[t])
            if tower_type[t] == TT_SNIPER:
                canvas.itemconfig(tower_img[t], fill = "black")
                canvas.delete(tower_shoot_animation[t])

                if tower_state_ticks[t]%2==0:
                    tower_shoot_animation[t] = canvas.create_line(towerx[t],towery[t],balloonx[tower_target[t]],balloony[tower_target[t]],width=5)
                else:
                    tower_shoot_animation[t]=dummy_img(canvas)
                if tower_state_ticks[t] > SHOOTING_TICKS:
                    if tower_target[t]>=0 and tower_target[t]< len(balloon_img):
                        damage_balloon(tower_target[t],sniper_tower_damage)

                    new_state=TS_RELOAD
            elif tower_type[t] == TT_SPIKE:
                canvas.itemconfig(tower_img[t], fill = "orange")
                if tower_state_ticks[t]==1:
                    track = random.randint(0,len(TRACKX)-2)
                    percent_on_track = random.randint(0,99)
                    x= TRACKX[track]+percent_on_track*(TRACKX[track+1]-TRACKX[track])/100.0
                    y= TRACKY[track]+percent_on_track*(TRACKY[track+1]-TRACKY[track])/100.0
                    global spike_amount
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
    update_balloon_state()
    window.update_idletasks()
    window.update()

    window.after(TIMER_MILISECONDS,master_timer)
    

canvas.bind("<Motion>",mouse_move)

canvas.bind("<Button>",mouse_click)

def tower_type_labler1():
    global next_tower_type
    global money_amount
    if money_amount >= 800:
        next_tower_type = 1
        money_amount = money_amount-600
        money_amount_tracker.config(text=money_amount)
        start_tower_place()
def tower_type_labler2():
    global next_tower_type
    global money_amount
    if money_amount >= 250:
        next_tower_type = 2
        money_amount = money_amount-250
        money_amount_tracker.config(text="you have $"+str(money_amount))
        start_tower_place()

tower_spawn_button = Button(window,text="click to spawn spiker for $800",command=tower_type_labler1,background="slate blue")
tower_spawn_button.grid(row= 1,column=4)

tower_spawn_button = Button(window,text="click to spawn sniper for $250",command=tower_type_labler2,background="grey")
tower_spawn_button.grid(row= 3,column=4)

balloon_amount_tracker = Label(window,text="there are "+str(len(balloonx))+" balloons")
balloon_amount_tracker.grid(column=0,row=5)

game_start_button = Button(window,text="click to start game",command=game_starter,background="pink")
game_start_button.grid(row=0,column=3)

def income_balloon_spawner(balloon_health,income_increase):
    global income
    global balloon_wave_state
    if balloon_wave_state != BWS_NOT_IN_GAME:
        income = income_increase+income
        print("you spawned a balloon")
        spawn_balloon(balloon_health)
        income_amount_tracker.config(text="you are gaining "+str(income)+" per round")

def income_balloon_spawner1():
    income_balloon_spawner(3,10)
def income_balloon_spawner2():
    income_balloon_spawner(13,20)
def income_balloon_spawner3():
    income_balloon_spawner(13,30)
def income_balloon_spawner4():
    income_balloon_spawner(18,40)

income_increaser_button1 = Button(window,text="spawn a balloon with 5 health \n to gain 10 income " ,command=income_balloon_spawner1,background= "red")
income_increaser_button2 = Button(window,text="spawn a balloon with 10 health \n to gain 20 income " ,command=income_balloon_spawner2,background= "orange")
income_increaser_button3 = Button(window,text="spawn a balloon with 15 health \n to gain 30 income " ,command=income_balloon_spawner3,background= "green")
income_increaser_button4 = Button(window,text="spawn a balloon with 20 health \n to gain 40 income " ,command=income_balloon_spawner4,background= "silver")



income_increaser_button1.grid(row=1,column=0)
income_increaser_button2.grid(row=2,column=0)
income_increaser_button3.grid(row=3,column=0)
income_increaser_button4.grid(row=4,column=0)

def sniper_tower_upgrade():
    global sniper_tower_damage
    global sniper_tower_upgrader
    global sniper_tower_upgrade_cost
    global money_amount
    if balloon_wave_state != BWS_NOT_IN_GAME:
        if sniper_tower_upgrade_cost<= money_amount:
            sniper_tower_damage = sniper_tower_damage+1
            money_amount = money_amount-sniper_tower_upgrade_cost
            money_amount_tracker.config(text="you have $"+str(money_amount))
            sniper_tower_upgrade_cost = sniper_tower_upgrade_cost+200
            sniper_tower_upgrader.config(text="upgrade your sniper tower for $"+str(sniper_tower_upgrade_cost))
def spiker_tower_upgrade():
    global spike_damage
    global spiker_tower_upgrader
    global spike_tower_upgrade_cost
    global money_amount
    if balloon_wave_state != BWS_NOT_IN_GAME:
        if spike_tower_upgrade_cost<= money_amount:
            spike_damage = spike_damage+2
            money_amount = money_amount-spike_tower_upgrade_cost
            money_amount_tracker.config(text="you have $"+str(money_amount))
            spike_tower_upgrade_cost = spike_tower_upgrade_cost+200
            spiker_tower_upgrader.config(text="upgrade your spiker tower for $"+str(spike_tower_upgrade_cost))

sniper_tower_upgrader = Button(window,text="upgrade your sniper tower for $"+str(sniper_tower_upgrade_cost),command=sniper_tower_upgrade,background="grey")
spiker_tower_upgrader = Button(window,text="upgrade your spiker tower for $"+str(spike_tower_upgrade_cost),command=spiker_tower_upgrade,background="slate blue")


tower_amount_stat = Label(window,text="there are: "+ str(len(towerx))+" towers")
tower_amount_stat.grid(row=5,column=2)

sniper_tower_upgrader.grid(row=4,column=4)
spiker_tower_upgrader.grid(row=2,column=4)

round_number_stat = Label(window,text="it is round: "+str(round_number))
round_number_stat.grid(column=1,row=5)

def tower_type_labler1():
    global next_tower_type
    next_tower_type = 1
def tower_type_labler2():
    global next_tower_type
    next_tower_type = 2
master_timer()
window.mainloop()