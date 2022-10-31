import socket
#import threading
import time
import pygame
pygame.init()

#--------------client_pong.py-------------#

WIDTH,HEIGHT=700,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

FPS=60
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

BLACK=(0,0,0)
WHITE=(255,255,255)
RADIUS=10
PADDLE_WIDTH,PADDLE_HEIGHT=20,100

def client_to_client_pong(msg):
    message=msg.split(",")
    if message[0]=="won":
        declare_winner(message)
    else:
        client_side_running(message)

def client_side_running(message):
    clock=pygame.time.Clock()
    clock.tick(FPS)
    user_input=""
    left_score,right_score=int(message[0]),int(message[1])
    left_paddle_x,left_paddle_y=int(message[2]),int(message[3])
    right_paddle_x,right_paddle_y=int(message[4]),int(message[5])
    ball_x,ball_y=int(message[6]),int(message[7])
    draw(left_score,right_score,left_paddle_x,left_paddle_y,right_paddle_x,right_paddle_y,ball_x,ball_y)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        user_input='right_peddle'+","+'up'
    elif keys[pygame.K_DOWN]:
        user_input='right_peddle'+","+'down'
    elif keys[pygame.K_w]:
        user_input='left_peddle'+","+'up'
    elif keys[pygame.K_s]:
        user_input='left_peddle'+","+'down'
    write(user_input)

def draw(left_score,right_score,left_paddle_x,left_paddle_y,right_paddle_x,right_paddle_y,ball_x,ball_y):
    WIN.fill(BLACK)
    left_score_text=SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_text=SCORE_FONT.render(f"{right_score}",1,WHITE)
    WIN.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    WIN.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    pygame.draw.rect(WIN,WHITE,pygame.Rect(left_paddle_x,left_paddle_y,PADDLE_WIDTH,PADDLE_HEIGHT))
    pygame.draw.rect(WIN,WHITE,pygame.Rect(right_paddle_x,right_paddle_y,PADDLE_WIDTH,PADDLE_HEIGHT))
    pygame.draw.circle(WIN,WHITE,(ball_x,ball_y),RADIUS)
    pygame.display.update()

def declare_winner(message):
    text = SCORE_FONT.render(message[1], 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

#---------------client.py-----------------#

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server='127.0.0.1'
port= 5555
client.connect((server,port))
data=""

username=input("Please enter your user name: ")

def receive():
    try:
        message=client.recv(2048).decode('utf-8')
        print("msg is ", message)
        if message=='Client_Name':
            client.send(username.encode('utf-8'))
        else:
            client_to_client_pong(message)
    except Exception as e:
        print("An error occured",e)
        time.sleep(10)
        client.close()

def write(data):
    try:
        client.send(data.encode('utf-8'))
    except socket.error as e:
        print(str(e))

while True:
    receive()

