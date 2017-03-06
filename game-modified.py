# Authors: Emily Quinn Finney and Madeleine Bulkow

import math
from visual import *

class Asteroid:
    """ Makes the beautiful objects in space you see hurtling about
    """
    def __init__(self, pos, radius):
        """ The constructor for objects of type Asteroid.
        """
        self.pos = vector(pos)
        self.radius = radius
        self.mass = 2*radius**3
        self.body = sphere(pos=self.pos, radius=radius, color=(.5,.5,.5))        

    def __repr__(self):
        """ Represents the beautiful objects in space you see hurtling about
        """
        s = "  position:" + str(self.pos) + "\n"
        s += "  heading: " + str(self.heading) + "\n"
        return s

    def update(self):
        """ Moves the pictoral representation of the asteroid"""
        self.body.pos = self.pos
        self.body.radius = self.radius

class ICT:
    """ Represents the ice cream truck driven around.
    """
    def __init__(self, pos, color=(1,1,1), heading=vector(1,0,0)):
        """ constructor for our ICT class """
        # list of vPython 3D shapes that make up this robot
        self.parts = []
        # Position of the origin of robot; we make sure it's a vector
        # For consistency, we use the same name as VPython's objects
        self.pos = vector(pos)
        # Direction in which robot is moving, normalized to unit length
        self.heading = norm(heading)
        self.color = color

        right_headlight1 = sphere(pos=self.pos+vector(8,-2,1.5),
                                  radius = .4,color=(1,1,0))
                 
        left_headlight1 = sphere(pos=self.pos+vector(8,-2,-1.5),
                                  radius = .4,color=(1,1,0))
                 
        self.parts += [right_headlight1]
        self.parts += [left_headlight1]

        right_taillight1 = sphere(pos=self.pos+vector(-5,-2,-1.5),
                                  radius = .4,color=(1,0,0))
                 
        left_taillight1 = sphere(pos=self.pos+vector(-5,-2,1.5),
                                  radius = .4,color=(1,0,0))
                 
        self.parts += [right_taillight1]
        self.parts += [left_taillight1]
        
        # the main body of our robot is a sphere
        self.body = box(pos=self.pos, length=10, height=6, width=6,
                           color=color)
        self.parts += [self.body] # add it to our "parts" list
        
        # front.
        HjemIS= box(pos=self.pos+vector(6.5,-1.5,0),
                    length=3, height=3, width=6, color=color) 

        self.parts += [HjemIS]

        forcefield = sphere(pos=self.pos, radius = 10, color = (0,0,1),
                            opacity = .15)

        self.radius = 10

    
        self.parts += [forcefield]

        FLwheel = cylinder(pos=self.pos+vector(5,-3,2.5), axis=(0,0,1),
                           radius=1.5, color=(0.5,0.5,0.5))
        FRwheel = cylinder(pos=self.pos+vector(5,-3,-2.5), axis=(0,0,-1),
                           radius=1.5, color=(0.5,0.5,0.5))
        BLwheel = cylinder(pos=self.pos+vector(-3,-3,2.5), axis=(0,0,1),
                           radius=1.5, color=(0.5,0.5,0.5))
        BRwheel = cylinder(pos=self.pos+vector(-3,-3,-2.5), axis=(0,0,-1),
                           radius=1.5, color=(0.5,0.5,0.5))

        self.parts += [FLwheel, FRwheel, BLwheel, BRwheel]

        windowRight = box(pos=self.pos+(5,1.5,1.5), length=0.1,
                          height=2.5, width=2.5, color=(0.1,0.1,0.1))
        
        windowLeft = box(pos=self.pos+(5,1.5,-1.5), length=0.1,
                          height=2.5, width=2.5, color=(0.1,0.1,0.1))

        self.parts += [windowRight,windowLeft]

        for part in self.parts:
            part.heading = self.heading

        self.Lights = []
        
        rightheadlight=local_light(pos=self.parts[0].pos,color=(0,1,1))
        leftheadlight=local_light(pos=self.parts[1].pos,color=(0,1,1))
        righttaillight=local_light(pos=self.parts[2].pos,color=(1,0,0))
        lefttaillight=local_light(pos=self.parts[3].pos,color=(1,0,0))

        self.Lights += [rightheadlight, leftheadlight, righttaillight,
                        lefttaillight]

        for light in self.Lights:
            light.heading = self.heading

        self.mass = 18000

           
    def forward(self, dt):
        ''' Change robot's location by moving in 
            the heading direction by a given amount '''
        motion_vector = self.velocity*dt
        self.pos += motion_vector
        for part in self.parts:
            part.pos += motion_vector
        for light in self.Lights:
            light.pos += motion_vector
    
    def turnXZ(self, angle):
        ''' Turn the robot by the given angle, in degrees '''
        # convert the angle to radians first
        theta = math.radians(angle)
        # rotate the heading vector around the vertical y-axis
        self.heading = rotate(self.heading, angle=theta, axis=(0,1,0))
        # rotate all of the parts around the current position
        for part in self.parts:
            part.rotate(angle=theta, axis=(0,1,0), origin=self.pos)
            part.heading = self.heading
        for i in range(0,4):
            self.Lights[i].pos = self.parts[i].pos
            self.Lights[i].heading = self.heading

    def turnUP(self, angle):
        ''' Turn the robot by the given angle, in degrees '''
        # convert the angle to radians first
        theta = math.radians(angle)
        # rotate the heading vector around the vertical y-axis
        self.heading = rotate(self.heading, angle=theta,
                              axis=(-self.heading.z,0,self.heading.x))
        # rotate all of the parts around the current position
        for part in self.parts:
            part.rotate(angle=theta, axis=(-self.heading.z,0,self.heading.x),
                        origin=self.pos)
            part.heading = self.heading
        for i in range(0,4):
            self.Lights[i].pos = self.parts[i].pos
            self.Lights[i].heading = self.heading


