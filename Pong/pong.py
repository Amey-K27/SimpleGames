import pygame
pygame.init()

WIDTH,HEIGHT=700,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

FPS=60

PADDLE_WIDTH,PADDLE_HEIGHT=20,100

BLACK=(0,0,0)
WHITE=(255,255,255)

class Paddle:
    COLOR=WHITE
    vel=5
    def __init__(self,x,y,width,height) -> None:
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    
    def draw(self,win):
        print(self.x)
        pygame.draw.rect(win,self.COLOR,(self.x,self.y,self.width,self.height))
        pygame.display.update()

    def move(self,up):
        if up:
            self.y-=self.vel
            print("going up")
        else:
            self.y+=self.vel

def draw(win):
    win.fill(BLACK)
    pygame.display.update()

def move_peddle(keys,left_peddle,right_peddle):
    if keys[pygame.K_UP] and right_peddle.y-right_peddle.vel>=0:
        print("right_key")
        right_peddle.move(up=True)
    if keys[pygame.K_w] and left_peddle.y-left_peddle.vel>=0:
        left_peddle.move(up=True)
    if keys[pygame.K_s] and left_peddle.y+left_peddle.vel+left_peddle.height<=HEIGHT:
        left_peddle.move(up=False)
    if keys[pygame.K_DOWN] and right_peddle.y+right_peddle.vel+right_peddle.height<=HEIGHT:
        right_peddle.move(up=False)
    

def main():
    run=True
    clock=pygame.time.Clock()
    left_paddle=Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle=Paddle(WIDTH-10-PADDLE_WIDTH,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    
    while run:
        clock.tick(FPS)
        draw(WIN)
        left_paddle.draw(WIN)
        right_paddle.draw(WIN)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
        keys = pygame.key.get_pressed()
        move_peddle(keys,left_paddle,right_paddle)
    pygame.quit()


if __name__=="__main__":
    main()