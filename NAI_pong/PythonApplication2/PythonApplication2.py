#Autorzy - Norbert Daniluk, Piotr Palczewski
#Projekt gry Pong z użyciem EasyAI

import turtle
import winsound

#inicjacja okna
game_window = turtle.Screen()
game_window.title("AI_Pong")
game_window.bgcolor("black")
game_window.setup(width=800, height=600)
#game_window.tracer(0) #odpowiada za prędkość gry

#paletka gracza-1
paddle_1 = turtle.Turtle()
paddle_1.speed(0)
paddle_1.shape("square")
paddle_1.color("white")
paddle_1.shapesize(stretch_wid=5, stretch_len=1)
paddle_1.penup()
paddle_1.goto(-350,0)

#paletka gracza-2
paddle_2 = turtle.Turtle()
paddle_2.speed(0)
paddle_2.shape("square")
paddle_2.color("white")
paddle_2.shapesize(stretch_wid=5, stretch_len=1)
paddle_2.penup()
paddle_2.goto(350,0)

#pileczka
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
#piksele ruchu piłeczki - prędkość gry
ball.dx = 6
ball.dy = 6

#wyświetlenie wyników
score_1 = 0
score_2 = 0
show_score = turtle.Turtle()
show_score.speed(0)
show_score.shape("square")
show_score.color("white")
show_score.penup()
show_score.hideturtle()
show_score.goto(0, 260)
show_score.write("Player 1: 0  Player 2: 0", align="center", font=("Courier", 24, "normal"))


#funcje ruchu paletek
def paddle1_up():
    if paddle_1.ycor() < 290:
        y = paddle_1.ycor()
        y += 20
        paddle_1.sety(y)

def paddle1_down():
    if paddle_1.ycor() > -290:
        y = paddle_1.ycor()
        y -= 20
        paddle_1.sety(y)

def paddle2_up():
    if paddle_2.ycor() < 290:
        y = paddle_2.ycor()
        y += 20
        paddle_2.sety(y)

def paddle2_down():
    if paddle_2.ycor() > -290:
        y = paddle_2.ycor()
        y -= 20
        paddle_2.sety(y)

#czytanie klawiszy
game_window.listen()
#klawisze gracza 1
game_window.onkeypress(paddle2_up, "Up")
game_window.onkeypress(paddle2_down, "Down")
#klawisze gracza 2
game_window.onkeypress(paddle1_up, "w")
game_window.onkeypress(paddle1_down, "s")


#pętla gry
while True:
    game_window.update()

    #ruch piłeczki
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #kolizja ze ścianką

    #dla odbijających ścianek
    if ball.ycor()>290:
        ball.sety(290)
        ball.dy *= -1
        #winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk odbijania piłeczki
    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        #winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk odbijania piłeczki

    #dla ścianek prawej i lewej
    if ball.xcor()>350:
        score_1 += 1
        show_score.clear()
        show_score.write("Player 1: {} Player 2 {}".format(score_1, score_2), align="center", font=("Courier", 24, "normal"))
        ball.goto(0,0)
        ball.dx *= -1
    elif ball.xcor()<-350:
        score_2 += 1
        show_score.clear()
        show_score.write("Player 1: {} Player 2 {}".format(score_1, score_2), align="center", font=("Courier", 24, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1

    #odbijanie piłeczki
    if ball.xcor() < -340 and ball.ycor() < paddle_1.ycor() + 50 and ball.ycor() > paddle_1.ycor() - 50:
        ball.dx *= -1
        #winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk odbijania piłeczki
    elif ball.xcor() > 340 and ball.ycor() < paddle_2.ycor() + 50 and ball.ycor() > paddle_2.ycor() - 50:
        ball.dx *= -1
        #winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk odbijania piłeczki