def collision(object1, object2):
    """ Handles the physics of a collision between two asteroids or between the
        ice cream truck and an asteroid.
    """

    relativeVelocity = object1.velocity - object2.velocity


    theta = diff_angle(object1.velocity,object2.velocity)

    changeInVelocity1 = relativeVelocity*(math.sqrt((object1.mass**2+object2.mass**2+
                                         2*object1.mass*object2.mass*math.cos(theta)))
                                         /(object1.mass+object2.mass))
   
    object1.pos += -norm(object2.pos - object1.pos)

    object1.velocity = changeInVelocity1 + object2.velocity
    

    changeInVelocity2 = (relativeVelocity*2*object1.mass*math.sin(theta/2)/
                         (object1.mass+object2.mass))

    object2.velocity = object2.velocity + changeInVelocity2
    

def menu():
    """ Prints the description of the game, directions, and the menu."""
    print 
    print "You wake up to find yourself in an ice cream truck. In space. "
    print
    print "You have no idea who you are or what you are doing there, but you " \
          "know you have a task to complete."
    print 
    Name = raw_input("What is your name? ")
    print 
    print "You must have taken a bump to the head when you got into the ice " \
          "cream truck, because you don't even remember your name! Your " \
          "name is actually Sally Ride. You have been kidnapped by " \
          "extraterrestrial space agents and must complete a mission! If you " \
          "fail, the space agents will destroy Planet Earth."
    print

    print "Your trusty computer Mel, between fits of weeping, tells you " \
          "that the only way to complete your mission is to knock " \
          "all asteroids in your new fun-sized universe into a supermassive " \
          "black hole with a bizarrely ineffective gravitational field. Mel " \
          "doesn't think you have a chance of succeeding, but promises to " \
          "tell corny jokes to keep the mood light."
    print
    Key = raw_input("Hit ENTER or RETURN to continue. ")
    print
    print "You look at the controls to the ice cream truck, and recognize a " \
          "large white piece of paper sitting on the drivers' seat.  The " \
          "paper contains the following instructions:"
    print
    print " TO OPERATE THIS MOTOR VEHICLE:"
    print "      HIT 'a' TO ACCELERATE.  "
    print "      HIT 'd' TO DECELERATE.  "
    print "      HIT 's' TO STOP INSTANTANEOUSLY.  "
    print "      HIT THE ARROW KEYS TO CONTROL THE ORIENTATION OF THE TRUCK.  "
    print "      RIGHT-CLICK AND DRAG TO CHANGE THE VIEW.  "
    print "WE ARE NOT RESPONSIBLE FOR DAMAGES INCURRED BY OPERATING THIS " \
          "MOTOR VEHICLE IN COMPLETELY INAPPROPRIATE CONTEXTS SUCH AS " \
          "OUTER SPACE. DRIVE AT YOUR OWN RISK."
    print
    Answer = raw_input("Are you ready to begin? ")
    print
    print "Good.  Choose a level of play: " 
    print  
    print " (1)   Easy   "         
    print " (2)   Medium "
    print " (3)   Hard   "  
    print
    Level = input("Which would you like to play? ")
    return Level


