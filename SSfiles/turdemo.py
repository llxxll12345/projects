from turtle import *

# draw a picture
title("first drawing!")

turtle = Turtle()

def change(r):
	return ((r * 10) % 10)/10
#change the color

r = 0.1
g = 0.1
b = 0.1
#initial color

sc = Screen()
sc.screensize(700,700)
sc.bgcolor("green")
sc.screensize(500.0,500.0)
turtle.pencolor(r, g, b)
leng = 10
#initialization

for i in range(144):
	print(turtle.position())
	if(turtle.position()[0] + leng > 350 or turtle.position()[0] - leng < -350) :

		turtle.pencolor(change(r),change(g),change(b))
		r += 0.1
		g += 0.1
		b += 0.1
		print(r, g, b)
		turtle.up()
		turtle.goto(0,0)
		turtle.left(60)
		leng = 10
		turtle.down()
	elif(turtle.position()[1] + leng > 350 or turtle.position()[1] - leng< -350) :
		turtle.pencolor(change(r),change(g),change(b))
		r += 0.1
		g += 0.1
		b += 0.1
		turtle.up()
		turtle.goto(0,0)
		turtle.left(60)
		leng = 10
		turtle.down()
	else:
		turtle.left(90)
		turtle.forward(leng)
		leng += 20

exitonclick()