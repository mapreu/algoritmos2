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


def calcular_posicion( coords, b, izq):
    # Para calcular la posicion del triangulo desde uno superior
    # coords: coordenadas (x,y) del triangulo superior
    # b: base del triangulo
    # izq: define si queremos las coordenadas del triangulo que "cuelgue" de la izquierda o derecha
    if izq:
        return (coords[0] - b/2, coords[1] -b/2)
    else:
        return (coords[0] + b/2, coords[1] -b/2)

def sierpinsky_iter(x, y, b, n):
    # x, y: posicion absoluta
    # b: longitud de la base del triangulo
    # n: nivel del triangulo

    # Triangulo inicial
    triangulos = [ (x,y) ]
    
    # Dibujamos cada nivel
    for i in range(0, 2**n):
        triangulos_siguientes = []
        # Dibujamos los triangulos del nivel y calculamos los siguientes
        for n, posicion in enumerate(triangulos):
            draw_triangle(posicion[0], posicion[1], b)
            # Si los triangulos dibujados se tocan, no "cuelgan" triangulos debajo de ese vertice
            if not ( n > 0 and posicion[0] == (triangulos[n - 1][0] + b) ):
                triangulos_siguientes.append(calcular_posicion(posicion, b, True))
            if not ( (n + 1) < len(triangulos) and (posicion[0] + b) == triangulos[n + 1][0] ):
                triangulos_siguientes.append(calcular_posicion(posicion, b, False))
        triangulos = triangulos_siguientes


if __name__ == '__main__':
    sierpinsky_iter(0,0,30,4)
    turtle.exitonclick()