def main():

    Level = menu()

    # set up the visual conditions - the window is called "scene"
    scene.autoscale = True  # should the scene fill the window?
    scene.background = color.black  # the background "space" color

    AsteroidsIn = 0 

    if Level == 1:    # avoiding magic numbers!
        UR = 120
        NA = 2
        MINR = 15
        MAXR = 20
        D = 1
    elif Level == 2:
        UR = 180
        NA = 4
        MINR = 15
        MAXR = 20
        D = 1
    elif Level == 3:
        UR = 240
        NA = 6
        MINR = 15
        MAXR = 20
        D = 1
    elif Level == 0:
        UR = 360
        NA = 42
        MINR = 5
        MAXR = 20
        D = -100
    else:
        print "That is not a valid option."
        print "Try again!"
        lose()
    
    # the ice cream truck
    SPAM = ICT(pos=(0,0,0))
    SPAM.velocity = vector(40,0,20)
    SPAM.speed = 0
    
    # list of Asteroids
    LoA = []

    for i in range(NA):       # creates randomly sized and positioned asteroids
        x = random.uniform(-UR,UR)
        y = random.uniform(-UR,UR)
        z = random.uniform(-UR,UR)
        while mag(vector(x,y,z))> UR or mag(vector(x,y,z)-vector(-60,0,0))< 50:
            x = random.uniform(-UR,UR)
            y = random.uniform(-UR,UR)
            z = random.uniform(-UR,UR)
        r = random.uniform(MINR,MAXR)
        
        LoA  += [Asteroid(pos=(x,y,z), radius = r)]
        
        LoA[i].heading = norm(vector(random.random(),random.random(),
                                     random.random()))
        LoA[i].speed = random.uniform(5,15)
        LoA[i].velocity = LoA[i].heading * LoA[i].speed    


    # the black hole
    BlackHoleOutside = sphere(pos=(-60,0,0), radius=50,
                              color=(1,0,0), opacity=.25)
    BlackHoleInside = sphere(pos=(-60,0,0), radius=15,
                             color=(0,0,0), opacity=1)

    # the Universe
    Universe = sphere(pos=(0,0,0), radius = UR, color=(0,1,1), opacity = .2)

    # the main loop - handle user events
    while True:

        # It's easier to adjust constants if they
        # have names and are all in one place!
        TURN_AMOUNT = 5 # degrees
        ACCEL = 10 # acceleration at 3 meters per second squared

        C = 10000*D # gravitational constant - it's over 9000!!!
        
        rate(30)  # at most 30 loops per second

        dt = 1.0/30.0

        SPAM.forward(dt)  # handles the physics of the ice cream truck

        AGrav = C/mag(SPAM.pos - vector(-60,0,0))**2

        SPAM.velocity += AGrav*norm(-SPAM.pos + vector(-60,0,0))*dt

        if mag(SPAM.pos - vector(-60,0,0))<50:
            SPAM.velocity += AGrav*norm(-SPAM.pos + vector(-60,0,0))*dt

        if mag(SPAM.pos - vector(-60,0,0))<15:
            break
        
        AsteroidsIn = 0

        for asteroid in LoA:         # handles the physics of the asteroids.
            asteroid.pos += ((asteroid.velocity)*dt)
            asteroid.update()
            if mag(asteroid.pos)> (UR-asteroid.radius):
                asteroid.pos += -norm(asteroid.pos)
                asteroid.velocity = -asteroid.velocity
                
            if mag(asteroid.pos-SPAM.pos)<(asteroid.radius+SPAM.radius):
                collision(asteroid, SPAM)

            if mag(asteroid.pos - vector(-60,0,0))<15:
                asteroid.pos = vector(-60,0,0)
                asteroid.radius = 1
                asteroid.velocity = vector(0,0,0)
                asteroid.update()
                AsteroidsIn +=1
                
            if mag(asteroid.pos - vector(-60,0,0))>15:
                
                AGrav = C/mag(asteroid.pos - vector(-60,0,0))**2

                asteroid.velocity += AGrav*norm(-asteroid.pos + vector(-60,0,0))*dt

                if mag(asteroid.pos - vector(-60,0,0))<50:
                    asteroid.velocity+=AGrav*norm(-asteroid.pos+vector(-60,0,0))*dt
  

        if AsteroidsIn == NA:   # checks to see if the asteroids have fallen in
            break

        for i in range(0,NA):
            for j in range(i,NA):
                if mag(LoA[i].pos - LoA[j].pos) < (LoA[i].radius + LoA[j].radius):
                    collision(LoA[i], LoA[j])

                
                
        if scene.kb.keys: # is there a keyevent?
            s = scene.kb.getkey() # get keypress

            # controls for the ice cream truck
            if s == "right":
                SPAM.turnXZ(TURN_AMOUNT)
            if s == "left":
                SPAM.turnXZ(-TURN_AMOUNT)
            if s == "up":
                SPAM.turnUP(TURN_AMOUNT)
            if s == "down":
                SPAM.turnUP(-TURN_AMOUNT)
            if s == "a":      # going forward - accelerating!
                SPAM.velocity += ACCEL*dt*SPAM.heading
            if s == "d":     # going backward - decelerating!
                SPAM.velocity += -ACCEL*dt*SPAM.heading
            if s == "s":     # stops the truck - defying the laws of physics!
                SPAM.velocity = vector(0,0,0)

        if mag(SPAM.pos) > UR:
            SPAM.pos += -norm(SPAM.pos)
            SPAM.velocity = -SPAM.velocity


    if AsteroidsIn == NA:  # checks to see if you've won the game
        win(UR)

    if AsteroidsIn != NA:   # checks to see if you've lost the game
        lose(UR)


