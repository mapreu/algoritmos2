# Formas de recursión en operaciones
En esta sección analizaremos un concepto relevante respecto a cómo se resuelve la recursión internamente cuando hablamos de operaciones.

## Recursión de pila
Recordemos la estructura de una operación recursiva que planteamos en la [introducción](./intro_recursion.md#diseño-de-una-operación-recursiva):

```
funcion resolver(problema)
    si problema es simple entonces
        devolver solucion
    sino
        dividir problema en subproblema1..N
        resolver(subproblema1)  # <- primera invocación recursiva
        resolver(subproblema2)
        ..
        resolver(subproblemaN)
        combinar_soluciones
        devolver solución
    finSi
finFuncion
```
Al momento de ejecutarse se realiza la primera invocación recursiva, toda información referida a la actual instancia de ejecución de la operación `resolver` será almacenada en la **pila de ejecución** y luego se apilará una nueva instancia en la misma pila la cual corresponderá a la ejecución recursiva recién lanzada. Por lo tanto, al llegar a esa sentencia, el programa comienza a ejecutar una nueva instancia recursiva y **suspende el resto de la ejecución de la instancia actual**, la cual será completada luego de que finalice la invocación recursiva.

Esto se ve claramente en el efecto de apilado en la pila de ejecución, ya que **las operaciones que aún tienen sentencias pendientes de ejecución estarán en bloques inferiores de la pila**. Si no apiláramos información de la instancia actual como variables locales, punteros de retorno, etc., el programa no sabría por dónde seguir o cuánto valen las variables locales previas para computar el resultado final.

> A este diseño de recursión lo llamaremos **recursión de pila**, ya que para resolver el problema recursivo **nos apoyamos en la pila de ejecución**.

Este tipo de recursión provee la ventaja de permitir soluciones recursivas en general más elegantes y es la forma más natural de soluciones recursivas, sobre todo en el paradigma funcional. Una desventaja no menor es que puede provocar la **saturación de la pila** cuando la recursión es muy profunda, ya que la pila de ejecución es finita.

> La recursión de pila sucede cuando en el caso recursivo **nos quedan operaciones pendientes por hacer luego de la invocación recursiva**.

### Ejemplo con factorial (pila)
Volviendo al ejemplo visto del [factorial](./intro_recursion.md#recursión-simple), analicemos cómo se resuelve la recursión.

```python
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    else:
        resultado_parcial = factorial(n-1)
        return resultado_parcial * n
```
Modificamos la función original para resaltar que en el caso recursivo primero se invoca `factorial(n-1)` y se lo almacena en una variable local `resultado_parcial`. Esta variable no tendrá valor asociado hasta que no finalice la invocación recursiva, por lo cual la instancia actual de factorial **se suspende y le queda pendiente realizar 2 acciones**: multiplicar el resultado de la llamada recursiva con el número n y devolverlo.

Entonces, en cada invocación de `factorial` estamos **entrando hacia lo profundo de la recursión** hasta llegar a la invocación de `factorial(1)` que corresponde al caso base. En ese momento, la pila de ejecución tiene el siguiente estado:

![pila ejecucion factorial](./imagenes/factorial_recursion_pila.png)

Las sucesivas invocaciones recursivas se manifiestan con las flechas rojas y en cada caso se apila una nueva instancia de ejecución de la función. Cuando se llega al caso base no existen otras invocaciones recursivas sino que **comienza la _vuelta hacia atrás_** de la recursión, donde cada operación termina de computar las sentencias pendientes y devolver el resultado correspondiente. Esto se visualiza con las flechas negras que **representan el retorno de cada instancia de `factorial()`**.

El primer retorno es el del caso base, donde se devuelve simplemente el literal `1` con la sentencia `return 1`. Luego, se desapila `factorial(1)` de la pila de ejecución porque finalizó su ejecución (no tiene más sentencias por ejecutar) y el programa retoma la ejecución donde quedó pendiente la instancia debajo en la pila. Entonces, se ejecuta el `return resultado_parcial * n` de la instancia `factorial(2)`, lo cual se muestra con la flecha de retorno `1 * 2 = 2`, porque en esa instancia `n = 2` y `resultado_parcial = 1`. Esto sucede para cada instancia pendiente de resolver en la pila de ejcución hasta llegar a la última (la primera, en realidad) `factorial(4)` que retorna el valor final `24`.

> Es común asociar la idea de construir la solución recursiva de _atrás hacia el principo_ cuando trabajamos con recursión de pila.

## Recursión de cola
Cuando estemos ante una **recursión simple**, es posible encontrar una forma de resolución que **no requiera apoyarse en la pila de ejecución**. Esta forma particular debe evitar realizar operaciones posteriores con el resultado parcial de la invocación recursiva. En este caso no existiría la idea de _la vuelta atrás_ para construir el resultado final, sino que **se construye a medida que se entra en la recursión y se devuelve el valor final al llegar al caso base**.

> La recursión de cola **no necesita apoyarse en la pila de ejecución** para resolver un problema, porque la solución se computa parcialmente en cada invocación desde el principio y se retorna al llegar al caso base.

### Ejemplo con factorial (cola)
Vamos a diseñar una solución distinta de la propuesta previamente. Ahora iremos generando un resultado parcial en cada instancia recursiva y lo devolveremos al llegar al caso base. Utilizaremos una variable acumuladora desde el inicio para computar este cálculo parcial. Dado que el factorial es una productoria, podemos inicializar el acumulador con un valor neutro: `1`.

```python
def factorial(n: int) -> int:
    def factorial_interna(n: int, acumulador: int) -> int:
        if n <= 1:
            return acumulador
        else:
            return factorial_interna(n-1, acumulador * n)
    return factorial_interna(n, 1)
```
El uso de una [función interna](../A_Python_POO/README.md#funciones-internas) es de gran utilidad en esta situación porque la función externa la invoca con cierta inicialización que es oculta a quien la consume, como el caso de inicializar el acumulador en `1`. Observemos que ahora la función recursiva cambió tanto su caso base, que ahora devuelve el acumulador, y en su caso recursivo, que ahora la última sentencia es la misma invocación recursiva `factorial_interna`. Otro cambio es que la construcción de la solución se produce previo a la invocación y se pasa como segundo argumento de la operación. Podríamos haber descompuesto el retorno del caso recursivo de esta forma para clarificarlo:

```python
resultado_parcial = acumulador * n
return factorial_interna(n-1, resultado_parcial)
```
Así queda bien resaltado que la última operación del caso recursivo es justamente la invocación recursiva `factorial_interna(n-1, resultado_parcial)`, **no queda nada pendiente por computar** sino sólo devolver el resultado. Cada invocación sucesiva a instancias de problemas más pequeños `(n - 1)` computa **un resultado parcial que se acerca cada vez más a la solución final**.

> En la recursión de cola **la última sentencia** del caso recursivo **es la invocación recursiva**.

### Recursión de cola -> Iteración
Probablemente lo más ventajoso de definir una operación con **recursión de cola** es que podemos escribirla como una simple **iteración**, y así nunca utilizaremos la pila de ejecución para sucesivas invocaciones recursivas. En algunos lenguajes existe un término denominado **optimización de invocación de cola** (_tail call optimization_) donde el lenguaje puede detectar una operación con recursión de cola y así **transformarla automáticamente en una iteración**, eliminando por debajo la recursión. 

> Python no tiene _tail call optimization_ , por lo que es necesario hacer la conversión de la operación a una iteración manualmente para **evitar el desborde de la pila**.

Así como planteamos un [diseño genérico](./intro_recursion.md#diseño-de-una-operación-recursiva) de una solución recursiva de pila, podemos intentar un diseño genérico para la recursión de cola.

```
funcion resolver(problema)
    si problema es simple entonces
        devolver solución_final
    sino
        reducir tamaño del problema
        computar solución parcial
        devolver resolver(subproblema)
    finSi
finFuncion
```
Resaltamos que la última operación del caso recursivo es la invocación a sí misma de `resolver()`. A partir de esta generalización podríamos proponer como se transformaría en una solución iterativa:
```
funcion resolver(problema)
    mientras problema no es simple
        computar_solución_parcial
        problema <- reducir el tamaño del problema
    finMientras
    devolver solución_final
finFuncion
```
La transformación, en términos genéricos, de una recursión de cola en una iteración se logra realizando lo siguiente:
- Se cambia el `if` por un bucle `while`
- La condición del `if` (caso base) negada pasa a ser la condición del `while`
- El caso recursivo pasa a ser el cuerpo del `while`
- El retorno del caso base es el retorno final de la solución iterativa

> La recursión de cola **siempre puede reemplazarse por una iteración**, por eso se la conoce también como **falsa recursión**.

Veamos cómo quedaría la versión iterativa del factorial.

```python
def factorial(n: int) -> int:
    solucion = 1
    while n > 1:
        solucion *= n
        n -= 1
    return solucion
```
Si contemplamos las indicaciones previas, estamos negando el caso base `n <= 1` que pasa a ser `n > 1` como condición del `while`, y resumimos el cómputo del caso recursivo como `solucion *= n` y luego el decremento del problema `n -= 1`.

## Eliminando la recursión
Cuando hablamos de _eliminar la recursión_ nos referimos a **evitar la recursión de pila**, **convirtiendo la solución a una recursión de cola** o una iteración. Vamos a ver dos estrategias que podemos aplicar en ciertas situaciones para convertir una recursión de pila en una recursión de cola y, por ende, en una iteración eventualmente.

### Acumulando solución parcial
El caso del [factorial](#ejemplo-con-factorial-cola) que se resuelve con recursión de cola se apoya en un acumulador (`acumulador`) sobre el que se almacenan las sucesivas multiplicaciones. El resultado final se guarda ahí hasta llegar al caso base donde se retorna.

Esta estrategia sigue el concepto mencionado de la **recursión de cola** que plantea una **construcción de la solución desde la primera invocación**. Esto difiere de la forma natural recursiva para construir soluciones, como lo es cuando utilizamos **recursión de pila**, donde **la construcción de la solución comienza desde el caso base**. Esta diferencia es muy importante ya que puede producir resultados distintos si no se contempla la **conmutatividad y asociatividad** de los cómputos parciales para combinar la solución final.

Veamos cómo se calcula realmente el factorial con ambas formas de recursión vistas.

- **Cálculo del resultado con recursión de pila**
```
factorial(4) = factorial(3) * 4
             = (factorial(2) * 3) * 4
             = ((factorial(1) * 2) * 3) * 4
             = ((1 * 2) * 3) * 4 = 24
```

- **Cálculo del resultado con recursión de cola**
```
factorial(4) = 4 * factorial(3)
             = (4 * 3) * factorial(2)
             = ((4 * 3) * 2) * factorial(1)
             = ((4 * 3) * 2) * 1 = 24
```

La construcción del valor cuando utilizamos la versión con recursión de pila es distinta a la solución con la recursión de cola. Afortunadamente, el resultado final es el mismo en este caso, porque **el producto es una operación asociativa y conmutativa**. Entonces siempre debemos contemplar el orden y cómo se combinan las soluciones cuando utilizamos la **estrategia del acumulador**.

> No siempre podremos eliminar la recursión con la estrategia de acumulación, debemos prestar atención en cómo se construyen las soluciones.

Veamos un ejemplo donde no podemos utilizar esta estrategia:

```python
def resta_lista(xs: list[int]) -> int:
    if xs == []:
        return 0
    else:
        return xs[0] - resta_lista(xs[1:])

resta_lista([10, 2, 5, 9])   # (10 - (2 - (5 - 9))
```
La función recursiva `resta_lista` se apoya en la pila de ejecución porque quedan operaciones pendientes por realizar luego de la invocación recursiva. El resultado generado es: `(10 - (2 - (5 - 9)) = 4`.

```python
def resta_lista(xs: list[int]) -> int:
    def resta_lista_interna(xs: list[int], acumulador: int) -> int:
        if xs == []:
            return acumulador
        else:
            return resta_lista_interna(xs[1:], acumulador - xs[0])
    return 0 if xs == [] else resta_lista_interna(xs[1:], xs[0])

resta_lista([10, 2, 5, 9]) # ((10 - 2) - 5) - 9)
```
Esta versión que utiliza recursión de cola intenta replicar la misma operación de restar elementos de la lista, pero produce un resultado diferente `((10 - 2) - 5) - 9) = -6`. El problema de esta conversión inválida es que no podemos computar previamente la resta de los elementos finales como el caso de la anterior. Por lo tanto no podemos convertir la función original con esta estrategia.

### Utilizando pila explícita
Cuando no podemos eliminar la recursión de pila utilizando un acumulador podemos optar por esta estrategia. La idea es simple, **gestionaremos nuestra propia pila de ejecución** en un objeto de tipo `Pila` o `Stack`. Entonces simularemos manualmente el apilado y desapilado de invocaciones recursivas con la información necesaria para construir la solución en el mismo orden y con la misma asociación de soluciones parciales. Así podremos eliminar la recursión de pila para convertir la solución en una recursión de cola o en una simple iteración.

Veamos una forma de resolver la función previa con una pila explícita:

```python
def resta_lista(xs: list[int]) -> int:
    def apilado(xs: list[int], pila: list[int]):
        if xs != []:
            pila.append(xs[0])
            apilado(xs[1:], pila)

    def desapilado(pila: list[int], acumulador: int) -> int:
        if pila == []:
            return acumulador
        else:
            return desapilado(pila, pila.pop() - acumulador)
      
    pila = []
    apilado(xs, pila)
    return desapilado(pila, 0)

resta_lista([10, 2, 5, 9]) # (10 - (2 - (5 - 9))
```
Si bien cada caso será diferente, en general este tipo de conversión se realiza con dos pasos, uno donde se apilan las instancias de problemas reducidos (similar a como se hace naturalmente con la pila de ejecución) y otro que representa la _vuelta atrás_ de la recursión. El primer paso se manifiesta con la función `apilado()` que recibe una lista vacía y la carga con cada elemento de la lista. El segundo paso se logra con `desapilado()` donde se recibe una lista cargada y se comienza a desapilar y realizando los _cálculos pendientes_ que se harían en la _vuelta atrás_ de la recursión de pila. Notemos que ambas funciones internas son ahora una recursión de cola, por lo cual logramos eliminar la recursión de pila.

### Ejercicio: resta_lista iterativa
Convertir la última función `resta_lista` que utiliza una pila explícita de forma que no use ningún tipo de recursión y sólo utilice iteración.

### Ejercicio: Suma-Resta alternada
Implementar una versión con recursión de cola que produzca el resultado esperado al pasar una lista: `suma_resta_alternada([1, 2, 3, 4, 5]) = 1 + 2 - 3 + 4 - 5
