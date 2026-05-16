from turtle import *
from colorsys import *

speed (0)
bgcolor('black')
hideturtle()
tracer (50)

pensize(1)

for i in range(360):
    color(hsv_to_rgb(i / 360, 1, 1))
    fd(i * 0.7)
    circle(i* 0.1)
    backward(i* 0.7)
    rt(7)
done()
