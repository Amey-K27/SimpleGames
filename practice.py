import pygame,time,random
from pygame.locals import *
SIZE=40
class Apple():
    def __init__(self,surface) -> None:
        self.parent_screen=surface
        self.image=pygame.image.load("resources/apple.jpg").convert()
        self.x=0
        self.y=0
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
    
    def move(self):
        self.x=random.randint(1,9)*SIZE
        self.y=random.randint(1,9)*SIZE

class Snake():
    def __init__(self,surface,length) -> None:
        self.parent_screen=surface
        self.block=pygame.image.load("resources/block.jpg").convert()   #size of block is 40*40
        self.x,self.y=0,0
        self.direction="down" 
        self.length=length
        self.x=[40]*length
        self.y=[40]*length

    def move_left(self):
        self.direction="left"
    
    def move_right(self):
        self.direction="right"
    
    def move_up(self):
        self.direction="up"
    
    def move_down(self):
        self.direction="down"
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=="left":
            self.x[0]-=SIZE
        if self.direction=="right":
            self.x[0]+=SIZE
        if self.direction=="up":
            self.y[0]-=SIZE
        if self.direction=="down":
            self.y[0]+=SIZE
        self.draw()

    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

def play(self):
    self.apple.draw()
    self.snake.walk()
    pygame.display.flip()

if __name__=="__main__":   
    pygame.init()
    surface=pygame.display.set_mode((400,400))
    apple=Apple(surface)
    apple.draw()
    snake=Snake(surface,5)
    snake.draw()
    running =True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        play()
        time.sleep(.5)
