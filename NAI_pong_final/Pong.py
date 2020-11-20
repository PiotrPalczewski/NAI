# Autorzy - Norbert Daniluk, Piotr Palczewski
# Projekt gry Pong
# Zasady gry: zdobądź więcej punktów niż przeciwnik 
# poprzez doprowadzenie piłeczki do pola przeciwnika

#do działania wymagane jest zainstalowanie modułu turtle
import turtle
import winsound


class Pong():
    def __init__(self):
        self.game_window = turtle.Screen()
        self.paddle_1 = turtle.Turtle()
        self.paddle_2 = turtle.Turtle()
        self.ball = turtle.Turtle()
        self.show_score = turtle.Turtle()
        self.set_window()
        self.set_paddles()
        self.set_ball()
        self.set_scoreboard()
        self.set_keymap()
        self.score_1 = 0
        self.score_2 = 0

    # funkcje ruchu paletek - przesunięcie paletki o y pikseli
    #ruch paletki w górę
    def paddle1_up(self):
        if self.paddle_1.ycor() < 290:
            y = self.paddle_1.ycor()
            y += 30
            self.paddle_1.sety(y)

    def paddle2_up(self):
        if self.paddle_2.ycor() < 290:
            y = self.paddle_2.ycor()
            y += 25
            self.paddle_2.sety(y)

    #ruch paletki w dół
    def paddle1_down(self):
        if self.paddle_1.ycor() > -290:
            y = self.paddle_1.ycor()
            y -= 30
            self.paddle_1.sety(y)

    def paddle2_down(self):
        if self.paddle_2.ycor() > -290:
            y = self.paddle_2.ycor()
            y -= 25
            self.paddle_2.sety(y)

    def set_window(self):
        # inicjacja okna
        self.game_window.title("AI_Pong")
        self.game_window.bgcolor("black")
        self.game_window.setup(width=800, height=600)
        # game_window.tracer(0) #odpowiada za prędkość gry

    def set_paddles(self):
        # paletka gracza-1
        self.paddle_1.speed(0)
        self.paddle_1.shape("square")
        self.paddle_1.color("white")
        self.paddle_1.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle_1.penup()
        self.paddle_1.goto(-350, 0)

        # paletka gracza-2
        self.paddle_2.speed(0)
        self.paddle_2.shape("square")
        self.paddle_2.color("white")
        self.paddle_2.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle_2.penup()
        self.paddle_2.goto(350, 0)

    def set_ball(self):
        # pileczka
        self.ball.speed(0)
        self.ball.shape("square")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, 0)
        # piksele ruchu piłeczki - prędkość gry
        self.ball.dx = 5
        self.ball.dy = 5

    def set_scoreboard(self):
        # wyświetlenie wyników
        self.show_score.speed(0)
        self.show_score.shape("square")
        self.show_score.color("white")
        self.show_score.penup()
        self.show_score.hideturtle()
        self.show_score.goto(0, 260)
        self.show_score.write("Player 1: 0  Player 2: 0", align="center", font=("Courier", 24, "normal"))

    def set_keymap(self):
        # czytanie klawiszy
        self.game_window.listen()
        # klawisze gracza 1
        self.game_window.onkeypress(self.paddle2_up, "Up")
        self.game_window.onkeypress(self.paddle2_down, "Down")
        # klawisze gracza 2
        self.game_window.onkeypress(self.paddle1_up, "w")
        self.game_window.onkeypress(self.paddle1_down, "s")

    #pętla gry
    def game_loop(self):

        while True:
            self.game_window.update()

            if self.paddle_1.ycor() < self.ball.ycor():
                self.paddle_1.sety(self.paddle_1.ycor() + 5)
            elif self.paddle_1.ycor() > self.ball.ycor():
                self.paddle_1.sety(self.paddle_1.ycor() - 5)


            # ruch piłeczki
            self.ball.setx(self.ball.xcor() + self.ball.dx)
            self.ball.sety(self.ball.ycor() + self.ball.dy)

            # kolizja ze ścianką

            # dla odbijających ścianek
            if self.ball.ycor() > 290:
                self.ball.sety(290)
                self.ball.dy *= -1
                # winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk
                # odbijania
                # piłeczki
            elif self.ball.ycor() < -290:
                self.ball.sety(-290)
                self.ball.dy *= -1
                # winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk
                # odbijania
                # piłeczki

            # dla ścianek prawej i lewej
            if self.ball.xcor() > 350:
                self.score_1 += 1
                self.show_score.clear()
                self.show_score.write("Player 1: {} Player 2 {}".format(self.score_1, self.score_2), align="center",
                                      font=("Courier", 24, "normal"))
                self.ball.goto(0, 0)
                self.ball.dx = 5
            elif self.ball.xcor() < -350:
                self.score_2 += 1
                self.show_score.clear()
                self.show_score.write("Player 1: {} Player 2 {}".format(self.score_1, self.score_2), align="center",
                                      font=("Courier", 24, "normal"))
                self.ball.goto(0, 0)
                self.ball.dx = 5

            # odbijanie piłeczki
            if self.ball.xcor() < -340 and self.paddle_1.ycor() + 50 > self.ball.ycor() > self.paddle_1.ycor() - 50:
                #self.ball.setheading(360-ball.heading())
                self.ball.dx *= -1.3
                # winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk odbijania piłeczki

            elif self.ball.xcor() > 340 and self.paddle_2.ycor() + 50 > self.ball.ycor() > self.paddle_2.ycor() - 50:
                #self.ball.setheading(360-ball.heading())
                self.ball.dx *= -1.3
                # winsound.PlaySound('bounce.wav', winsound.SND_ASYNC) #dzwięk odbijania piłeczki

    def play(self, **kwargs):
        self.game_loop()

