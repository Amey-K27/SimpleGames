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
        pygame.display.flip()
    
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
        pygame.display.flip() 
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.surface=pygame.display.set_mode((400,400))
        self.snake=Snake(self.surface,5)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()
    
    def is_collision(self,x1,y1,x2,y2):
        if (x1==x2 and y1==y2):
            return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(100,100))
        pygame.display.flip()


    def play(self):
        self.snake.walk()
        self.apple.draw()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                return False
        
        return True

    def run(self):
        running =True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

            if self.play()==False:
                break
            else:
                time.sleep(1)
        self.display_score()
        time.sleep(5)
if __name__=="__main__":
    game=Game()
    game.run()