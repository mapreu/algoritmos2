import turtle
import math

def draw_H(x, y, h):
    # x, y: Centro de la H
    # h: altura/base
    turtle.pu()
    turtle.goto(x-h/2,y-h/2)

    # Lado izquierdo
    turtle.pd()
    turtle.left(90)
    turtle.forward(h)
    # Centro
    turtle.left(180)
    turtle.forward(h/2)
    turtle.left(90)
    turtle.forward(h)
    # Lado derecho
    turtle.left(90)
    turtle.forward(h/2)
    turtle.left(180)
    turtle.forward(h)
    turtle.left(90)
    
    turtle.pu()


def haches(x, y, h, n):
    # x, y: posicion absoluta
    # h: tamano de la hache
    # n: nivel de profundidad

    if (n > 0):
        # H central
        draw_H(x, y, h)

        # H inferior izquierda
        haches(x-h/2, y-h/2, h/2, n-1)
        # H superior izquierda
        haches(x-h/2, y+h/2, h/2, n-1)
        # H superior derecha
        haches(x+h/2, y+h/2, h/2, n-1)
        # H inferior derecha
        haches(x+h/2, y-h/2, h/2, n-1)
        
if __name__ == '__main__':
    haches(0,0,200,4)
    turtle.exitonclick()