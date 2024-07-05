# Type Hints en Python
En esta sección exploraremos una opción interesante para mejorar la legibilidad, mantenimiento y seguridad de nuestro código Python. Se trata de una especie de extensión al lenguaje que nos permitirá trabajar con Python como si fuese un **lenguaje tipado**, es decir, incorporar un **sistema de tipos estático**.

## Introducción
Los _type hints_ o **anotaciones de tipos** en Python son una característica introducida en Python 3.5 a través de la [PEP 484]((https://peps.python.org/pep-0484/)). Estas anotaciones de tipo **opcionales** que se pueden añadir a las variables, parámetros de funciones y valores de retorno para indicar el tipo de datos que se espera en una determinada posición en el código. Aunque **Python sigue siendo un lenguaje de tipado dinámico**, los type hints pueden ser **útiles para documentar el código, mejorar la legibilidad y facilitar el análisis estático del código** por parte de herramientas externas.

Veamos por qué decimos que Python es un lenguaje de **tipado dinámico**.
```python
variable = 45   # variable apunta a tipo int
variable = 4.3  # variable apunta a tipo float
variable = 'a'  # variable apunta a tipo str
variable = [1]  # variable apunta a tipo list
```
Si invocáramos `type(variable)` luego de cada asignación veríamos los distintos tipos de datos comentados. Esto nos indica que el tipo de dato referido en `variable` es dinámico, ya que en realidad el tipo de dato está asociado a la instancia (objeto) y no al identificador (variable). Python puede entonces inferir el tipo de `variable` a través de consultar el tipo asociado al objeto que apunta en ese momento.

> Esta flexibilidad que provee un sistema de tipos dinámico requiere un mayor cuidado al momento de implementar nuestro código y su eventual mantenimiento, porque nos puede llevar a introducir defectos más fácilmente.

## Beneficios de usar Type Hints
- **Documentación del código**: Los type hints proporcionan información adicional sobre los tipos de datos que se esperan en una función o método, lo que puede ayudar a entender rápidamente cómo debe usarse esa operación. Manifiestan explícitamente la firma.
- **Mejora la legibilidad**: Al agregar type hints, se hace más evidente el propósito y la función de las variables, parámetros y valores de retorno en el código.
- **Facilita la detección de errores**: Los type hints pueden ayudar a detectar errores de tipo en **tiempo de desarrollo**, incluso antes de ejecutar el código, lo que puede ahorrar tiempo y esfuerzo en la depuración. Recordemos que Python es un lenguaje interpretado, por lo cual carece de una etapa de compilación donde se podrían verificar estas condiciones. Para lograrlo, se utilizan herramientas externas como [_linters_](https://code.visualstudio.com/docs/python/linting) que analizan el código a medida que lo escribimos.
- **Ayuda en la refactorización**: Al tener información sobre los tipos de datos utilizados en el código, es más fácil realizar cambios y refactorizaciones sin introducir errores inadvertidos.

### ¿Cuándo es bueno evitarlos?
Si bien el uso de type hints es muy importante para una gran mayoría de casos, contemplando que no incorporan beneficios de rendimiento (como sí lo hacen los sistemas de tipado estático reales gracias a una fase de compilación) y agregan un esfuerzo adicional en la escritura de código, podemos mencionar casos dodne es mejor evitar su uso:
- **Proyectos pequeños**: Si estamos implementando algo reducido, en forma de scripts o de pocas líneas, probablemente sea un esfuerzo adicional innecesario incorporar hints.
- **Funcionalidad básica**: Si vemos que el código se explica por sí mismo sin la necesidad de usar hints, podríamos evitarlos. Es común para casos donde la funcionalidad implementada sea sencilla de entender.
- **Aprendizaje**: Si estamos aprendiendo el lenguaje de cero, sería mejor dejar los hints para más adelante para evitar confundirnos.
- **Compatibilidad**: Si necesitamos implementar código compatible con versiones legacy de Python, seguramente no podamos usarlos o su implementación sea más confusa.

## Sintaxis básica de Type Hints
La sintaxis básica de type hints implica añadir anotaciones de tipo utilizando dos puntos (`:`) después del nombre de la variable o parámetro, seguido del tipo de dato esperado. En el caso de anotar un tipo de dato de retorno, se utiliza `->` al final de la firma de la operación.

```python
def potencia(base: float, exponente: int) -> float:
    return base ** exponente

potencia(10, 2)     # 100
```
En este ejemplo, indicamos que la función espera dos parámetros, el primero de tipo `float` y el segundo de tipo `int` y devuelve un valor de tipo `float`. Notemos que aún si invocamos la operación con tipos incompatibles con los declarados en la firma, por ejemplo con `potencia(10, 2.4)`, Python aún permite la evaluación de la función.

> El uso de type hints **no altera la ejecución del código**, sino que sirve para analizar con herramientas externas y entornos de desarrollo en etapas previas (_type checkers_).

Volviendo al ejemplo inicial, ahora con las anotaciones de tipo podemos agregar cierta seguridad en la asignación.

```python
var: int = 45   # ok
var = 4.3  # Expression of type "float" cannot be assigned to declared type "int"
var = 'a'  # Expression of type "str" cannot be assigned to declared type "int"
var = [1]  # Expression of type "list[int]" cannot be assigned to declared type "int"
__annotations__     # {'var': int}
```
Habiendo definido a `var` como `int`, nuestro _type checker_ nos notificará del error de intentar asignarle otro tipo de dato. La información referida a type hints se resguarda en el diccionario `__annotations__`.

## Comprobando el código
Existen herramientas externas como [`mypy`](https://pypi.org/project/mypy/) que pueden realizar **verificaciones estáticas de tipos** en el código Python basadas en los type hints añadidos.

Podemos instalar `mypy` con `pip`.

```bash
pip install mypy
```

Veamos cómo podemos ejecutar `mypy` para realizar una comprobación estática de tipos:

```bash
mypy mi_aplicacion.py
```
El binario `mypy` analizará el código en el archivo `mi_aplicacion.py` en busca de errores de tipo y nos proporcionará información sobre cualquier discrepancia encontrada entre las anotaciones de tipo y el código implementado.

## Colecciones
De la misma forma que podemos utilizar type hints para tipos de datos primitivos, también podemos utilizarlos para declarar tipos de datos de colecciones de objetos. Veamos cómo lo haríamos con los aquellos que vienen incorporados en Python.

### Listas
En general las listas están compuestas por elementos de un mismo tipo de dato, por lo tanto su definición es simple.

```python
xs: list[int] = [1, 3, 4]
ys: list[str] = ['a', 'b', 'c']
```

### Conjuntos
Los conjuntos son similares a las listas, sólo que no son una colección desordenada y de elementos sin duplicar. Podemos declararlos indicando el tipo de dato de sus elementos.

```python
s1: set[int] = {1, 2, 4}
s2: set[str] = {'a', 'b', 'c'}
s3: set[list[int]] = {[1,2], [3,5]}     # TypeError: unhashable type: 'list'
s3: set[tuple[int]] = {(1,2), (3,5)}    # ok
```
Recordemos que un `set` requiere que sus elementos sean _hasheables_ para poder determinar su identidad, por lo cual el tipo debe implementar el método `__hash__()`. El tipo `list` no lo tiene implementado y por lo tanto no puede ser utilizado en un `set`, pero sí `tuple` que es inmutable.

### Diccionarios
Los diccionarios pueden definirse con dos tipos de datos, el primero corresponde al tipo de dato de las claves y el segundo al tipo de dato de los valores.

```python
d1: dict[str, float] = {'a': 2.1, 'b': 3.4}
d2: dict[int, list[str]] = {1: ['a','b'], 2: ['c','d']}
d3: dict[list[int], int] = {[1,2]: 0, [3,5]: 1}     # TypeError: unhashable type: 'list'
d3: dict[tuple[int, ...], int] = {(1,2): 0, (3,5): 1}   # ok
```
Similar al caso previo, los tipos `dict` necesitan valores _hasheables_ como claves, ya que lo utilizan para determinar la ubicación indexada de un elemento. Por lo tanto, no podemos utilizar `list` como clave, pero sí `tuple` que es inmutable.

## Tipos de construcción
Python ofrece un conjunto de tipos predefinidos que nos facilitan la creación de nuevos tipos para anotar nuestro código. Veamos algunos relevantes.

### [`Any`](https://docs.python.org/3.12/library/typing.html#the-any-type)
Todo tipo de dato es compatible con el tipo `Any` y viceversa, por lo cual podemos realizar cualquier operación sobre una variable con este tipo anotado y asignarlo a otra variable de cualquier tipo (no se realiza verificación de tipo en ese caso).

```python
from typing import Any

variable_any: Any = None    # ok
variable_any = 4            # ok
variable_any = (1, 3,)      # ok
variable_any = [1, 2, 3]    # ok
len(variable_any)           # ok

variable_int: int = 9
variable_int = variable_any # ok, no se verifica asignación de Any

def operacion(parametro_any: Any) -> str:
    return parametro_any.metodo1()      # ok, no verifica si existe método1
```
Podemos ver que el uso de `Any` es sencillamente la forma implícita de **tipado dinámico** que hace por defecto Python. Es una anotación útil para indicar que un valor es de tipo dinámico, por lo cual se suele usar para definir un **sistema de tipado híbrido** en nuestro código.

### [`Union[t1, t2, ...]`](https://docs.python.org/3.12/library/typing.html#typing.Union)
El tipo `Union` permite identificar tipos de datos que son **subtipos de al menos uno de los tipos** incluidos en la unión.

Supongamos que deseamos definir una función que acepte un número o una cadena. La solución para declararlo sería así:

```python
from typing import Union
def mi_funcion(x: Union[float, str]):
    pass

mi_funcion(4)           # ok
mi_funcion(3.6)         # ok
mi_funcion('prueba')    # ok
```
El parámetro `x` puede tener asociada una referencia de objeto de tipo `float` o de tipo `str`, por lo cual `Union` nos provee mayor flexibilidad al definir anotaciones de tipo sin perder la validación de tipos.

A partir de la especificación [PEP 604](https://peps.python.org/pep-0604/) podemos utilizar [expresiones de uniones de tipo](https://docs.python.org/3.12/library/stdtypes.html#types-union) que resultan más amigables de escribir utilizando el operador lógico _or_: `|`.

```python
def potencia(base: int | float, exponente: int | float) -> int | float:
    return base ** exponente
```
Esta implementación permite recibir como argumentos tanto `int` como `float`, y de la misma forma devolver un `int` o un `float`.

### [`Optional`](https://docs.python.org/3.12/library/typing.html#typing.Optional)
El tipo `Optional[X]` es análogo a `X | None` o `Union[X, None]`. En el paradigma funcional se lo suele relacionar con la mónada `Maybe` donde **se representa la posibilidad de tener un valor o no**. En la programación imperativa clásica podemos encontrar una relación con el tipo de dato **puntero**, el cual puede apuntar a una ubicación en memoria o a `null`.

```python
from typing import Optional

def division(x: int, y: int) -> Optional[float]:
    if y == 0:
        return None
    return x / y

division(9, 4)      # 2.25
division(10, 0)     # None
```

### [`Callable`](https://docs.python.org/3.12/library/typing.html#annotating-callables)
Las **funciones** y el resto de **objetos invocables**, aquellos que implementan el método especial `__call__()`, pueden anotarse utilizando `collections.abc.Callable`. La sintaxis para utilzarlo es la siguiente:

`Callable[[tipo_param_1, tipo_param_2, tipo_param_3], tipo_retorno]`

Los tipos de datos de los parámetros que recibe un `Callable` se declaran como una lista de tipos que se sitúa como primer elemento, el segundo elemento es el tipo de dato de retorno. Veamos algunos ejemplos.

```python
from collections.abc import Callable

def procedimiento() -> None:
    pass

def mi_funcion(x: int) -> int:
    pass

def funcion_superior(f: Callable[[int], int]):
    return f

funcion_superior(mi_funcion)    # ok
funcion_superior(procedimiento) # Argument of type "() -> None" cannot be assigned to parameter
```
La función `mi_funcion` puede ser asignada como parámetro de `funcion_superior` porque respeta la firma declarada en `Callable`, la cual solicita un objeto invocable que acepte un argumento `int` y devuelva otro `int`.

Si deseamos declarar un invocable con una cantidad arbitraria de argumentos, podemos utilizar la notación `...`.

```python
from collections.abc import Callable

def concatenar_listas(*args: list) -> list:
    ys: list = []
    for xs in args:
        ys += xs
    return ys

def tratar_listas(*args: list, func: Callable[..., list]) -> list:
    return func(*args)

tratar_listas([1,2], [3,4], [5,6], func=concatenar_listas)  # [1, 2, 3, 4, 5, 6]
tratar_listas([], func=concatenar_listas)   # []
```
En este ejemplo utilizamos la anotación `Callable[..., list]` para identificar el parámetro `func` que recibe como argumento un invocable con una cantidad arbitraria de argumentos. Si bien funciona, debemos aclarar que esta notación no es muy segura ya que acepta cualquier lista de argumentos de cualquier tipo.

> Una forma de mejorar la declaración de invocables con firmas más complejas es apoyarse en [`Protocol`](https://docs.python.org/3.12/library/typing.html#typing.Protocol) y [`ParamSpec`](https://docs.python.org/3.12/library/typing.html#typing.ParamSpec).

En la especificación [PEP 677](https://peps.python.org/pep-0677/) se introduce una notación más sencilla para declarar invocables utilizando un estilo similar a la firma de las operaciones.

```python
x: Callable[[list[int]], float]
x: (list[int]) -> float
```
Ambas formas de declarar `x` son iguales.

### [`tuple`](https://docs.python.org/3.12/library/typing.html#annotating-tuples)
A diferencia de otras colecciones nativas de Python, las tuplas pueden contener elementos de distintos tipos de datos, por lo tanto se pueden especificar tantos tipos de datos de sus items como sean necesario.

Cuando definimos el tipo `tuple` podemos especificar el tipo de dato de sus elementos uno a uno, o bien, utilizar la notación `...` como segundo parámetro de tipo para indicar que puede tener una cantidad variable de elementos de cierto tipo de dato (que se precede como primer parámetro de tipo).

```python
t1: tuple[int, int] = (1, 2)                # ok
t1 = (1, 'a')                               # error, el 2do elemento debe ser int
t1 = (1,)                                   # error, falta 2do elemento int
t2: tuple[str, int] = ('a', 3)              # ok
t3: tuple = ('a', 2, 3, 1)                  # ok, tuple[Any, ...]
t4: tuple[int, ...] = (1, 2, 3, 4, 5, 6)    # ok
t4 = (1, 2)                                 # ok
```
En este caso podemos ver que el _type checker_ detecta problemas al asignar t1 a objetos de tipo `tuple` que no coincida con la defición. Luego, la definición de `t4` permite tuplas de cualquier cantidad de números enteros. Si quisiéramos aceptar tuplas de cualquier cantidad de elementos de cualquier tipo podríamos usar `tuple[Any, ...]`.

## Subtipado estructural
La especicación PEP 484 define el sistema de tipos desde el punto de vista _nominal de subtipos_, una variable tipo `A` puede aceptar la asignación de un objeto de tipo `B` si y sólo si `B` es subclase de `A`.

En la especificación [PEP 544](https://peps.python.org/pep-0544/) se introduce el concepto de **subtipado estructural** donde se permite definir una clase con cierto comportamiento que coincide con otras clases para que el sistema reconozca a la primera como subclase de las últimas. Esto implica que aún sin declarar explícitamente las superclases con una herencia, Python reconoce estructuralmente que la nueva clase es un subtipo de otra a través del comportamiento definido. Se conoce también como **static duck-typing**.

```python
from collections.abc import Iterator, Iterable

class Contenedor:
    def __init__(self):
        self.elementos: list[int] = []

    def __len__(self) -> int:
        return len(self.elementos)
    
    def __iter__(self) -> Iterator[int]:
        return self.elementos.__iter__()

def mostrar_elemntos(xs: Iterable[int]):
    for x in xs:
        print(x)

mostrar_elemntos(Contenedor())
```
En este caso, la clase `Contenedor` es estructuralmente un subtipo de `Iterable` para el sistema de tipos según PEP 544, aún cuando no la hayamos declarado a través de la herencia. Esto se logra definiendo el comportamiento correspondiente implementando los métodos propios de `Iterable` como `__len__()` y `__iter__()`. Por ese motivo, el sistema no detecta un error cuando se utiliza el objeto de `Contenedor` como argumento de `mostrar_elementos()` que espera un `Iterable`.

Si no definiéramos el comportamiento esperado, el sistema de chequeo devolvería el error: `TypeError: 'Contenedor' object is not iterable`.

## Generics
En Python, a diferencia de lenguajes como Java o C#, no hay un soporte nativo para la definición de tipos genéricos como parte del lenguaje. Sin embargo, existen algunas técnicas y convenciones que podemos utilizar para lograr resultados similares a los que se obtienen con la programación genérica en otros lenguajes.

Recordemos que Python es un lenguaje de [tipado dinámico](#objetos), lo que significa que **las variables no están asociadas a tipos de datos específicos en tiempo de compilación**. Esto permite escribir código que funcione con diferentes tipos de datos **sin la necesidad de definirlos explícitamente como genéricos**, pero esto conlleva el riesgo de errores de tipos en tiempo de ejecución.

Una forma de proveer la seguridad que nos aportaban los tipos genéricos es a través de los type hints que proporcionan información sobre los tipos de datos que se esperan asociados a ciertas variables.

Veamos un ejemplo de un contenedor genérico en Python.

```python
from collections.abc import Iterator
from typing import TypeVar, Generic

T = TypeVar('T')

class Contenedor(Generic[T]):
    def __init__(self):
        self.elementos: list[T] = []

    def agregar(self, elemento: T):
        self.elementos.append(elemento)

    def __len__(self) -> int:
        return len(self.elementos)
    
    def __iter__(self) -> Iterator[T]:
        return self.elementos.__iter__()

contenedor: Contenedor[int] = Contenedor()
contenedor.agregar(1)
contenedor.agregar(3)
contenedor.agregar('a')     # error, porque contenedor es de tipo Contenedor[int]
```
Esta versión es compatible con Python 3.11 hacia atrás, donde se necesita generar una variable de tipo `T` con [`TypeVar`](https://docs.python.org/3.12/library/typing.html#typevar).

Desde Python 3.12 hacia adelante, podemos declarar la clase genérica así:
```python
class Contenedor[T]:
```

También podríamos limitar los tipos de datos aceptados por una variable. Simplemente se incorpora una expresión de tipo que refleje aquellos que son compatibles con la variable de tipo definida.
```python
from decimal import Decimal

# 3.11 o inferior
from typing import TypeAlias, Union, TypeVar, Generic
Number: TypeAlias = Union[decimal.Decimal, float]
T = TypeVar('T', bound=Number)
class Contenedor(Generic[T]):
    ...

# 3.12 o superior
type Number = Decimal | float
class Contenedor[T: Number]:
    ...
```
En este caso también utilizamos [`TypeAlias`](https://docs.python.org/3/library/typing.html#typing.TypeAlias) o [`type`](https://docs.python.org/3/reference/simple_stmts.html#type) para definir un nuevo **alias de tipo**, lo cual puede resultar útil para mejorar la comprensión del código y la reutilización. Luego se ven ambas formas de definir una variable de tipo llamada `T` que está acotada a aceptar tipos de datos numéricos.





> **Lectura de interés**:
> - [PEP 483: La teoría de Type Hints](https://peps.python.org/pep-0483/)
> - [PEP 484: Especificación de Type Hints](https://peps.python.org/pep-0484/)
> - [Librería typing - Soporte para Type Hints](https://docs.python.org/3.12/library/typing.html)
> - [Type Hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
> - [Python Style Guide](https://www.python.org/doc/essays/styleguide/)
> - [Python Type Checking](https://realpython.com/python-type-checking)
