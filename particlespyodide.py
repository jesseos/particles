#from particle import Particle

class Particle(object):
    def __init__(self, position, w, type, ID):
        self.position = position
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)
        self.magnitude = (0.5)
    
        self.w = w
        self.mass = self.w*0.3
        
        self.type = type
        
        self.doesSplit = False
        
        self.ID = ID
        
        self.health = 25*self.mass
        self.alive = True
        
        self.isCrowded = False
        
    def attract(self):
        for p in particles:
            distance = dist(self.position.x, self.position.y, p.position.x, p.position.y)
            
            if distance != 0:
                nDistance = 1/distance
            else:
                nDistance = 0
            
            if (self.type == p.type):
                fAttract = PVector.sub(p.position, self.position)
                #fAttract.mult(1+p.mass)
                fAttract.div(self.mass)
                #fAttract.setMag(self.magnitude*(1-(distance*0.000001)))
                fAttract.setMag(self.magnitude*nDistance*5)
                self.acceleration.add(fAttract)
            else:
                fRepel = PVector.sub(p.position, self.position)
                #fRepel.mult(1+p.mass)
                fRepel.div(self.mass)
                #fRepel.setMag(self.magnitude*(1-(distance*0.000001)))
                fRepel.setMag(self.magnitude*nDistance)
                self.acceleration.sub(fRepel)
            
            if mousePressed == True:
                distMouse = dist(self.position.x, self.position.y, mouseX, mouseY)
                mouse = PVector(mouseX, mouseY)
                fMouse = PVector.sub(mouse, self.position)
                fMouse.div(self.mass)
                #fMouse.setMag(self.magnitude*(1-(distMouse*0.001)))
                fMouse.setMag(self.magnitude*nDistance*20)
                self.acceleration.add(fMouse)
    
    def crowded(self):
        numClose = 0
        for p in particles:
            distance = dist(self.position.x, self.position.y, p.position.x, p.position.y)
            if distance != 0:
                nDistance = 1/distance
            else:
                nDistance = 0
                
            if ((distance) < (abs(self.w-p.w))) and (p.ID != self.ID):
                numClose += 1
                
            #if  (((distance) < (self.w*2)) and (numClose >= 3) and (self.type == p.type)):
            if  (((distance) < (self.w)) and (self.type == p.type)) and (self.ID != p.ID):
                fCrowded = PVector.sub(p.position, self.position)
                #fCrowded.mult(1+p.mass)
                fCrowded.div(self.mass)
                fCrowded.setMag(self.magnitude*nDistance)
                self.acceleration.add(fCrowded)

                canSplit = int(random(splitChance))
                if canSplit == splitChance/2 and self.w > 75:
                    self.w = self.w/2
                    self.mass = self.w*.03
                    self.doesSplit = True
                else:
                    self.doesSplit = False

                self.health += 1
                
    def friction(self):
        fFriction = self.velocity.get()
        fFriction.normalize()
        c = -0.1
        fFriction.mult(c)
        fFriction.div(self.mass)
        self.acceleration.add(fFriction)
        
    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(20)
        self.position.add(self.velocity)
        self.acceleration.mult(0)
        self.health -= 0.3
        
        self.w += 0.01
        self.mass = self.w*.3
        
        if self.health <= 0:
            self.alive = False
            
    def changeColor(self):
        for p in particles:
            distance = dist(self.position.x, self.position.y, p.position.x, p.position.y)
            if distance != 0:
                if (distance < self.w + p.w + 20) and (self.type == p.type):
                    self.isCrowded = True
                    noFill()
                    stroke(255)
                    strokeWeight(1)
                    ellipse((self.position.x+p.position.x)/2, (self.position.y+p.position.y)/2, self.w+distance, self.w+distance)
                else:
                    self.isCrowded = False
            
    def display(self):
        #noStroke()
        #fill(colorRule[self.type][0], colorRule[self.type][1], colorRule[self.type][2])
        # if self.isCrowded == True:
        #     fill(230)
        # else:
        #     fill(colorRule[self.type])
        # if (abs(abs(255-bkgColor)-colorRule[self.type])) <= 20:
        #     strokeWeight(1)
        #     stroke(abs(255-colorRule[self.type]))
        # else:
        #     noStroke()
        fill(colorRule[self.type])
        ellipse(self.position.x, self.position.y, self.w, self.w)
    
        
    def checkEdges(self):
        if (self.position.x > winX):
            self.position.x = winX
            self.velocity.x *= -0.5
        elif(self.position.x < 0):
            self.position.x = 0
            self.velocity.x *= -0.5
        if (self.position.y > winY):
            self.position.y = winY
            self.velocity.y *= -0.5
        elif(self.position.y < 0):
            self.position.y = 0
            self.velocity.y *= -0.5
            
numTypes = 10    
colorRule = []

splitChance = 500

winX = 1000
winY = 1000
particles = []
numParticles = 10
assignID = 0
maxCrowding = 5

colorGoal = 0
bkgColor = 128

def setup():
    size(winX, winY)
    global assignID
    for i in range(numParticles):
        particles.append(Particle(PVector(random(winX), random(winY)), int(random(20, 100)), int(random(2)), assignID))
        assignID += 1
        
    for i in range(numTypes):
        #colorRule.append([random(255), random(255), random(255)])
        colorRule.append(random(255))
        
def draw():
    global bkgColor
    colorGoal = 0
    for p in particles:
        colorGoal += colorRule[p.type]
    colorGoal = colorGoal/len(particles)
    #background(200, 220, 230)
    if bkgColor < colorGoal:
        bkgColor += 1
    elif bkgColor > colorGoal:
        bkgColor -= 1
    elif bkgColor == colorGoal:
        bkgColor = colorGoal 
    background(abs(255-bkgColor))
    global assignID
    for p in particles:
        if p.alive == True:
            p.attract()
            p.crowded()
            p.friction()
            p.checkEdges()
            p.update()
            p.changeColor()
            if p.doesSplit == True:
                particles.append(Particle(PVector(p.position.x+p.w+5, p.position.y), p.w, int(random(numTypes)), assignID))
                assignID += 1
                p.doesSplit = False
            #print(len(particles))
    for p in particles:
        if p.alive == True:
            p.display()
            
            
    for i in range(len(particles)):
        if particles[i].alive == False:
            particles.pop(i)
            break
        
        