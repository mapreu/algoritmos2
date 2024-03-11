import turtle
import math

def draw_square(x, y, b):
    # x, y: Centro del cuadrado
    # b: lado/base
    turtle.color("black","grey")
    turtle.pu()
    turtle.goto(x-b/2,y-b/2)
    turtle.pd()
    turtle.begin_fill()

    for i in range(0,4):
        turtle.forward(b)
        turtle.left(90)

    turtle.end_fill()
    turtle.pu()


def cuadrados(x, y, b, n):
    # x, y: posicion absoluta
    # b: base del cuadrado
    # n: nivel de profundidad

    if (n > 0):
        # Cuadrado inferior izquierdo
        cuadrados(x-b/2,y-b/2,b/2,n-1)
        # Cuadrado superior izquierdo
        cuadrados(x-b/2,y+b/2,b/2,n-1)
        # Cuadrado superior derecho
        cuadrados(x+b/2,y+b/2,b/2,n-1)
        # Cuadrado inferior derecho
        cuadrados(x+b/2,y-b/2,b/2,n-1)
        
        # Cuadrado del nivel
        draw_square(x, y, b)
 
 
if __name__ == '__main__':
    cuadrados(0,0,200,4)
    turtle.exitonclick()