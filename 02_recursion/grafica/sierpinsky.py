import turtle
import math

def draw_triangle(x, y, b):
    # Base = Altura * 2
    turtle.goto(x,y)
    turtle.pd()

    # Base (hipotenusa)
    turtle.forward(b)
    turtle.left(135)
    # Cateto derecho
    turtle.forward(math.sqrt(2*pow(b/2,2)))
    turtle.left(90)
    # Cateto izquierdo
    turtle.forward(math.sqrt(2*pow(b/2,2)))
    turtle.left(135)
    
    turtle.pu()


def sierpinsky(x, y, b, n):
    # x, y: posicion absoluta
    # b: longitud de la base del triangulo
    # n: nivel del triangulo

    if (n > 0):
        # Triangulo inferior izquierdo
        sierpinsky(x, y, b/2, n-1)
        # Triangulo inferior derecho
        sierpinsky(x + b/2, y, b/2, n-1)
        # Triangulo superior
        sierpinsky(x + b/4, y + b/4, b/2, n-1)
    else:
        draw_triangle(x,y,b)


if __name__ == '__main__':
    sierpinsky(0,0,300,3)
    turtle.exitonclick()
