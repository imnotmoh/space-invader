import time
from turtle import Turtle,Screen
from alien import *
pace = 3
game_is_on  = True
space_ship = "outfile.gif"

myscreen = Screen()
myscreen.setup(height=1000,width=800)
myscreen.addshape("alien_t.gif")
myscreen.addshape(space_ship)
myscreen.title("moh's space invader")
myscreen.bgcolor("black")
myscreen.tracer(0)
game_score=Score()
lives = Lives()
dead_list = []

def set():
    all_obstacle=arrange_obstacle()
    line = Laser()
    alien_list, alien_gun = arrange_alien(myscreen)
    return all_obstacle,line,alien_list,alien_gun

all_obstacle,line,alien_list,alien_gun =set()
star = Space_ship(line)
mile_stone = 3000

while game_is_on:
    myscreen.update()
    myscreen.listen()
    # adds life if mile stone is reached
    if game_score.score == mile_stone:
        lives.lives += 1
        lives.update_()
        mile_stone += 3000
    # checks if all aliens are dead
    if len(alien_list) < 1:
        star.goto(0,star.ycor())
        for i in all_obstacle:
            i.hideturtle()
        all_obstacle,line,alien_list,alien_gun=set()

    edge,hit = alien_prop(alien_list, pace, star.laser,star, alien_gun, all_obstacle,game_score,myscreen,dead_list)
    # chages the direction of movement in aliens are are the edge of the screen
    if edge:
        pace *= -1
    # checks if spaceship has been hit
    if hit:
        lives.reduce_lives()
        star.goto(0,-280)
        star.laser.goto(0,-280)
        for n in range(10):
            star.hideturtle()
            myscreen.update()
            time.sleep(0.05)
            star.showturtle()
            myscreen.update()
            time.sleep(0.05)
    myscreen.onkey(key="space",fun=star.shoot)
    myscreen.onkey(key="Right", fun=star.right)
    myscreen.onkey(key="Left",fun=star.left)

    if star.fire:
        star.laser.showturtle()
        star.laser.forward(10)
    if star.laser.ycor() > 500:
        star.laser.hideturtle()
        star.laser.goto(star.xcor(),star.ycor())
        star.fire = False
    # resets the game if all lives has been exhausted
    if lives.lives < 1:
        time.sleep(3)
        star.goto(0,star.ycor())
        for i in all_obstacle:
            i.hideturtle()
        for i in alien_list:
            i.hideturtle()
        for i in alien_gun:
            i.hideturtle()
        all_obstacle,line,alien_list,alien_gun=set()
        lives.lives=3
        lives.update_()
        game_score.score=0
        game_score.add()








myscreen.mainloop()
