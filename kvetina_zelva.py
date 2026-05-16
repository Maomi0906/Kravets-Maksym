from turtle import *
import colorsys

speed(0)
pensize(2)
h = 0.18
bgcolor("black")

for i in range(200):
    c = colorsys.hsv_to_rgb(h,1,1)
    # Ограничиваем значения RGB в диапазоне [0.0, 1.0], чтобы избежать ошибки.
    c = (max(0.0, min(1.0, c[0])), 
         max(0.0, min(1.0, c[1])), 
         max(0.0, min(1.0, c[2])))
    color(c)
    h -= 0.0012
    circle(200-i, 100)
    lt(100)
    circle(200-i, 100)
    rt(100)

    for j in range(3):
        rt(20)

done()
