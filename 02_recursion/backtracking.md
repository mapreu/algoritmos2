# Backtracking
En el ámbito de la ciencia de la computación existen una amplia variedad de problemas donde es necesario **explorar exhaustivamente un conjunto finito de posibles soluciones** para encontrar aquellas que cumplan con ciertas condiciones o restricciones.

## Características de los problemas

Los problemas mencionados comparten las siguientes características.

- **Espacio de soluciones finito**: Los problemas tienen un espacio de soluciones finito y bien definido. Esto implica que podríamos enumerar todas las posibles soluciones de manera sistemática y exhaustiva.

- **Restricciones o condiciones explícitas**: Los problemas deben tener restricciones claras y bien definidas que las soluciones deben cumplir. Estas restricciones pueden estar relacionadas con la validez de la solución, limitaciones de tiempo o recursos, o cualquier otro criterio específico del problema.

- **Solución satisfactoria**: En algunos casos, se busca encontrar **la solución óptima** que satisfaga ciertos criterios predefinidos. En otros casos, el objetivo puede ser simplemente encontrar **cualquier solución válida**. Es importante tener en cuenta cuál es el objetivo final del problema para determinar si se busca una solución óptima o simplemente identificar todas las válidas.

## Resolución por fuerza bruta

Una estrategia posible para resolver este tipo de problemas es utilizar la _fuerza bruta_ para encontrar las soluciones satisfactorias. Esta búsqueda dentro de un espacio de soluciones **reducido** puede resultar válida y aceptable. En ese caso, podemos **generar todas las soluciones posibles** (el espacio de soluciones completo) y seleccionar aquellas que resultan ser soluciones válidas u óptimas.

La dificultad de esta estrategia surge cuando el espacio de soluciones posibles empieza a ser muy grande. Esto es común cuando hablamos de **problemas de explosión combinatoria**, donde es muy probable que sea muy costoso (o directamente inviable) generar el conjunto completo de soluciones para probar cada una de ellas.

## El concepto de backtracking

Cuando vemos que la estrategia previa no es viable, podemos aplicar la idea de backtracking. Es una **técnica de resolución de problemas** que se basa en la **exploración sistemática de todas las posibles soluciones** para encontrar **aquellas que cumplen con ciertas restricciones o condiciones**. Es especialmente útil cuando se enfrentan problemas combinatorios o de búsqueda, donde se debe probar una serie de opciones para encontrar la solución óptima o satisfactoria. En general resulta práctico para algunos problemas donde la **solución no es determinística**, es decir, no existe un curso de acción que nos permita llegar siempre a la solución.

> Backtracking es una estrategia de resolución no determinística de problemas

Si bien puede parecer una estrategia similar a la de _fuerza bruta_, la ventaja en eficiencia de esta técnica se apoya en que puede **descartar previamente soluciones parciales que sabemos que no construirán una solución óptima o válida**. Este descarte permite reducir notablemente el conjunto completo de soluciones posibles sobre el cual buscaremos.

Al aplicar backtracking con operaciones recursivas, en cada llamada recursiva **exploramos una rama del árbol de posibles soluciones** y, si llegamos a un punto en el que **no se satisfacen ciertas condiciones**, **retrocedemos** (_backtrack_) y **probamos otra opción**. Básicamente, estaremos resolviendo el problema mediante la **prueba y error**.

## El diseño con backtracking
Si bien cada problema tendrá una resolución diferente, podemos generalizar algunas pautas para tener presente durante el proceso de diseño para soluciones con esta técnica.

