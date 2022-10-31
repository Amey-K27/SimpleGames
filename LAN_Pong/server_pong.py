import pygame
from server import server_pong_to_server

WINNING_SCORE=5
WIDTH,HEIGHT=700,500
FPS=60
RADIUS=10
PADDLE_WIDTH,PADDLE_HEIGHT=20,100

class Paddle:
    vel=5
    def __init__(self,x,y,width,height) -> None:
        self.x,self.original_x=x,x
        self.y,self.original_y=y,y
        self.width=width
        self.height=height

    def move(self,up):
        if up:
            self.y-=self.vel
        else:
            self.y+=self.vel
    
    def reset(self):
        self.x=self.original_x
        self.y=self.original_y

class Ball:
    VEL=5
    def __init__(self,x,y,radius) -> None:
        self.x,self.original_x=x,x
        self.y,self.original_y=y,y
        self.radius=radius
        self.x_vel=self.VEL
        self.y_vel=0

    def move(self):
        self.x+=self.x_vel
        self.y+=self.y_vel
    
    def reset(self):
        self.x=self.original_x
        self.y=self.original_y
        self.y_vel=0
        self.x_vel*=-1

def move_peddle(data):
    if data:
        user_input=data.split(",")
        if user_input[0]=="right_peddle":
            if user_input[1]=="up" and main().right_peddle.y-main().right_peddle.vel>=0:
                main().right_peddle.move(up=True)
            if user_input[1]=="down" and main().right_peddle.y+main().right_peddle.vel+main().right_peddle.height<=HEIGHT:
                main().right_peddle.move(up=False)
        else:
            if user_input[1]=="up" and main().left_peddle.y-main().left_peddle.vel>=0:
                main().left_peddle.move(up=True)
            if user_input[1]=="up" and main().left_peddle.y+main().left_peddle.vel+main().left_peddle.height<=HEIGHT:
                main().left_peddle.move(up=False)
    

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
        server_pong_to_server(str(left_score)+','+str(right_score)+','+str(left_paddle.x)+','+str(left_paddle.y)+','+str(right_paddle.x)+','+str(right_paddle.y)+','+str(ball.x)+','+str(ball.y))
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
            server_pong_to_server(str("won"+","+win_text))
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
    pygame.quit()
    