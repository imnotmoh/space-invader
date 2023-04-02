from turtle import Turtle, Screen


class Alien(Turtle):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.penup()
        self.fire = False
        self.speed("fastest")
    # sets fire to true if shots been fired
    def alien_shoot(self):
        self.fire = True


class Laser(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("#67c94d")
        self.shapesize(stretch_wid=0.1, stretch_len=1.5)
        self.penup()
        self.hideturtle()
        self.setheading(90)
        self.speed("fastest")


class Space_ship(Turtle):
    def __init__(self, laser: Turtle):
        super().__init__()
        self.shape("outfile.gif")
        self.penup()
        self.goto(0, -280)
        self.laser = laser
        self.laser.hideturtle()
        self.laser.penup()
        self.laser.goto(0, -280)
        self.fire = False
        self.speed("fastest")
    # sets fire to true if shots been fired
    def shoot(self):
        if self.laser.ycor() < -270:
            self.fire = True
    # move right
    def right(self):
        self.goto(self.xcor() + 10, self.ycor())
        if not self.fire:
            self.laser.goto(self.xcor(), self.ycor())
    # move left
    def left(self):
        self.goto(self.xcor() - 10, self.ycor())
        if not self.fire:
            self.laser.goto(self.xcor(), self.ycor())



def arrange_alien(screen):
    alien_list = []
    alien_gun_list = []
    x = -250
    y = 400
    for n in range(24):
        alien_list.append(Alien(screen))
        alien_gun_list.append(Laser())
        alien_list[n].goto(x, y)
        alien_list[n].shape("alien_t.gif")
        x += 60
        if x > 200:
            x = -250
            y -= 45
    return alien_list, alien_gun_list


# game physics
def alien_prop(alien_list: list, pace, laser: Turtle, space_ship: Turtle, alien_gun_list, obstacle_list,score,screen: Screen, dead_gun):
    import random
    edge = False
    hit = False
    track = 0
    # for the aliens movement
    for alien in alien_list:
        alien.goto(alien.xcor() + pace, alien.ycor())
        # checks if the aliens gun has been shot
        if not alien.fire:
            alien_gun_list[track].hideturtle()
            alien_gun_list[track].goto(alien.xcor() + pace, alien.ycor())
            # to increase the odds of firing
            probability = random.randint(0, 200 + round((len(alien_list)/24) * 300))
            # probality of an alien shooting is 1 of probability
            if probability == 5:
                alien.fire = True
        else:
            alien_gun_list[track].showturtle()
            alien_gun_list[track].backward(10)
        # returns laser  to the alien if it has passed a coordinate
        if alien_gun_list[track].ycor() < -300:
            alien_gun_list[track].hideturtle()
            alien_list[track].fire = False

        if alien.xcor() > 350 or alien.xcor() < -350:
            edge = True

        # checks if laser has hit an obstacle
        for i in obstacle_list:
            if alien_gun_list[track].distance(i) < i.dist:
               if alien_gun_list[track].xcor() + 2 >= i.xcor() >= alien_gun_list[track].xcor() or alien_gun_list[track].xcor() - 2 <= i.xcor() <= alien_gun_list[track].xcor():
                   if i.lenght > 1:
                       alien.fire = False
                       alien_gun_list[track].hideturtle()
                       i.lenght -= 1
                       i.dist = (50 * i.lenght) / 4.16
                       i.shapesize(0.1, i.lenght)
                       i.backward(i.rev_dist)
                       i.rev_dist += (i.lenght / 10) - 0.5 - 0.05
                       alien_gun_list[track].goto(alien.xcor(), alien.ycor())
                   else:
                       i.hideturtle()
                       obstacle_list.remove(i)

            # space ship laser hits an obstacle
            if laser.distance(i) < i.dist:
                if laser.xcor() + 2 >= i.xcor() >= laser.xcor() or laser.xcor() - 2 <= i.xcor() <= laser.xcor():
                    if i.lenght > 1:
                        i.lenght -= 1
                        i.dist = (50 * i.lenght) / 4.16
                        i.shapesize(0.1, i.lenght)
                        i.forward(i.rev_dist)
                        i.rev_dist += (i.lenght / 10) - 0.5 - 0.05
                        laser.hideturtle()
                        laser.goto(space_ship.xcor(), space_ship.ycor())
                        space_ship.fire = False
                    else:
                        i.hideturtle()
                        obstacle_list.remove(i)

        # checks if space ship has been hit
        if alien_gun_list[track].distance(space_ship) < 75:
            if alien_gun_list[track].xcor() + 25 >= space_ship.xcor() >= alien_gun_list[track].xcor() or alien_gun_list[track].xcor() - 25 <= space_ship.xcor() <= alien_gun_list[track].xcor():
                alien_gun_list[track].hideturtle()
                alien_gun_list[track].goto(alien.xcor(), alien.ycor())
                hit = True


        #checks if an alien has been hit
        if laser.distance(alien) < 25 and laser.ycor() < alien.ycor() < laser.ycor() + 25:
            score.score += 100
            score.add()
            alien.hideturtle()
            alien_list.remove(alien)
            dead_gun.append(alien_gun_list[track])
            alien_gun_list.pop(track)
            laser.hideturtle()
            laser.goto(space_ship.xcor(), space_ship.ycor())
            space_ship.fire = False
        # checks if alien laser collides with space ship laser
        elif alien_gun_list[track].distance(laser) < 35 and alien.fire:
            if alien_gun_list[track].xcor() + 3 >= laser.xcor() >= alien_gun_list[track].xcor() or alien_gun_list[track].xcor() - 3 <= laser.xcor() <= alien_gun_list[track].xcor():
                laser.hideturtle()
                laser.goto(space_ship.xcor(), space_ship.ycor())
                alien_gun_list[track].hideturtle()
                alien_gun_list[track].goto(alien.xcor(), alien.ycor())
                alien.fire = False
                space_ship.fire = False
        # to make sure the already shot laser of a dead alien continues moving
        try:
            dead_gun[track].forward(10)
            if dead_gun[track].ycor < -280:
                dead_gun[track].hideturtle()
                dead_gun[track].pop(track)
        except IndexError:
            pass
        except TypeError:
            pass


        track += 1

    return edge,hit


class Obstacle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("#67c94d")
        self.setheading(90)
        self.penup()
        self.lenght = 10
        self.shapesize(0.1, 10)
        self.speed("fastest")
        self.dist = 120
        self.rev_dist = 10


def obstacle_line(pos):
    obstacle_list = []
    width = 20
    x = pos
    y = -50
    for ver in range((width)):
        obstacle_list.append(Obstacle())
        obstacle_list[ver].goto(x, y)
        x += 5
    return obstacle_list


def arrange_obstacle():
    all_obstacle = []
    for i in range(-350, 350, 120):
        all_obstacle += obstacle_line(i)
    return all_obstacle


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.score=0
        self.goto(250,420)
        self.hideturtle()
        self.color("#67c94d")
        self.write(f"score:{self.score}",font=("Arial",24,"normal"))

    def add(self):
        self.clear()
        self.goto(250,420)
        self.write(f"score:{self.score}",font=("Arial",24,"normal"))

class Lives(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.lives=3
        self.goto(-300,420)
        self.hideturtle()
        self.color("#67c94d")
        self.write(f"lives:{self.lives}",font=("Arial",24,"normal"))

    def reduce_lives(self):
        self.clear()
        self.lives -= 1
        self.write(f"lives:{self.lives}",font=("Arial",24,"normal"))
    def update_(self):
        self.clear()
        self.write(f"lives:{self.lives}",font=("Arial",24,"normal"))


