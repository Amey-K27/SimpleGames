import socket
import threading
import pygame
import time

#----------------Server_pong.py-------------------#
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

def move_paddle(data,left_paddle,right_paddle):
    #print("data",data)
    if data:
        user_input=data.split(",")
        #print("user_input",user_input)
        if user_input[0]=="right_paddle":
            if user_input[1]=="up" and right_paddle.y-right_paddle.vel>=0:
                right_paddle.move(up=True)
            if user_input[1]=="down" and right_paddle.y+right_paddle.vel+right_paddle.height<=HEIGHT:
                right_paddle.move(up=False)
        else:
            if user_input[1]=="up" and left_paddle.y-left_paddle.vel>=0:
                left_paddle.move(up=True)
            if user_input[1]=="down" and left_paddle.y+left_paddle.vel+left_paddle.height<=HEIGHT:
                left_paddle.move(up=False)
    

def handle_collision(ball,left_paddle,right_paddle):
    if ball.y+ball.radius>=HEIGHT or ball.y-ball.radius<=0:
        ball.y_vel*=-1
    if ball.x_vel<0:        #ball moving toward left side
        if ball.y>=left_paddle.y and ball.y<=left_paddle.y+left_paddle.height:
            if ball.x-ball.radius<=left_paddle.x+left_paddle.width:
                ball.x_vel*=-1

                middle_y=left_paddle.y+left_paddle.height/2
                difference_of_y=middle_y-ball.y
                ball.y_vel=int(-1*(difference_of_y*ball.VEL)/(left_paddle.height/2))
    else:
        if ball.y>=right_paddle.y and ball.y<=right_paddle.y+right_paddle.height:
            if ball.x+ball.radius>=right_paddle.x:
                ball.x_vel*=-1

                middle_y=right_paddle.y+right_paddle.height/2
                difference_of_y=middle_y-ball.y
                ball.y_vel=int(-1*(difference_of_y*ball.VEL)//(right_paddle.height/2))
                

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
        #------for debugging
        #print(str(left_score)+','+str(right_score)+','+str(left_paddle.x)+','+str(left_paddle.y)+','+str(right_paddle.x)+','+str(right_paddle.y)+','+str(ball.x)+','+str(ball.y))
        
        server_to_client(str(left_score)+','+str(right_score)+','+str(left_paddle.x)+','+str(left_paddle.y)+','+str(right_paddle.x)+','+str(right_paddle.y)+','+str(ball.x)+','+str(ball.y))
        time.sleep(0.015)
        ball.move()
        handle_collision(ball,left_paddle,right_paddle)
            #To receive userID we are sending request
        for c in clients:
            c.send('user_input'.encode('utf-8'))
            user_input=c.recv(2048).decode('utf-8')
            if user_input!="none":
                move_paddle(user_input,left_paddle,right_paddle)
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
            server_to_client(str("won"+","+win_text))
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
    pygame.quit()


#--------Server.py---------------------#

server="127.0.0.1"
port= 5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen()
users=[]
clients=[]

def server_to_client(message):
    for c in clients:
        c.send(message.encode('utf-8'))

#----------Need to use this to handle when user disconnects.
"""
def handle(client):
    while True:
        try:
            data=client.recv(2048).decode('utf-8')
            move_peddle(data)
        except:
            if client in clients:
                index=clients.index(client)
                user=users[index]
                clients.remove(client)
                client.close()
                print(f'{user} left the game')
                users.remove(user)"""

def establish_connection():
    no_of_users=0
    while True:
        client,address=s.accept()                     #to accept users
        client.send('Client_Name'.encode('utf-8'))    #To receive userID we are sending request
        user_id=client.recv(2048).decode('utf-8')     #To receive userID 
        users.append(user_id)
        clients.append(client)

        print(f'User connected: {user_id} and address is {address}')
        no_of_users+=1
        
        #thread=threading.Thread(target=handle,args=(client,))
        #thread.start()
        if no_of_users==2:
            break
        for c in clients:
            print(c)
    main()

print("Waiting for a connections, Server Started")
establish_connection()
    