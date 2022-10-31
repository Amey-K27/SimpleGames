import client
import pygame
pygame.init()

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
    print("msg is ", msg)
    message=msg.split(",")
    if message[0]=="won":
        declare_winner(message)
    else:
        client_side_running(message)

def client_side_running(message):
    run=True
    clock=pygame.time.Clock()
    while run:
        user_input=""
        clock.tick(FPS)
        left_score,right_score=int(message[0]),int(message[1])
        left_paddle_x,left_paddle_y=int(message[2]),int(message[3])
        right_paddle_x,right_paddle_y=int(message[4]),int(message[5])
        ball_x,ball_y=int(message[6]),int(message[7])
        draw(left_score,right_score,left_paddle_x,left_paddle_y,right_paddle_x,right_paddle_y,ball_x,ball_y)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            user_input='right_peddle'+","+'up'
        elif keys[pygame.K_DOWN]:
            user_input='right_peddle'+","+'down'
        elif keys[pygame.K_w]:
            user_input='left_peddle'+","+'up'
        elif keys[pygame.K_s]:
            user_input='left_peddle'+","+'down'
        client.write(user_input)

def draw(left_score,right_score,left_paddle_x,left_paddle_y,right_paddle_x,right_paddle_y,ball_x,ball_y):
    WIN.fill(BLACK)
    left_score_text=SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_text=SCORE_FONT.render(f"{right_score}",1,WHITE)
    WIN.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    WIN.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    pygame.draw.rect(WIN,WHITE,(left_paddle_x,left_paddle_y,WIDTH,HEIGHT))
    pygame.draw.rect(WIN,WHITE,(right_paddle_x,right_paddle_y,WIDTH,HEIGHT))
    pygame.draw.circle(WIN,WHITE,(ball_x,ball_y),RADIUS)
    pygame.display.update()


def declare_winner(message):
    text = SCORE_FONT.render(message[1], 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)