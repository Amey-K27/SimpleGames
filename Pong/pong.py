import pygame
pygame.init()

WIDTH,HEIGHT=700,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

FPS=60
WINNING_SCORE=5
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

PADDLE_WIDTH,PADDLE_HEIGHT=20,100

BLACK=(0,0,0)
WHITE=(255,255,255)
RADIUS=10

class Paddle:
    COLOR=WHITE
    vel=5
    def __init__(self,x,y,width,height) -> None:
        self.x,self.original_x=x,x
        self.y,self.original_y=y,y
        self.width=width
        self.height=height
    
    def draw(self,win):
        pygame.draw.rect(win,self.COLOR,(self.x,self.y,self.width,self.height))
        pygame.display.update()

    def move(self,up):
        if up:
            self.y-=self.vel
        else:
            self.y+=self.vel
    
    def reset(self):
        self.x=self.original_x
        self.y=self.original_y

class Ball:
    COLOR=WHITE
    VEL=5
    def __init__(self,x,y,radius) -> None:
        self.x,self.original_x=x,x
        self.y,self.original_y=y,y
        self.radius=radius
        self.x_vel=self.VEL
        self.y_vel=0
    
    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)
        pygame.display.update()

    def move(self):
        self.x+=self.x_vel
        self.y+=self.y_vel
    
    def reset(self):
        self.x=self.original_x
        self.y=self.original_y
        self.y_vel=0
        self.x_vel*=-1

def draw(win,left_score,right_score):
    win.fill(BLACK)
    left_score_text=SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_text=SCORE_FONT.render(f"{right_score}",1,WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))
    pygame.display.update()

def move_peddle(keys,left_peddle,right_peddle):
    if keys[pygame.K_UP] and right_peddle.y-right_peddle.vel>=0:
        right_peddle.move(up=True)
    if keys[pygame.K_w] and left_peddle.y-left_peddle.vel>=0:
        left_peddle.move(up=True)
    if keys[pygame.K_s] and left_peddle.y+left_peddle.vel+left_peddle.height<=HEIGHT:
        left_peddle.move(up=False)
    if keys[pygame.K_DOWN] and right_peddle.y+right_peddle.vel+right_peddle.height<=HEIGHT:
        right_peddle.move(up=False)

def handle_collision(ball,left_paddle,right_paddle):
    if ball.y+ball.radius>=HEIGHT or ball.y-ball.radius<=0:
        ball.y_vel*=-1
    if ball.x_vel<0:        #ball moving toward left side
        if ball.y>=left_paddle.y and ball.y<=left_paddle.y+left_paddle.height:
            if ball.x-ball.radius<=left_paddle.x+left_paddle.width:
                ball.x_vel*=-1

                middle_y=left_paddle.y+left_paddle.height/2
                difference_of_y=middle_y-ball.y
                ball.y_vel=-1*(difference_of_y*ball.VEL)/(left_paddle.height/2)
    else:
        if ball.y>=right_paddle.y and ball.y<=right_paddle.y+right_paddle.height:
            if ball.x+ball.radius>=right_paddle.x:
                ball.x_vel*=-1

                middle_y=right_paddle.y+right_paddle.height/2
                difference_of_y=middle_y-ball.y
                ball.y_vel=-1*(difference_of_y*ball.VEL)/(right_paddle.height/2)

def main():
    run=True
    clock=pygame.time.Clock()
    left_paddle=Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle=Paddle(WIDTH-10-PADDLE_WIDTH,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    ball=Ball(WIDTH//2,HEIGHT//2,RADIUS)

    left_score=0
    right_score=0

    while run:
        clock.tick(FPS)
        draw(WIN,left_score,right_score)
        left_paddle.draw(WIN)
        right_paddle.draw(WIN)
        ball.draw(WIN)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
        keys = pygame.key.get_pressed()
        move_peddle(keys,left_paddle,right_paddle)

        ball.move()
        handle_collision(ball,left_paddle,right_paddle)

        if ball.x<=0:
            right_score+=1
            ball.reset()
        if ball.x>=WIDTH:
            left_score+=1
            ball.reset()
        
        won=False
        if right_score>=WINNING_SCORE:
            won=True
            win_text="Right player won"
        if left_score>=WINNING_SCORE:
            won=True
            win_text="Left player won"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
    pygame.quit()


if __name__=="__main__":
    main()