#importing cmu library and all other needed libraries
from cmath import cos, pi, sin
from turtle import onkeypress
from cmu_graphics import *
import random
import math
#changing background color 
app.background='Black'
#instruction labels
ins=Group(
    Label("space - shoot",200,300,fill='white',size=20),
    Label("right arrow - turn clockwise",200,320,fill='white',size=20),
    Label("left arrow - turn anticlockwise",200,340,fill='white',size=20)
    )
#The score labels
counterL=Label('score',360,15,size=20,fill='white')
counter=Label(0,380,30,size=20,fill='white')
#speed multiplier of the projectiles 
app.speed=0.005
#number of steps per second
app.stepsPerSecond=15
#a variable to count the steps
app.steps=0
#a variable that uses the steps variable to count seconds
app.seconds=0
#a variable that acts as an angle in the sin and cos functions that help
#spawn the projectiles equidistant from the player and in a circle
app.angle=0
#a helper variable that helps determine how many projectiles to send 
#by checking the previous cycle of projectiles
app.eightCycle=0
#a list that stores the projectiles
app.projs=[]
#a list that stores the player's bullets
app.bullets=[]
#a variable that stored in a list at the same index as the bullet that spawns along with it
#it helps determine where the bullets spawns initially and what direction it needs to go 
app.pAngle=0
#the list that stores the app.pAngle variable each time a bullet spawns
app.pAngles=[]
#the label that holds the amount of ammo you have 
ammoL=Label('Ammo: '+str(3-len(app.bullets)),50,15,fill='white',size=20)
#the group of shapes that makes up the player
player=Group(
    Oval(200,200,40,24,fill=rgb(186,186,186)),
    Circle(200,200,10,fill='blue'),
    Rect(180,180,10,20,fill='brown'),
    Rect(210,180,10,20,fill='brown')
    )
#the function that creates projectiles
def createProjectiles(eightCycle):
    #checks if the eightcycle is true to determine if it needs to spawn 8 or 4 projectiles
    if eightCycle==True:
        #spawns 8 projectiles
        for i in range(8):
            #uses app.angle and trig to spawn the projectiles equidistant 
            #from the player and makes them spawn every 45 degrees 
            proj=Circle(200+(200*math.cos(math.radians(app.angle))),200+(200*math.sin(math.radians(app.angle))),10,fill='red')
            app.angle+=45
            app.projs.append(proj)
    elif eightCycle==False:
        #spawns 4 projectiles 
        for i in range(4):
            #uses app.angle and trig to spawn the projectiles equidistant 
            #from the player and makes them spawn every 90 degrees
            proj=Circle(200+(200*math.cos(math.radians(app.angle))),200+(200*math.sin(math.radians(app.angle))),10,fill='red')
            app.angle+=90
            app.projs.append(proj)
#function that spawns the player's bullets
def createBullet():
    #makes sure the player can only shoot bullets if there are less than 3 bullets on screen
    if len(app.bullets)<=2:
        #creates bullet and adds it to the app.bullets list
        bullet=Circle(200+20*math.sin(math.radians(player.rotateAngle)),200-20*math.cos(math.radians(player.rotateAngle)),10,fill='blue')
        app.bullets.append(bullet)
#onStep function
def onStep():
    for i in app.projs:
        #moves projectiles inward
        i.centerX-=(i.centerX-200)*app.speed
        i.centerY-=(i.centerY-200)*app.speed
        #makes the player lose if the projectile touches them
        if player.hitsShape(i):
            Label('YOU LOST!',200,125,size=40,fill='red')
            #removes all projectiles and bullets of the screen
            for i in app.projs:
                i.visible=False
            for i in app.bullets:
                i.visible=False
            app.paused=True
        for l in app.bullets:
            #makes th bullets and the projectiles dissapear if they hit each other
            if i.hitsShape(l):
                i.visible=False
                l.visible=False
                #removes them from their respective lists
                if i in app.projs:
                    app.projs.remove(i)
                app.bullets.remove(l)
                #adds to your score
                counter.value+=1
    for i in app.bullets:
        #moves bullets outward
        if i.centerX<450 and i.centerX>-50:
            i.centerX+=(i.centerX-200)*0.1
        if i.centerY<450 and i.centerY>-50:
            i.centerY+=(i.centerY-200)*0.1
        if i.centerX>400 or i.centerX<0 or i.centerY>400 or i.centerY<0:
            app.bullets.remove(i)
    #counts steps
    app.steps+=1
    #calculating seconds and assigning it to the app.seconds variable
    app.seconds=app.steps/15
    #Setting the value that will be checked to determine a eightcycle
    app.eightCycle=app.seconds%4
    #removes the instructions after 2.5 seconds
    if app.seconds>=2.5:
        ins.visible=False
    #checks the eight cycle value and runs the createProjectiles function with a different parameter
    if app.eightCycle==1:
        createProjectiles(False)
    if app.eightCycle==3:
        createProjectiles(True)
    #increases the speed of the projectiles        
    app.speed+=0.00005
    #displays and changes the ammo value depending on how many bullets are on the screen
    ammoL.value='Ammo: '+str(3-len(app.bullets))
#onKeyPress function
def onKeyPress(k):
    #rotates the player right if the right arrow is pressed
    if 'right' in k:
        player.rotateAngle+=45
    #rotates the player left if the lwft arrow is pressed
    if 'left' in k:
        player.rotateAngle-=45
    #shoots a bullet if the space bar is pressed
    if 'space' in k:
        createBullet()
cmu_graphics.run()