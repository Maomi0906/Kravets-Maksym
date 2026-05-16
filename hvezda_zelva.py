import turtle
count = 1
t = turtle.Turtle()
turtle.bgcolor("black")
t.speed(0)
while count < 300:
    t.forward(count)
    t.color("yellow")
    t.left(143)
    t.left(1)
    count += 1
    t.forward(count)
    t.color("greenyellow")
    t.right(350)
    t.radians()
    t.color("orange")
    t.right(30)
    t.hideturtle()
turtle.done()