def lose(UR):
    """ You just lost the game."""
    Universe = sphere(pos=(0,0,0), radius = UR, color=(1,0,0), opacity = .9)
    print
    print
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print
    print "You thought the black hole looked so pretty and inviting that " \
          "you decided to make a visit to its center."
    print
    print "THAT WAS A BAD IDEA, SALLY RIDE."
    print
    print "The extraterrestrial space agents decided that earthlings must " \
          "not be so special after all...and are going to destroy the planet!"
    print
    print "Better luck next time!"
    print


def win(UR):
    """ What happens when you win.
    """
    for i in range(UR):
        x = random.uniform(-UR,UR)
        y = random.uniform(-UR,UR)
        z = random.uniform(-UR,UR)

        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        
        local_light(pos=vector(x,y,z),color=(r,g,b))  # SO PRETTY!!!
        firework = sphere(pos=vector(x,y,z), radius=1.5, color=(r,g,b))
        
    print
    print
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print
    print "VICTORY!!!"
    print
    print "You have won, against all odds.  You rejoice, and Mel tells even " \
          "cornier jokes than usual.  You find yourself suddenly transported " \
          "to extraterrestrial space agent headquarters, where you are " \
          "awarded with the Milky Way Medal of Bravery for your noble " \
          "efforts on behalf of the human race. Also, you get all the ice " \
          "cream in the truck."
    print
    print "Thanks for playing!  Hope to see you at camp!"
    print