1. **El problema**: El primer paso al diseñar cualquier algoritmo es identificar correctamente el problema a resolver y analizar si cumple las [características mencionadas](#características-de-los-problemas).

2. **Solución parcial y la solución final**: Debemos definir la generación de **soluciones parciales** que iremos construyendo paso a paso hasta llegar a una **solución válida**. También es importante identificar cuándo hemos alcanzado una **solución final** que cumple con todas las condiciones del problema.

3. **Exploración exhaustiva**: Probamos todas las opciones posibles para construir la solución mediante llamadas recursivas que nos permiten **explorar diferentes ramas del árbol de soluciones**. Cada rama del árbol representa una solución posible que se construye mientras cumpla las restricciones o condiciones necesarias.

4. **Rechazo y retroceso**: Si llegamos a un punto donde no podemos seguir avanzando sin violar alguna restricción, **se descarta esa solución parcial y debemos retroceder** (_backtrack_) para probar una opción diferente. Esto implica deshacer los cambios realizados en la solución parcial y volver a un estado anterior para explorar otra rama.

## Recorriendo un laberinto
Analicemos en cómo podríamos plantear una estrategia para recorrer y salir exitosamente de un laberinto. Asumimos que este laberinto tiene una única entrada y una única salida para facilitar el problema. Una idea muy simple, pero a la vez poderosa puede ser la siguiente:

1. Avanzar en una dirección determinada (norte, sur, este, oeste).
2. En cada bifurcación, recorrer todos los caminos posibles.
3. Si llegué a un final sin salida o un lugar ya visitado, vuelvo hacia atrás a probar otro camino.

En este problema claramente no conocemos un curso de acción determinado para resolverlo, debemos probar opciones para encontrar una solución válida (salir del laberinto). Podemos pensar como solución parcial a **cada recorrido desde el inicio hasta cierta posición** dentro del laberinto. El conjunto de todos estos recorridos conforma el **espacio finito de soluciones posibles del problema**.

Veamos una representación sencilla del problema.

![laberinto](./imagenes/representacion_laberinto.png)

Entonces, cada posición dentro del laberinto puede ser **una bifurcación si permite avanzar en más de una dirección**.

### El árbol de soluciones
En el paso 2 mencionado debemos establecer una estrategia para construir las soluciones parciales, es decir, cómo recorreremos todos los caminos posibles en cada bifurcación. Una forma sería elegir una opción de manera aleatoria, otra más simple sería determinar el orden con el cual elegimos avanzar. Optando por la segunda estrategia, vamos a establecer el orden de búsqueda así:

1. Ir al este (hacia la derecha en la imagen)
2. Ir al oeste (hacia la izquierda en la imagen)
3. Ir al sur (hacia abajo en la imagen)
4. Ir al norte (hacia arriba en la imagen)

Quien ingrese al laberinto deberá probar en cada posición diferentes caminos en el orden de búsqueda que planteamos en la estrategia. Una forma de representar **todas estas opciones que probará** es mediante un **árbol de soluciones** donde cada nodo representa la posición en el laberinto y cada rama un recorrido posible. Veamos cómo quedaría el árbol mencionado.

![arbol soluciones laberinto](./imagenes/laberinto_arbol_soluciones.png)

Partiendo desde la posición 1, primero decidimos avanzar a la posición 2 porque nuestro orden de búsqueda primero es ir a la derecha, dejando pendiente la posición 5 para una eventual exploración posterior. En sucesivas posiciones, realizamos la misma decisión hasta llegar a una posición sin salida (posición 8). Aquí debemos regresar nuestros pasos (backtrack) hasta donde teníamos más opciones disponibles, lo que nos lleva a la posición 3 para continuar explorando. Si bien el segundo paso del orden de búsqueda indica ir a la izquierda, elegimos avanzar hacia abajo a la posición 7 porque estamos probando todas las posibilidades a partir de la posición 3 y no queremos regresar aún a la posición 2 para probar otras. Este juego de prueba y error es lo que termina generando el árbol. Siguiendo la analogía con la recursión, veremos que **las hojas de este árbol son los casos base**.

### Implementando la solución

Un estilo de implementación de este tipo de soluciones requiere mantener presente en cada instancia de recursión **una copia de la solución parcial** para construir a partir de esta las siguientes posibles soluciones. Es importante la idea de la copia parcial, que sería el **camino recorrido hasta el momento**, porque al probar diferentes opciones recursivas es necesario evitar que dichas pruebas alteren esta solución parcial de la que partimos. De lo contrario, el concepto de _vuelta atrás_ no sería posible. En el caso del laberinto, sería similar a marcar el camino recorrido de forma que otro pueda seguirlo.

Siguiendo la imagen del árbol previa, imaginemos que comenzamos caminando las posiciones 1, 2 y 3. Al llegar a la posición 3, tenemos la posibilidad de ir a la posición 4 o 7. Cuando avanzamos a la posición 4, debemos _recordar_ que en la posición 3 aún nos queda pendiente visitar la posición 7. Entonces, cuando regresamos a la posición 3 porque el camino que llevaba por la 4 no tenía salida, debemos continuar pero contemplando que el camino parcial es 1-2-3. Esa es la **copia de solución parcial** a la que hacemos referencia, porque al visitar la posición 7 la solución parcial se compone de la previa agregando el 7, dando el camino 1-2-3-7.

Veamos una idea para implementar un algoritmo que encuentre un camino que lleve a la salida, una solución válida.

```python
def recorrer(camino_previo: list[Posicion]) -> (bool, list[Posicion]):
    posicion_actual = camino_previo[-1]
    if es_salida(posicion_actual):
        return True, camino_previo
    else:
        salida_encontrada = False
        direcciones = ['N', 'S', 'O', 'E']
        while direcciones and not salida_encontrada:
            nueva_posicion = avanzar(posicion_actual, direcciones.pop())
            if hay_paso(nueva_posicion) and nueva_posicion not in camino_previo:
                camino_actual = camino_previo.copy()
                camino_actual.append(nueva_posicion)
                salida_encontrada, solucion = recorrer(camino_actual)
            
        return salida_encontrada, solucion
```

La precondición de esta función es que recibe como `camino_previo` una lista sólo con la posición inicial del laberinto (la entrada). La `posicion_actual` se determina con el último elemento de ese parámetro, ya que nos indica el camino realizado desde la entrada hasta la situación actual. Hay algunas operaciones que abstraemos para facilitar la lectura del código:
- `es_salida()`: devuelve verdadero si la posición es una salida del laberinto.
- `avanzar()`: dada una posición en el laberinto y una dirección, devuelve la nueva posición que surge de ir en esa dirección desde la posición original.
- `hay_paso()`: valida si la posición actual es válida para avanzar (si no tiene un muro que lo impida).

El **caso base** es claro, si estamos parados en la salida hemos encontrado una **solución válida** y la retornamos. El detalle del retorno es que también anunciamos que encontramos la salida con un `bool`, de forma que retornamos una tupla donde el primer elemento es el indicador que encontramos una solución válida y el segundo elemento es justamente la solución (el camino recorrido).

El caso recursivo realiza lo siguiente:
1. Asume que aún no encontramos la salida.
2. Planteamos la estrategia de búsqueda con las 4 direcciones posibles.
3. Para cada dirección probamos avanzar si tenemos paso por esa dirección y validando que no estemos regresando por donde vinimos:
    - si no podemos avanzar, se descarta esa dirección.
    - si avanzamos copiamos el `camino_previo` como `camino_actual`, le agregamos la posición actual al final y continuamos el recorrido utilizando `camino_actual`.

Es importante notar que en el caso recursivo recibimos el retorno del recorrido futuro porque necesitamos saber si por allí se encontró una salida. Esta información llega como el primer elemento de la tupla retornada. Es por eso que se utiliza como condición de corte del `while` la variable `salida_encontrada` que se inicializa en `False` para cada instancia recursiva.

Si bien con este algoritmo podemos encontrar la primera solución válida, también podríamos pensar otro para que nos genere todos los recorridos posibles con salida, es decir, todas las soluciones válidas (si existen más de una). La estrategia para resolverlo sería la misma, intentando diferentes direcciones en cada posición mientras construimos caminos parciales que iremos descartando si no llevan a ningún lado. Y al llegar a la salida guardaríamos ese camino encontrado y volveríamos a probar otros que hayan quedado pendiente para ver si llegamos a salir utilizando otro recorrido.

### Ejercicio: Permutaciones
Definir la función permutaciones, que dada una lista de enteros, retorne una lista de listas de enteros, donde cada lista es cada una de las posibles permutaciones de la lista original.

Por ejemplo: `permutaciones([6,2,3]) = [[6,2,3], [6,3,2], [2,3,6], [2,6,3], [3,2,6], [3,6,2]]`

### Ejercicio: Hagamos un laberinto
Pensando una representación simplificada de un laberinto, les propongo definir una estructura que permita modelar un laberinto cuadrado. La construcción del laberinto podría pensarse así:
1. Generar un cuadrado con todas las posiciones (por ejemplo, 5x5 o 10x10, etc) donde cada posición sea un muro. Inicialmente, el laberinto no tiene recorrido alguno.
2. Definir como entrada la posición de arriba a la izquierda y la salida sería abajo a la derecha.
3. Construir al menos un camino utilizando el concepto de backtracking donde comenzamos desde la entrada e iremos _tirando muros_ en un recorrido aleatorio hasta llegar a la salida. Imaginemos este proceso como el de una lombriz que va generando surcos en la tierra.

Finalmente, implementar una operación que permita encontrar todos los caminos posibles desde la entrada hasta la salida del laberinto.
