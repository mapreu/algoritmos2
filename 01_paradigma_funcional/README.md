# Paradigma Funcional en Python

## Introducción
El paradigma funcional se basa en el concepto de funciones matemáticas y **evita el cambio de estado y las mutaciones de variables**. En lugar de modificar valores asociados a variables, se centra en el uso de expresiones, la **evaluación de funciones** y en la **composición** de estas para resolver problemas. Es un paradigma **declarativo** ya que se diseñan soluciones a través de la aplicación de funciones, definiendo qué se debe calcular en lugar de cómo realizarlo a través de instrucciones.

Existen diversos **lenguajes funcionales** como [Haskell](https://www.haskell.org/), [Lisp](https://lisp-lang.org/), [OCaml](https://ocaml.org/) o [Erlang](https://www.erlang.org/). Si bien Python no es un lenguaje puramente funcional, podremos utilizarlo aplicando algunos conceptos de este paradigma que aportan varios beneficios.

Si bien no lo trabajamos en la materia, este paradigma se apoya en el modelo computacional introducido por Alonzo Church, denominado [Cálculo Lambda](https://es.wikipedia.org/wiki/C%C3%A1lculo_lambda), donde todo cómputo se expresa como aplicaciones de abstracciones (funciones).

### Conceptos del Paradigma Funcional
A lo largo de este módulo analizaremos algunos conceptos característicos de la programación funcional y cómo se relacionan con Python.

- [Inmutabilidad](#inmutabilidad): Los datos son inmutables, una vez que se crean no se pueden cambiar. En lugar de modificar el estado de un objeto, se crean nuevos objetos con el estado deseado.

- [Funciones Puras](#funciones-puras-y-transparencia-referencial): Las funciones no tienen efectos secundarios y siempre producen el mismo resultado para los mismos argumentos. No dependen de variables externas o del estado del programa y tampoco lo alteran.

- [Transparencia Referencial](#funciones-puras-y-transparencia-referencial): Una función dada con los mismos argumentos siempre devolverá el mismo resultado, lo que facilita la comprensión y la validación del código.

- [Evaluación perezosa](#estrategias-de-evaluación): Es una estrategia de evaluación que demora la evaluación de una expresión hasta el momento en que se necesite su valor.

- [Recursión](#iteraciones): Se fomenta el uso de la recursión en lugar de ciclos iterativos para controlar el flujo del programa. Lo veremos con mayor detalle en el [módulo de Recursión](./02_recursion/README.md).

### El concepto de estado
Recordando el [paradigma orientado a objetos](https://github.com/mapreu/algoritmos1/tree/main/01_introduccion#atributos), el **estado** de un objeto se define a partir del valor asociado en cierto instante a sus atributos. Luego, mediante la invocación de métodos podíamos modificar el estado del objeto. Esta idea de estado no es única de este paradigma, sino que es común en el **paradigma imperativo**, donde se realizan modificaciones sobre el valor de las variables (memoria) a través de la **ejecución ordenada de sentencias o instrucciones**.

Veamos un ejemplo de contador con el paradigma imperativo en python:

```python
contador: int = 0

def incrementar_contador():
    global contador
    contador += 1

incrementar_contador()
print(contador)     # Salida: 1
```
La variable global `contador` almacena su valor en memoria y la función `incrementar_contador()` modifica su valor. Este es un **enfoque imperativo**, donde la operación produce un cambio en memoria (un **efecto secundario**) que depende del valor de esa variable en ese instante. Dado que la funcionalidad de `incrementar_contador()` no depende de un parámetro sino del estado del programa (particularmente el valor actual de `contador`), puede ser complejo de probar y detectar errores.

> Es propio del **paradigma imperativo** el uso de **procedimientos**, donde se modulariza cierta funcionalidad en un bloque de código que no devuelve un retorno. Es por ello que un procedimiento necesariamente produce algún **efecto secundario** en el programa al ejecutarse, de lo contrario no tendría sentido de existir.

```python
def incrementar_contador(contador: int) -> int:
    return contador + 1

contador = incrementar_contador(0)
print(contador)     # Salida: 1
```
Este simple cambio permite mejorar la _testeabilidad_ de la operación ya que ahora su retorno depende exclusivamente del argumento recibido. Analizaremos esto con las [funciones puras](#funciones-puras-y-transparencia-referencial).

> Un detalle positivo que nos provee el lenguaje Python es que todo parámetro de funciones **se pasa por valor y no por referencia**. Esto reduce la posibilidad de modificar variables ya que dentro de la función trabajamos con **copias de los argumentos originales**. Aunque recordemos que **en Python todo es un objeto**, así que estamos hablando de copias de **referencias**, por lo cual sí podríamos alterar el estado de un objeto.

En el paradigma funcional entonces reemplazaremos la noción estado por la **evaluación de funciones**, las cuales generarán nuevos valores a partir de los recibidos por parámetros. En Python, veremos que **generamos nuevos objetos** a partir de otros recibidos.

### Ciudadanos de primera clase
El concepto de **funciones como ciudadanos de primera clase** está estrechamente relacionado con otro concepto de **funciones de orden superior** que viene de las matemáticas. Una **función de orden superior** cumple al menos una de estas condiciones:
- Recibe una o más funciones como argumento
- Devuelve una función como retorno

En el área de computación algunos lenguajes permiten definir funciones de orden superior, y es principalmente una característica clave en la **programación funcional**. De esta forma, estos lenguajes consideran a las funciones como **ciudadanos de primera clase**, ya que podemos:
- pasarlas como parámetros de una función
- devolverlas como resultado de una función
- asignarlas a variables
- almacenarlas en estructuras de datos

Entonces, **las funciones de orden superior son aquellas funciones que pueden aceptar otras funciones como argumentos y/o devolver funciones como resultados**. Nos permiten la creación de abstracciones más poderosas y genéricas en el código, ya que las funciones de orden superior pueden ser configuradas o personalizadas para realizar una variedad de tareas. A su vez, nos facilitan la composición de funciones, la modularidad y la reutilización del código.

> En un lenguaje que admite funciones como ciudadanos de primera clase, **las funciones son tratadas como cualquier otro tipo de dato**, como números o cadenas de texto. Esto significa que las funciones pueden ser asignadas a variables, pasadas como argumentos a otras funciones, retornadas como resultados de funciones y almacenadas en estructuras de datos.

Esto nos provee de gran flexibilidad en el diseño de soluciones. Imaginemos que deseamos aplicar diferentes operaciones sobre los elementos de un arreglo. Una opción sería implementar diferentes métodos, uno para cada operación, donde dentro de un bucle se aplique esta operación particular. Por ejemplo, si queremos elevar al cuadrado todos los números de un arreglo, implementaríamos ese método específico realizando la operación `elemento * elemento` dentro del bucle. Ahora bien, si pudiéramos pasar la operación a realizar como parámetro, podríamos definir un único método que la aplique a los elementos. Luego, al momento de invocarlo le decimos qué operación queremos hacer. Esta versión más flexible es propia del estilo funcional (la función `map`).

Veamos este ejemplo en python de una función de orden superior que aplica una función a cada elemento de una lista.

```python
from typing import TypeVar, Union
from collections.abc import Callable, Sequence

Numerico = Union[int, float]

T = TypeVar("T")

def aplicar_operacion(lista: Sequence[T], operacion: Callable[[T], T]) -> Sequence[T]:
    resultado = []
    for elemento in lista:
        resultado.append(operacion(elemento))
    return resultado

# Definición de funciones que se aplicarán a la lista
def cuadrado(x: Numerico) -> Numerico:
    return x * x

def inverso(x: Numerico) -> Numerico:
    return 0 - x

# Uso de funcion de orden superior
numeros: list[int] = [1, -2, 3, -4, 5, -6]
numeros_cuadrados = aplicar_operacion(numeros, cuadrado)  # Elevar al cuadrado
numeros_inversos = aplicar_operacion(numeros, inverso)   # Inverso aditivo

print(numeros_cuadrados)  # [1, 4, 9, 16, 25, 36]
print(numeros_inversos)  # [-1, 2, -3, 4, -5, 6]
```
En este ejemplo definimos una función de orden superior `aplicar_operacion` que recibe una función como segundo parámetro. Luego, como en Python las funciones son ciudadanos de primera clase (son objetos), podemos pasarlas como argumento a nuestra función previa. 

### Ejercicio: Función de orden superior
- Implementar una función llamada _wrapper_ que reciba por parámetro a otra función _f_ sin argumentos, la ejecute e imprima en pantalla el mensaje de ejecución: "Ejecutada f()".
- Extender la función _wrapper_ de forma que pueda aceptar cualquier función con argumentos variables y se puedan pasar también desde la función _wrapper_ para que se invoquen en _f_. Por ejemplo, si _f_ acepta 3 argumentos, éstos deberían también pasarse a _wrapper_ para que se invoque _f(arg1, arg2, arg3)_ dentro.

    _TIP: Ver el type hint [`Callable`](../B_Python_Type_Hints/README.md#callable)._

    _TIP 2: Ver pasaje de argumentos con [*args](https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists) y [**kwargs](https://docs.python.org/3/tutorial/controlflow.html#keyword-arguments)._

### Composición de funciones
El cocepto de composición de funciones también parte de la matemática, donde podemos definir una nueva función a partir de dos o más funciones. La idea es evaluar la aplicación sucesiva de las funciones compuestas a partir de un argumento inicial. 

`h = g o f => h(x) = g(f(x))`

Este _encadenamiento_ de funciones es clave en la programación funcional ya que nos permite _conectar_ la entrada y salida de funciones para realizar la transformación deseada. Incluso podemos pensar este concepto de composición a niveles mayores de abstracción, por ejemplo, componiendo programas o módulos completos.

Veamos este ejemplo en paradigma imperativo:
```python
def add_elemento(xs: list[int], x: int) -> None:
    xs.append(x)

lista_enteros: list[int] = []
add_elemento(lista, 1)
add_elemento(lista, 2)
add_elemento(lista, 3)
```
Dado que trabajamos modificando un objeto mutable como la lista, en el estilo imperativo realizamos instrucciones que permiten modificar la lista incorporando elementos. Ahora veamos cómo podríamos construir la lista desde la mirada funcional.

```python
def add_elemento(xs: list[int], x: int) -> list[int]:
    ys: list[int] = xs.copy()
    ys.append(x)
    return ys

lista_enteros: list[int] = add_elemento(add_elemento(add_elemento([], 1), 2), 3)
```
En este caso nos apoyamos en la composición de funciones, particularmente reutilizando la misma operación `add_elemento`, para generar un resultado similar al previo. El cambio más importante es devolver la estructura modificada en la función, de forma que pueda ser consumida sucesivamente como argumento de la próxima.

> Así como en matemática hablamos de dominio y codominio de una función, en la programación debemos contemplar los **tipos de datos de los parámetros y retorno**. Necesitamos considerar bien la firma de nuestras funciones durante el diseño para poder aplicar luego las composiciones requeridas.

## Inmutabilidad
La inmutabilidad se refiere a la incapacidad de un objeto para cambiar su estado después de su creación. Esto implica que una vez que se ha creado un objeto inmutable, sus atributos internos no pueden ser modificados. Por lo tanto, **no puede cambiar su estado**.

### ¿Por qué diseñaríamos algo inmutable?
Recordemos que en la programación funcional no registramos el estado de ejecución de un programa en variables u objetos como sí lo hacemos en otros paradigmas, por lo tanto trabajamos siempre con elementos inmutables que sirven de entrada y salida a las funciones. 

Diseñar soluciones con elementos inmutables nos provee algunos beneficios.

#### Claridad y Entendimiento
La inmutabilidad simplifica la lógica del programa al reducir la cantidad de cambios de estado posibles. Esto hace que el código sea más fácil de entender ya que no es necesario rastrear cambios en el estado a lo largo del tiempo.

#### Prevención de Cambios Accidentales
Cuando se crea una instancia de una clase inmutable, sus valores no pueden ser modificados. Esto ayuda a prevenir cambios accidentales en el estado del objeto, lo que puede conducir a resultados inesperados o errores difíciles de rastrear.

#### Concurrencia más sencilla y segura
En entornos con concurrencia (_multi-threading_), las clases inmutables eliminan la necesidad de sincronización para evitar problemas de concurrencia. Dado que no hay posibilidad de cambios en el estado, varios hilos (_threads_) pueden acceder y utilizar objetos inmutables de manera segura sin preocuparse por conflictos o inconsistencias.

#### Facilita la Programación Funcional
Al diseñar clases inmutables, se facilita la adopción de principios funcionales, como la creación de funciones puras y la composición de operaciones, porque necesariamente se deben devolver nuevos objetos generados a partir de los originales agregando la modificación que corresponda.

#### Optimización de Rendimiento:
En ciertos casos, los compiladores y entornos de ejecución pueden optimizar el código que involucra objetos inmutables, ya que la falta de cambios de estado permite realizar ciertas optimizaciones.

### Transitividad
> En lenguajes orientados a objetos como Python debemos tener presente que los atributos de un objeto pueden ser en realidad referencias a otros objetos, por lo cual deberíamos buscar una **_inmutabilidad transitiva_**, lo cual implica que esos objetos asociados a los atributos también sean inmutables. De lo contrario, nuestro objeto podría mutar aún sin haberle realizar una modificación directa.

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class ContenedorInmutable(Generic[T]):
    def __init__(self, valor: T):
        self._valor: T = valor
    
    def contenido(self) -> T:
        return self._valor

xs: list[int] = [1, 2, 3]
contenedor: ContenedorInmutable[list[int]] = ContenedorInmutable(xs)
xs[0] = 9

print(contenedor.contenido())   # [9, 2, 3]
```
En este ejemplo definimos la clase genérica "inmutable" donde sólo tiene un método _getter_ `contenido`. Luego instanciamos un objeto llamado `contenedor` que tendrá una lista de enteros como valor. Si bien la referencia a la lista dentro del contenedor es inmutable, la lista en sí no lo es. Por eso no se cumple la transitividad de inmutabilidad en este caso, porque el contenido de `contenedor` puede cambiar cuando se lo modifica directamente como se hace en `xs[0] = 9`.

Un detalle no menor es que el atributo `_valor` aún puede ser accedido y modificado desde afuera de la clase, simplemente invocando por ejemplo `contenedor._valor = [4]`. Veremos más adelante cómo mejorarlo en [Clases propias inmutables](#clases-propias-imnutables).

### Tipos nativos de Python
En general, los tipos de datos incorporados en el lenguaje son **inmutables**, por lo tanto una vez creado un objeto de esos tipos, no podremos modificar su estado. La única forma es generar un objeto nuevo a partir del primero con los cambios necesarios.

Los siguientes tipos de datos son **inmutables**:
- **Números**: clases `int`, `float`, `complex`
- **Bytes**: clase `bytes`
- **Cadenas**: clase `str`
- **Tuplas**: clase `tuple`
- **Booleanos**: clase `bool`
- **Frozen Sets**: clase `frozenset`

Los siguientes tipos de datos son **mutables**:
- **Listas**: clase `list`
- **Diccionarios**: clase `dict`
- **Conjuntos**: clase `set`
- **Byte arrays**: clase `bytearray`

Entonces debemos tener cuidado al utilizar aquellos tipos de datos mutables cuando buscamos un enfoque funcional. Esto no implica en usar sólo tipos inmutables, porque seguramente necesitáramos definir otro tipo de estructuras, sino que tendremos que evitar mutarlos y procurar instanciar nuevos objetos.

### Clases inmutables
En el [acceso a miembros de una clase](../A_Python_POO/README.md#accesibilidad-a-miembros-de-clase), Python no ofrece un mecanismo para ocultar completamente un miembro del acceso público. A su vez Python es muy flexible por lo cual debemos tener mucho cuidado cuando buscamos definir clases propias que sean inmutables. Analicemos algunas técnicas que podemos utilizar para lograrlo.

### Clases imnutables: Ocultando atributos
La condición más importante, pero no suficiente, sería ocultar los atributos de nuestra clase utilizando la convención de nombre que indica **utilizar como prefijo el guión bajo**. Decimos que no es suficiente porque podríamos alterar el valor de nuestros atributos si los accedemos públicamente, recordemos que es una simple notación que indica a quien consume la clase que no debería hacerlo.

El ejemplo de [ContenedorInmutable](#transitividad) aplica este concepto.

> Existe un **atributo de clase** especial [`__slots__`](https://docs.python.org/3/reference/datamodel.html#object.__slots__) que permite optimizar la creación de instancias en memoria, ya que **podemos asignarle un conjunto fijo de nombres de atributos** que tiene una instancia de esa clase. Por lo tanto, si definimos `__slots__ = ('x', 'y',)` como atributo de una clase significa que un objeto de esa clase sólo podrá tener como atributos a _x_ e _y_.

### Clases imnutables: Properties
Sabemos que en Python existe posibilidad de [convertir atributos en propiedades](../A_Python_POO/README.md#atributos---propiedades) para mejorar el encapsulamiento de la clase. Una estrategia sería **convertir los atributos en propiedades de sólo lectura**, es decir, no definir los _setters_.

```python
class MiClaseInmutable:
    def __init__(self, valor_inicial):
        self._valor = valor_inicial
    
    @property
    def valor(self):
        return self._valor

objeto_inmutable = MiClaseInmutable(20)
objeto_inmutable.valor                      # 20
objeto_inmutable.valor = 10                 # AttributeError: property 'valor' of 'MiClaseInmutable' object has no setter
objeto_inmutable._valor = 10                # Modifica el valor
objeto_inmutable.valor                      # 10
```
En este ejemplo, sólo definimos el _getter_ de la propiedad, por lo cual no puede ser modificada normalmente desde fuera de la clase. Aunque sí podríamos modificar el atributo directamente como sucede en `objeto_inmutable._valor = 10`.

Las propiedades en Python se implementan por debajo mediante un [descriptor](https://docs.python.org/3/howto/descriptor.html#managed-attributes). No veremos esta funcionalidad en este módulo, pero básicamente los descriptores son **clases que implementan ciertos métodos especiales** que dan comportamiento paricular a los objetos instanciados cuando **se asignan como atributos de una clase**. Diseñar nuestros propios descriptores podría ser una opción más bajo nivel para diseñar clases inmutables.

### Clases imnutables: Métodos especiales `__setattr__` y `__delattr__`
Cuando intentamos realizar una asignación para un atributo de un objeto, internamente se invoca el método [`__setattr__`](https://docs.python.org/3/reference/datamodel.html#object.__setattr__) que recibe como argumentos: el objeto en sí, el nombre del atributo y el valor a asignarle. Entonces, si sobreescribimos este método en nuestra clase inmutable, podríamos evitar cualquier tipo de asignación en los atributos de la clase. Sólo necesitaríamos invocar el método sin modificar (heredado de `object`) para inicializarlos en el método `__init__`.

El método [`__delattr__`](https://docs.python.org/3/reference/datamodel.html#object.__delattr__) es similar y sólo recibe como argumento el nombre del atributo. Se invoca cuando se intenta eliminar un atributo de un objeto con el comando `del`. Así que también nos serviría para evitar que se eliminen atributos.

Veamos un ejemplo:

```python
class MiClaseInmutable:
    __slots__ = ('_valor',)

    def __init__(self, valor_inicial):
        super().__setattr__('_valor', valor_inicial)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        raise AttributeError(f'No es posible setear el atributo {__name}')
    
    def __delattr__(self, __name: str) -> None:
        raise AttributeError(f'No es posible eliminar el atributo {__name}')
    
    def valor(self):
        return self._valor
```
En la inicialización debemos utilizar el `super().__setattr__()` porque el propio devuelve una excepción. Entonces una vez inicializado el objeto, nunca podremos modificarlo.

> Si combinamos la sobreescritura de estos métodos con el uso del atributo `__slots__` logramos una **muy buena inmutabilidad** de la clase, por lo menos superficial (recordar el tema de la [transitividad](#transitividad)).

### Clases imnutables: Named Tuples
Las tuplas son un tipo de dato inmutable en Python, por lo cual nos pueden ser útiles para construir nuevos objetos inmutables también. La forma más básica sería asociar valores a una tupla como si fueran los atributos ordenados de mi abstracción de dato, pero eso sería complejo de comprender y mantener eventualmente. Una opción sería utilizar [`namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple) que nos permite generar un objeto subclase de `tuple`, por ende inmutable, pero con los atributos con nombres en lugar de índices.

```python
from collections import namedtuple

MiClaseInmutable = namedtuple('MiClaseInmutable', 'valor1 valor2')
mi_obj = MiClaseInmutable(10, 20)
mi_obj                  # MiClaseInmutable(valor1=10, valor2=20)
mi_obj.valor1           # 10
mi_obj.valor2           # 20
```
En este ejemplo, definimos nuestra clase a partir de la función `namedtuple` que devuelve una clase con el nombre que le pasamos en el primer argumento y los atributos como una cadena separada por espacios en el segundo argumento (también se acepta una lista de cadenas). Una vez instanciada, no es posible realizar modificaciones en los atributos.

> El problema con esta estrategia es que perdemos el concepto de **encapsulamiento** que nos proveen las clases, vinculando la estructura con el comportamiento. Como solución podemos definir nuestra clase heredando desde `namedtuple`.

```python
from collections import namedtuple

class MiClaseInmutable(namedtuple('MiClaseInmutable', 'valor1 valor2')):
    __slots__ = ()
    def __repr__(self) -> str:
        return f'{super().__repr__()} INMUTABLE'
    
mi_obj = MiClaseInmutable(10, 20)
mi_obj                  # MiClaseInmutable(valor1=10, valor2=20) INMUTABLE
```
Debemos agregar `__slots__` para evitar que la clase pueda aceptar nuevos atributos, pero luego podemos definir el comportamiento que deseemos, como en el ejemplo sobreescribiendo el método especial `__repr__`.

### Clases imnutables: dataclasses
El módulo [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) provee funcionalidad que implementa automáticamente [**métodos especiales**](../A_Python_POO/README.md#métodos-especiales) en clases que diseñamos. La particularidad es que definimos la estructura de nuestras clases con **variables de clase** con anotaciones de tipo, y luego la función decoradora [`dataclass`](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass) genera los atributos de instancia correspondientes implementando el método `__init__()`.

Veamos este ejemplo:
```python
from dataclasses import dataclass

@dataclass
class Persona:
    nombre: str
    apellido: str
    edad: int

    def es_adulta(self):
        return edad >= 18
```
Al incorporar el decorador `@dataclass` se generan automáticamente métodos especiales como el siguiente:
```python
def __init__(self, nombre: str, apellido: str, edad: int) -> None:
    self.nombre = nombre
    self.apellido = apellido
    self.edad = edad
```
De esa forma se simplifica la implementación de clases, por lo menos su estructura, y luego nos centramos en definir el comportamiento normalmente. 

Por defecto, el decorador `@dataclass` nos implementará automáticamente los siguientes métodos: `__init__()`, `__repr__()` y `__eq__()`.

El decorador `@dataclass` tiene un parámetro (recordemos que es una función como cualquier otra) que permite convertir a los **atributos de instancia de solo lectura**. El nombre del parámetro es `frozen` y es un booleano que si se define en `True` podemos evitar la asignación nueva de valores y así **proveer inmutabilidad a nuestra clase**.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Persona:
    nombre: str
    apellido: str
    edad: int

    def es_adulta(self):
        return edad >= 18
    
p = Persona("Julia", "Martinez", 22)
print(p)        # Persona(nombre='Julia', apellido='Martinez', edad=22)
p.edad = 20     # FrozenInstanceError: cannot assign to field 'edad'
```
El uso de `@dataclass(frozen=True)` es una opción sencilla muy interesante para alcanzar clases inmutables.

> Siempre recordemos que, si asignamos objetos como atributos de una clase que deseamos que sea inmutable, estos objetos **también deberían ser de clases inmutables**. De lo contrario debemos tener mucho cuidado en cómo se mutan estos objetos para evitar problemas de consistencia y efectos secundarios.

### Ejercicio: Conjunto inmutable
Implementar una versión de un conjunto de elementos de cualquier tipo que sea inmutable. Podemos apoyarnos en la `tuple` de Python. El conjunto se crea con una cantidad de elementos variables y luego ya no puede modificarse.

## Funciones puras y transparencia referencial
Una **función pura** cumple con dos condiciones:
- Dados los mismos parámetros de entrada, **siempre** devuelve el mismo valor como retorno.
- No debe producir **efectos secundarios**, sólo debe enfocarse en realizar el cálculo necesarios para generar el retorno a partir de sus parámetros.

> Una consecuencia interesante de utilizar funciones puras para computar algo es que es posible optimizar el cómputo cambiando el orden de evaluación o paralelizándolo.

### Tramsparencia referencial
La primera condición está relacionada con el concepto lingüístico de **transparencia referencial**, donde podríamos reemplazar a cierta expresión de una función y argumentos aplicados simplemente con su valor de retorno y así no se producirían cambios semánticos en el programa. Por ejemplo:

```python
def suma(x: int, y: int) -> int:
    return x + y

nro: int = suma(10, 6) * 2
nro: int = 16 * 2           # Reemplazamos suma(10, 6) por su valor evaluado 16
```
La operación `suma` es una función pura porque cumple ambas condiciones mencionadas. La primera asignación de `nro` consume la función `suma` y es equivalente semánticamente a la segunda definición, porque `suma(10, 6)` siempre se evaluará en `16`.

> Si una función no es referencialmente transparente, se dice que es **referencialmente opaca**.

### Efectos secundarios
Este concepto está fuertemente relacionado con el de **estado**. Una operación que produce efectos secundarios o colaterales es aquella que **puede incluir diversas interacciones con el entorno del programa y modificar el estado fuera del ámbito local de la función**. 

Algunos de los tipos comunes de efectos secundarios incluyen:

- **Modificación de Variables Globales**: Una función impura puede modificar variables globales, alterando así el estado global del programa. Esto puede afectar a otras partes del código que dependen de esas variables.

- **Modificación de Argumentos**: Una función impura puede modificar el valor asociado a un parámetro (si se pasa por referencia) o alterar el estado de un objeto que se pase como argumento (en lenguajes que aceptan el pasaje por valor de referencias). Esto puede afectar a otras partes del código que dependen de esas variables.

- **Operaciones de Entrada/Salida (I/O)**: Interacciones con el mundo exterior, como lectura o escritura en archivos, envío de correos electrónicos, acceso a bases de datos, etc. Estas operaciones son típicamente impuras ya que pueden tener efectos que van más allá de la propia ejecución de la función.
    - **Impresiones en Consola o Registro de Eventos**: La impresión en la consola o el registro de eventos (_logging_) también se considera un efecto secundario, ya que implica una interacción con el entorno fuera de la función, son operaciones de salida.
    - **Interacciones de Red**: Las operaciones de red, como solicitudes a una API, también pueden ser impuras, ya que están interactuando con el entorno.

- **Llamadas a Funciones con Efectos Secundarios**: Si una función llama a otra función impura, automáticamente se convierte en una función impura también. A su vez, si ambas producen efectos colaterales, se pueden acumular y propagarse.

- **Generación de Números Aleatorios**: Si una función genera números aleatorios, su resultado puede variar en diferentes llamadas, lo que introduce una variabilidad no determinista.

> En lenguajes funcionales, donde nos apoyamos en funciones puras, se suele utilizar una estructura algebraica denominada [**Mónada**](https://es.wikipedia.org/wiki/M%C3%B3nada_(programaci%C3%B3n_funcional)) para tratar problemas que requieren encapsular cierta secuencia de pasos ordenados para resolverlos, por ejemplo la Entrada/Salida. Si bien en Python no es necesario su uso, disponemos del paquete [`PyMonad`](https://pypi.org/project/PyMonad/) que incluye varias mónadas y otras funciones interesantes.

Veamos un ejemplo de efecto secundario al modificar un argumento:

```python
def duplicar_elemento(lista: list[int], indice: int) -> list[int]:
    lista[indice] *= 2
    return lista

def duplicar_elemento_pura(lista: list[int], indice: int) -> list[int]:
    nueva_lista = lista.copy()
    nueva_lista[indice] *= 2
    return nueva_lista

# Uso de ambas funciones
original: list[int] = [1, 2, 3]
resultado1: list[int] = duplicar_elemento(original, 1)
resultado2: list[int] = duplicar_elemento_pura(original, 1)

print(f"Impura: {resultado1}")  # Salida: [1, 4, 3]
print(f"Pura: {resultado2}")  # Salida: [1, 8, 3]
```
La función `duplicar_elemento` produce de forma sutil un efecto secundario al modificar los elementos de la lista original que se pasa como argumento. Esto es posible debido a que Python utiliza el pasaje por valor de referencias de objetos, es decir, pasa una copia de la referencia a memoria donde vive el objeto. Entonces, al acceder a un modificador de la clase mediante la asignación `lista[indice]`, estamos alterando el estado del objeto y así generando el efecto colateral que luego se ve reflejado cuando se invoca la operación `duplicar_elemento_pura` que recibe una lista original modificada.

> El uso de `lista.copy()` es suficiente en este caso porque sabemos que tiene elementos de un tipo de dato inmutable (`int`), así que usamos una [copia superficial](https://github.com/mapreu/algoritmos1/blob/main/04_igualdad_orden_copia/README.md#copia-superficial). Si hubiésemos trabajado con una lista de elementos mutables (por ejemplo otras listas), deberíamos haber hecho una [copia profunda](), por ejemplo con [`copy.deepcopy()`](https://docs.python.org/3/library/copy.html#copy.deepcopy).

Algo interesante que surge de este ejemplo es que podríamos decir que ambas operaciones son referencialmente transparentes, ya que su retorno siempre depende exclusivamente del argumento que se pasa. El hecho de que la primera genere un efecto secundario es que la convierte en función impura.

> Un tipo de efecto secundario que encontramos en los lenguajes imperativos es el **ciclo o iteración**. Dado que se logra almacenando cierto estado local del programa, sea mediante una variable contadora o alterando la condición de terminación del bucle. En el paradigma funcional, esta estructura de control se reemplaza mediante el uso de la [recursión](../02_recursion/README.md).

### Ejercicio: Funciones puras e impuras
Proponer ejemplos de funciones impuras para cada tipo de efecto secundario mencionado y cómo se podrían conventir, si es posible, a versiones de funciones puras.

> Es importante destacar que, aunque las funciones puras son preferibles en muchos casos debido a su predictibilidad y facilidad de razonamiento, las funciones impuras suelen ser necesarias para interactuar con el entorno y realizar operaciones prácticas en el mundo real. La clave es gestionar y controlar cuidadosamente estos efectos secundarios para mantener un código claro y mantenible.

## Estrategias de evaluación

En el cálculo lambda computamos una expresión a través de la reescritura de la misma, aplicando diferentes reglas de conversión y reducción hasta llegar a expresiones irreducibles, lo que se denomina en _forma normal_ o _forma canónica_. A través de la reducción Podemos encontrar dos estrategias para reducir un término a una _forma normal_, una expresión que resulta irreducible.
- **Orden aplicativo**: Se reducen primero las expresiones reducibles más internas, aquellas que no contienen términos reducibles.
- **Orden normal**: Se reducen primero las expresiones reducibles (_redex_) más externas, aquellas que no están incluidas como términos de otras.

Veamos este ejemplo:
```python
def cuadrado(x):
    return x * x

cuadrado(4 + 2)
```
Si seguimos el orden aplicativo la reducción sería: `cuadrado(4 + 2) -> cuadrado(6) -> 6 * 6 -> 36`. Primero se evalúa `4 + 2` y luego se evalúa `cuadrado(6)`.

En cambio, si seguimos el orden normal sería: `cuadrado(4 + 2) -> (4 + 2) * (4 + 2) -> 6 * 6 -> 36`. Podemos imaginar a esta estrategia como **reemplazar el cuerpo de la función dentro de la expresión**. En este caso reemplazamos el cuerpo de la función `x * x` aplicándole los argumentos aún sin reducir. Por eso aparece la expresión `(4 + 2) * (4 + 2) `.

### Evaluación estricta
Podemos encontrar una analogía entre el concepto de reducción mencionado y la evaluación de expresiones en la programación. Similar al **orden aplicativo**, en la evaluación estricta **se requieren resolver antes las expresiones internas** o argumentos de una función. Esta idea está relacionada con el concepto de **evaluación _impaciente_** o _eager_ que plantea que debemos evaluar todos las expresiones internas antes de avanzar con la externa, aún si no fueran necesarias para calcular el valor.

> En **Python** prácticamente todo se evalúa de **forma estricta**, con ciertas excepciones que veremos a continuación en evaluación no estricta.

Veamos este ejemplo:
```python
def func1():
    print('Evalua funcion 1')
    return 1
def func2():
    print('Evalua funcion 2')
    return 2
def sumaRara(x, y):
    print('Evalua funcion externa')
    return x if x == 1 else x + y

sumaRara(func1(), func2())
# Salida:
# Evalua funcion 1
# Evalua funcion 2
# Evalua funcion externa
# 1
```
Previo a la ejecución de la función `sumaRara`, el intérprete ejecuta las funciones que se pasan como argumento. Esto está relacionado con la estrategia de **pasaje de parámetros** que comúnmente llamamos **pasaje por valor**. Sería difícil pasar un valor como argumento sin antes evaluar la expresión que lo genera. De forma similar ocurre con otros tipos de pasajes de parámetros que vemos en la programación imperativa (como es el caso de pasaje por referencia).

Esta estrategia puede traer algunos problemas si la función externa no requiere siempre de todos sus argumentos evaluados para retornar un valor. En el ejemplo, el segundo argumento `func2()` podría haberse evitado ya que no se utiliza en el retorno de la función (porque x es igual a 1). Si el costo de la evaluación de `func2` fuera muy alto, habríamos tenido un impacto en rendimiento innecesario.

### Evaluación no estricta
Esta estrategia es similar al **orden normal**, pero no necesariamente requiere evaluar antes todas las externas, sino que puede hacer una evaluación parcial de las internas. Por ejemplo, una función evaluada de forma no estricta p**odría devolver un resultado aún si no se evaluaron todos sus argumentos** (porque no lo necesitaron). Por ese motivo se denomina no estricta, haciendo referencia a toda estrategia que no cumpla el caso estricto.

> Uno de los aspectos que hace **eficiente** la programación funcional es la capacidad de **diferir el cómputo de expresiones al momento en el cual son requeridas**. Aquí el concepto de **evaluación en orden normal es fundamental** ya que permite ignorar expresiones que puedan ser muy costosas de operar si no son necesarias, como así también expresiones que pudieran generar algún error.

#### Evaluación de cortocircuito
Esta estrategia se aplica a **expresiones booleanas** y se implementa en varios lenguajes de programación, incluyendo Python, donde se permite evitar la evaluación de un segundo término dependiendo del valor del primero. Veamos los dos casos donde se aplica.

```python
<expresion_1> and <expresion_2>
```
Si `<expresion_1>` es `False`, entonces `<expresion_2>` **no se evalúa**.

```python
<expresion_1> or <expresion_2>
```
Si `<expresion_1>` es `True`, entonces `<expresion_2>` **no se evalúa**.

Veamos este ejemplo para saber si un número es divisor de otro:
```python
def esDivisor(nro: int, divisor: int) -> bool:
    return (divisor > 0) and (nro % divisor == 0)

esDivisor(10, 0)    # False
```
La expresión de retorno incorpora esta estrategia de evaluación, porque si fuera estricta tendría que primero resolver la expresión `divisor > 0` y luego la expresión `nro % divisor` para continuar con las restantes (si utilizamos el orden de izquierda a derecha), pero no podría hacerlo porque surgiría la excepción de que no es posible obtener el módulo de un número con 0. Dado que Python utiliza la evaluación no estricta para estos casos, es posible devolver directamente `False` porque el primer término del `and` ya retorna ese valor y no tiene sentido evaluar el segundo.

#### Evaluación perezosa
La **evaluación perezosa o _lazy_** es una estrategia que establece que **la evaluación de una expresión puede dilatarse hasta que sea necesario su valor**. Podría pensarse como el opuesto de la [evaluación _impaciente_](#evaluación-estricta). A su vez se combina con el concepto de [**memoización**](../02_recursion/README.md#memoizacion) que resulta clave en la programación dinámica, donde se almacenan los valores de expresiones previamente evaluadas.

Esta estrategia es fundamental en la programación funcional ya que permite trabajar con **estructuras infinitas**. En Python encontraremos solución a esto a través de **generadores** implemetados mediante [funciones generadoras](https://peps.python.org/pep-0255/) o [expresiones generadoras](https://peps.python.org/pep-0289/), las cuales permiten retornar un **iterador perezoso** mediante la palabra reservada `yield`.

> El `yield` es análogo al `return` de una función normal. La diferencia es que devuelve un [iterador](https://docs.python.org/3/glossary.html#term-iterator) de cierta colección de datos. Cuando invocamos la función generadora, se devuelve el iterador que podemos almacenar en una variable. Luego, cuando se invoca `next(<iterador>)` (implementado en el método `__next()__`) sobre el iterador, se ejecutan las instrucciones de la función generadora hasta el `yield`, momento en el cual **suspende la ejecución de la función** y se devuelve el valor actual dado por la expresión del `yield` en ese instante. En cada invocación del `next()` continúa la ejecución de la función (desde la instrucción siguiente del `yield`) y se vuelve a suspender como el caso previo o termina si ya no quedan instrucciones.

> Un **iterador** en Python es un **objeto** que implementa los métodos especiales `__iter()__` y `__next()__` que nos permite iterar sobre una colección de datos [_iterable_](https://docs.python.org/3/glossary.html#term-iterable). Se basa en el [patrón de diseño Iterator](https://en.wikipedia.org/wiki/Iterator_pattern), donde se desacopla la lógica de iteración de los contenedores o colecciones de datos y se agrega un nivel de abstracción sobre esta actividad. Proveen una forma de **acceder a los elementos de a uno a la vez y sin repetirlos**, es decir, recorrer la colección de datos sin la necesidad de cargarla completamente en memoria. Podemos generarlos sencillamente extendiendo la clase [collections.abc.Iterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator).

Veamos un ejemplo básico:
```python
from collections.abc import Iterator

def genera_saludo() -> Iterator[str]:
    yield "Hola"
    yield "Buenas"
    yield "Buen día"

iterador_saludos = genera_saludo()
print(next(iterador_saludos))   # Hola
print(next(iterador_saludos))   # Buenas
print(next(iterador_saludos))   # Buen día
print(next(iterador_saludos))   # Error StopIteration
```
Nuestra función generadora retorna un **iterador** que produce 3 valores hasta llegar al final del flujo. En cada llamada al `next()` se avanza con la ejecución de la función **hasta el próximo `yield`** y se vuelve a suspender. El final está marcado por la **excepción `StopIteration`**, por lo cual podría utilizarse sencillamente como iteración en un bucle así:
```python
for saludo in genera_saludo():
    print(saludo)
```

A diferencia de una secuencia como las listas, **un generador finito sólo puede consumirse una única vez**. Una vez que ha llegado al final, no es posible volver atrás. En ese caso se debe instanciar un nuevo objeto generador.
```python
iterador_saludos = genera_saludo()
for saludo in iterador_saludos:
    print(saludo)
for saludo in iterador_saludos:
    print(saludo)
```
En este ejemplo, el segundo bucle `for` no presenta ninguna impresión en consola porque el iterador ya fue consumido en el primer bucle.

> Algo interesante de los generadores de Python es que **son también iteradores**, ya que el objeto retornado por una función o expresión generadora pertenece a la clase [Generator](https://docs.python.org/3/library/collections.abc.html#collections.abc.Generator), la cual es subclase de [Iterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator). Por eso decimos que los generadores, al invocarlos, devuelven iteradores. Por ese motivo tienen incorporados varios métodos en común con las secuencias como el `sorted()`, `max()`, `sum()`, etc.

Entonces, mediante el uso del funciones o expresiones generadoras podemos lograr en Python una evaluación diferida al momento en el cual se lo necesita (se consume el valor retornado). Mencionamos que esto es útil para modelar **estructuras infinitas**, veamos con un ejemplo.
```python
from collections.abc import Iterator

def positivos_pares() -> Iterator[int]:
    numero: int = 0
    while True:
        yield numero
        numero += 2
```
Esta función generadora produce de forma infinita (hasta el límite del tipo `int`) los números pares positivos. Si la consumiéramos dentro de un `for` se ejecutaría utilizando en cada iteración el siguiente número par. También podríamos hacer un mínimo cambio en la condición de corte del `while` para hacer, en lugar de un generador infinito, un generador finito de cierta cantidad (por ejemplo con `while numero < <limite>`).

> Los generadores nos permiten construir estructuras _a demanda_ de forma _perezosa_, ¿podemos notar alguna consideración respecto a las [funciones puras](#funciones-puras-y-transparencia-referencial)?

También podríamos implementar la función previa como una **expresión generadora**, utilizando una sintaxis similar a [list comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions). Es más, una _list comprehension_ es en realidad una expresión generadora a la cual se le aplica la función `list()` para construir la lista completa de sus elementos.

Veamos cómo se construye la expresión generadora del ejemplo previo.

```python
positivos_pares = (x for x in range(0, 10, 2))  # <generator object <genexpr> ...>
```
La variable `positivos_pares` es un generador que produce los números pares del 0 al 8.

> Existe otro caso de uso popular para los generadores en Python, son útiles para consumir flujos infinitos como _streams_ de datos en tiempo real.

### Ejercicio: Generador de primos
Implementar una función generadora que permita producir todos los números primos uno a uno.

### Ejercicio: Pipeline de datos con generadores
En ciertos casos podemos encontrarnos con archivos CSV muy grandes que no entren en memoria para procesarlos completamente, por lo cual veremos una forma de procesar datos a demanda a medida que se leen. Se pide implementar: 
- un lector de archivo CSV utilizando 3 generadores:
    - uno para producir cada línea leída del archivo.
    - otro para producir una lista de campos _string_ a partir de cada línea leída, consumiendo el generador previo.
    - otro para producir un diccionario a partir de cada lista de campos obtenida con el generador previo.
- calcular la suma de los _sepal\_width_ de todas las especies _Iris-setosa_ del dataset [IRIS.csv](../datasets/IRIS.csv), utilizando un generador que produzca cada valor de _sepal\_width_ de una planta a la vez que sea de esa especie. _Valor esperado: 170.9_
- similar al punto anterior, pero calculando el promedio del _sepal\_width_ de las especies _Iris-setosa_. _Valor esperado: 3.418_

_TIP: Ver la función [`open()`](https://docs.python.org/3/library/functions.html#open) para leer archivos de texto._

## Transformación de funciones
Mencionamos al principio que un programa funcional se apoya en computar algo a través de la composición de funciones, que pueden ser abstracciones más grandes como programas o módulos. No siempre es trivial la transformación de un conjunto de sentencias imperativas a una sucesión de funciones aplicadas desde cierta entrada. Veremos algunos conceptos y herramientas que provee tanto el lenguaje Python como el paradigma funcional en general para lograr estas composiciones y mejorar el diseño de nuestros programas.

### Currificación
Definiremos currificación (_currying_) como la **conversión de una función con _n_ argumentos en _n_ funciones con un único argumento**, de forma que se devuelve una función con aplicación parcial de un argumento en cada caso.

`f(x, y, z) -> f(x)(y)(z)`

Entonces, la función f(x) devuelve en realidad una función nueva con el argumento _x_ aplicado y espera como argumento a _y_. Esta última función devuelve una nueva función con _y_ aplicado y devuelve otra función que espera como argumento a _z_ y devuelve el valor final de _f(x, y ,z)_.

> La **aplicación parcial** de una función se produce cuando pasamos menos argumentos de los necesarios para evaluarla, por lo cual **se devuelve otra función con los argumentos pasados aplicados y aceptando los argumentos restantes**.

Esto nos provee algunos beneficios:
- Construir funciones generalizadas que sean más fáciles de reutilizar.
- Generar de funciones específicas a partir de funciones generalizadas con algunos parámetros predefinidos.
- Facilita la composición de funciones. 
- Facilita el razonamiento usando funciones parcialmente aplicadas.

Veamos un ejemplo:

```python
# Función simple de suma
def suma(x, y):
    return x + y

# Función currificada de suma
def suma_curry(x):
    def suma_x(y):
        return x + y
    return suma_x

print(suma(1, 3))
print(suma_curry(1)(3))
```
La operación `suma_curry` ahora puede producir el mismo resultado mediante la invocación sucesiva con los mismos argumentos. En este caso, `suma_curry(1)` es una aplicación parcial que devuelve la función `f(y) = 1 + y` porque _x_ ya fue aplicado con `suma_x`. Otra opción más simple sería devolver directamente una expresión _lambda_.
```python
def suma_curry(x):
    return lambda y: x + y
```
> Una **expresión _lambda_** en python es simplemente una función sin nombre o anónima que se define en el momento. La sintaxis es: `lambda <lista_parámetros>: <expresión>`.
> El valor de una expresión _lambda_ es una **función** que puede ser invocada, similar a cómo se la define con el operador `def`.

También podríamos haber aprovechado la aplicación parcial para definir nuevas funciones.

```python
def doble(x):
    return suma_curry(x)(x)

def incrementar_10(x):
    return suma_curry(10)(x)
```
Es interesante la posibilidad que nos plantea esta técnica de escribir funciones, permitiendo modularizar y simplificar nuestra funcionalidad para mejorar la reutilización y pruebas del software.

Si deseamos _currificar_ una función deberíamos generar tantos niveles de anidado como parámetros tiene la función original.
```python
def suma_xyz(x):
    def suma_x(y):
        def suma_y(z):
            return x + y + z
        return suma_y
    return suma_x

suma_xyz(1)(2)(3)
```

#### functools.partial
En python disponemos de la función [partial](https://docs.python.org/3/library/functools.html#functools.partial) del módulo _functools_ que nos permite realizar la vinculación de la **aplicación parcial** a otra función. Por lo cual puede resultar en una herramienta útil en lugar de _currificar_ nuestras funciones.

```python
from functools import partial

def producto(x: int, y: int) -> int:
    return x * y

producto_10 = partial(producto, 10)
producto_10(2)
```
En este caso `producto_10` es una nueva función de aplicación parcial de la original que produce `partial`, donde espera un nuevo parámetro _y_ para devolver el resultado final.

#### pymonad.tools.curry
Existe otro paquete interesante en Python para aplicar enfoque funcional, en este caso podemos usar la función decoradora [`curry()`](https://pypi.org/project/PyMonad/#curried-functions) del módulo PyMonad para lograr el mismo objetivo de facilitar la currificación de una función. Simplemente le debemos indicar la cantidad de argumentos con la cual se currifica.

```python
from pymonad.tools import curry

@curry(2)
def producto(x: int, y: int) -> int:
    return x * y

producto_10 = producto(10)
producto_10(2)
```
También podríamos asignar la función currificada a una nueva variable sin utilizar el decorador.
```python
from pymonad.tools import curry

producto_curry = curry(2, producto)
```
Esta opción es interesante ya que nos permite currificar funciones nativas o importadas desde otros módulos existentes.

### Ejercicio: Registrando logs
A lo largo de nuestro programa es posible que necesitemos almacenar información de interés en el log de ejecución. A efectos prácticos, nuestro destino de log será la consola, por lo que podemos utilizar simplemente un `print()` para registrar un mensaje de log.

Implementar una función `log` _currificada_ que permita registrar un mensaje de log y el tipo, que puede ser _error_, _alerta_ o _información_.

### Composición con decoradores
Repasando la funcionalidad de un [decorador](../A_Python_POO/README.md#decoradores) en Python, podemos aprovecharlo para realizar la composición de funciones. Recordemos que una composición es la aplicación de una función sobre el resultado de otra función evaluada. En ese aspecto, un decorador puede cumplir con esa definición ya que básicamente realiza lo siguiente: `mi_funcion = decorador(mi_funcion)`.

> Es una opción útil para definir cierto comportamiento común aplicable a varias funciones, por lo cual podría justificarse eventualmente tener una librería de decoradores listos para reutilizar. Esto suele ser común para incorporar funcionalidad que es ajena a la función decorada, por ejemplo incorporar auditoría de ejecución, logging, controles de seguridad, etc. 

Veamos ahora un ejemplo sencillo, podríamos definir un decorador para limpiar los espacios al principio y final de una cadena.

```python
from collections.abc import Callable
from functools import wraps

def trim(f: Callable[[str], str]) -> Callable[[str], str]:
    @wraps(f)
    def wrapper(texto: str) -> str:
        return f(texto).strip()
    return wrapper

@trim
def transforma_texto(texto: str) -> str:
    return texto.replace('.',' ')

transforma_texto('  esto es una prueba. ')  # 'esto es una prueba'
```
El decorador `trim` adapta la función sobre la cual se aplica de forma que incorpora la eliminación de espacios en blanco de la cadena resultante. Entonces, la función `transforma_texto` queda decorada de forma que luego de evaluarse la definición original, se aplica la operación `strip()` sobre su resultado.

También podemos definir [parámetros en funciones decoradoras](../A_Python_POO/README.md#parametrizando-decoradores), logrando así una composición del estilo: `h = g(y) o f`, donde `y` sería un parámetro propio de la función decoradora. Por ejemplo, podríamos extender la versión previa de forma que reciba parámetros que determinen si deseamos eliminar sólo espacios en el inicio o el final de la cadena.

```python
from collections.abc import Callable
from functools import wraps

def trim(inicio: bool = True, fin: bool = True) -> Callable[[Callable[[str], str]], Callable[[str], str]]:
    def trim_deco(f: Callable[[str], str]) -> Callable[[str], str]:
        @wraps(f)
        def wrapper(texto: str) -> str:
            texto = f(texto)
            if inicio:
                texto = texto.lstrip()
            if fin:
                texto = texto.rstrip()
            return texto
        return wrapper
    return trim_deco
```
Ahora si aplicamos este nuevo decorador, debemos hacerlo con parámetros:
```python
@trim(inicio=False)
def transforma_texto(texto: str) -> str:
    return texto.replace('.',' ')

transforma_texto('  esto es una prueba. ')  # '  esto es una prueba'
```
```python
@trim(fin=False)
def transforma_texto(texto: str) -> str:
    return texto.replace('.',' ')

transforma_texto('  esto es una prueba. ')  # 'esto es una prueba  '
```

### Ejercicio: Decorando para _valores faltantes_
En ciertas situaciones veremos que una función no siempre puede devolver un valor como esperamos. Dependiendo de los argumentos recibidos, es posible que la función produzca algún error durante su evaluación o simplemente no encuentre un valor apropiado a devolver. En la programación funcional se suele utilizar la mónada _Maybe_ para resolver este problema, pero nosotros itentearemos una solución más sencilla.

Se pide implementar una función decoradora `acepta_no_valor` que permita adaptar una función con un único parámetro de cualquier tipo no nulo de forma que devuelva la evaluación de esa función si el argumento recibido no es `None`. De lo contrario, debe devolver `None`.

TIP: Se puede usar el _hint_ de tipo de retorno de la decoradora como: `Callable[[T | None], R | None]`. Ver [Generics](../B_Python_Type_Hints/README.md#generics).

## Iteraciones e iterables
En la programación imperativa trabajamos comúnmente con estructuras de control que permiten modelar una lógica repetitiva, estamos hablando de **bucles** como el `while`, `for`, `do`. Esto es posible gracias al registro de cierto estado del programa que verifica si la condición de corte del bucle se cumple o no, usualmente apoyándonos en variables que cambian de valor en cada iteración. Dado que en el paradigma funcional **no disponemos de este tipo de estructuras**, debemos modelar esta lógica a través de funciones puras y la [**recursión**](../02_recursion/README.md).

El concepto de recursión lo veremos en el siguiente módulo, pero veamos un ejemplo de cómo podríamos modelar la lógica de un **`for` con enfoque funcional**. Primero definamos una función con esta estructura que resuelva potencias de 2:
```python
def potencia2(n: int) -> int:
    retorno: int = 1
    for x in range(0, n):
        retorno *= 2
    return retorno

potencia2(11)   # 2048
```
Esta simple función permite calcular las potencias de 2 con exponente positivo utilizando un bucle y acumulando el resultado de cada iteración en la variable `retorno`. Veamos cómo podríamos resolver esto desde el paradigma funcional convirtiendo la estructura de iteración en una función pura.
```python
def iterar(veces: int, func: Callable[..., Any], valor: Any) -> Any:
    if veces <= 0:
        return valor
    else:
        return iterar(veces - 1, func, func(valor))
    
def potencia2(n: int) -> int:
    return iterar(n, lambda x: 2 * x, 1)

potencia2(11)   # 2048
```
En este caso estamos utilizando sólo funciones puras. La función `iterar` es recursiva y realiza la evaluación de la función recibida como argumento (`func`) aplicada al argumento `valor`. El resultado de dicha evaluación se pasa como nuevo valor de la próxima invocación de `iterar`, junto con el contador `veces` reducido en 1. Esto sucede hasta que se llega al caso base donde `veces <= 0`. La función aplicada es `lambda x: 2 * x`, donde `x` será el valor acumulado en cada _iteración_ (recursión), el cual se inicializa en `1`.

Dejaremos para más adelante el tema de recursión para resumir ahora algunas funciones que podemos utilizar para **trabajar con objetos iterables** desde un enfoque funcional en Python. En general cuando trabajamos con colecciones nos encontraremos con un conjunto de funciones comunes que pueden clasificarse en tres grupos:
- **Mapeos**: Construyen una **nueva colección** a partir de la original con la misma cantidad de elementos pero aplicando cierta **transformación**, por ejemplo la función `aplicar_operacion` que vimos en el [concepto de estado](#el-concepto-de-estado).
- **Filtrado**: Construyen una **nueva colección** a partir de la original pero con una cantidad reducida de elementos, ignorando aquellos que no cumplen cierto criterio.
- **Reducciones**: Producen un **valor** a partir de los elementos de una colección, por ejemplo `sum()`, `max()`, `len()`.

Esto no quiere decir que todas las operaciones sobre colecciones siempre son de este estilo. Por ejemplo la operación para ordenar una estructura no podría colocarse en ninguna clasificación previa, como así tampoco una operación que extienda la colección actual con nuevos elementos.

### map
En Python disponemos de la operación nativa [`map`](https://docs.python.org/3/library/functions.html#map) que recibe una función y al menos un objeto iterable, y **devuelve un iterador perezoso** (recordemos el `yield`) que entrega (a demanda) el resultado de aplicar esa función a cada elemento del iterable. Si se pasaran más de un iterable, entonces la función debe aceptar tantos argumentos como iterables ya que se apicaría a sus elementos.

```python
map(function, iterable, *iterables)
```
Dado que recibe a otra función como argumento, `map` es una **función de orden superior**.

Esta operación básicamente reemplaza el comportamiento de un bucle `for-each` sobre cierta colección iterable, donde se aplica cierta operación en cada elemento de la colección para construir una nueva.

```python
xs: list[int] = [1, 2, 3, 4]
ys: list[int] = []
operacion = lambda x: x * x
for x in xs:
    ys.append(operacion(x))
```
En este caso abstraemos la _operación_ a aplicar con una expresión lambda, pero podríamos haber definido una nueva función sin problemas. Lo importante es tener presente cuando se define es que el argumento recibido será un elemento de la colección.

```python
cuadrados: map = map(operacion, xs)    # <map at 0x1beb3187940>
list(cuadrados)     # [1, 4, 9, 16]
```
En este ejemplo podemos ver que el objeto retornado por `map` es un iterador perezoso (en realidad un objeto _map_), por lo cual no aplica la función a toda la colección `xs` inmediatamente, sino que lo hará cuando sea necesario. Justamente, recién cuando construimos una lista a partir de un iterador con el constructor `list()`, se itera sobre cada elemento para obtener su cuadrado.

Cuando utilizamos `map` con más de un iterable podemos tratar los elementos de cada uno de ellos en la operación, sólo debemos aceptarlos como parámetros en el orden que se pasan los iterables del `map`.

Veamos un ejemplo.
```python
totales: list[int] = [100, 200, 300]
registros: list[int] = [50, 40, 120]

proporciones = registros / totales    # TypeError: unsupported operand type(s) for /: 'list' and 'list'
```
Si queremos obtener la proporción de registros obtenidos a partir de un total, simplemente se realiza la división correspondiente. El problema es que no podemos extenderlo cuando tenemos varios registros y varios totales y deseamos aplicar esto a cada tupla de elementos.
```python
proporciones: map = map(lambda x, y: x / y, totales, registros)
list(proporciones)  # [2.0, 5.0, 2.5]
```
De esta forma con `map` podemos aplicar la operación que recibe dos argumentos (registros y total) para generar las proporciones deseadas.

Cuando aplicamos **`map` a listas** en Python, es recomendable utilizar [list comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) ya que facilitan la lectura de código:

```python
proporciones: list[float] = [x / y for x, y in zip(totales, registros)]
```
Recordemos que la operación `zip()` permite construir un **iterable de tuplas** que contienen los elementos de cada iterable en el orden que los recibe. Como última práctica veamos cómo podríamos implementar nuestro propio `zip()`, ya que es una operación de mapeo aplicada en varios iterables.

```python
from collections.abc import Iterable, Iterator
from typing import Any

def mi_zip(*iterables: Iterable[Any]) -> Iterator[tuple[Any, ...]]:
    return map(lambda *elementos: tuple(elementos), *iterables)

list(mi_zip([1,2,3], ['a','b','c']))    # [(1, 'a'), (2, 'b'), (3, 'c')]
```
El `*iterables` representa una lista de argumentos posicionales (recordar `*args`) y luego podemos pasar esta lista de parámetros como argumentos al `map` también utilizando el prefijo `*`. De la misma forma definimos la lista de parámetros para la expresión lambda con `*elementos` para luego consumirla en `tuple(elementos)`.

### Ejercicio: Contar letras
A través del uso del `map`, dada una lista de cadenas generar una nueva lista que devuelva la cantidad que tiene de cierta letra (pasada como argumento) cada elemento. Por ejemplo, si queremos contar la letra 'a' en ['casa', 'hogar', 'espacio', 'cuento'] deberíamos obtener [2, 1, 1, 0].

### filter
El filtrado de una colección consiste en aplicarle un predicado (función que devuevle un booleano) para generar una **nueva colección** que contiene sólo aquellos elementos de la original donde al aplicarles el predicado retorna _Verdadero_. En Python disponemos de la **función de orden superior** [`filter`](https://docs.python.org/3/library/functions.html#filter) que permite realizar la operación descripta.

Veamos un ejemplo de cómo podríamos filtrar una lista de números para obtener una lista con aquellos que son número par.
```python
def es_par(n: int) -> bool:
    return n % 2 == 0

xs = [1, 2, 3, 4, 5, 6]
ys = []
for x in xs:
    if es_par(x):
        ys.append(x)
```
El ejemplo simplemente recorre una lista de números agregando en una nueva `ys` aquellos que cumplen con la condición de `es_par()`. A continuación se reemplaza la iteración imperativa por una versión funcional con `filter`.

```python
filter(es_par, xs)  # <filter at 0x1d2af1aed70>
list(filter(es_par, xs))    # [2, 4, 6]
```
La función `filter` retorna también un **iterador perezoso**, un objeto _filter_, el cual retorna el valor del próximo elemento que cumple con el predicado (`es_par(<elemento>)` igual a `True`) cuando se lo requiere.

> Si bien hablamos de una función predicado para realizar el filtrado, en Python se puede utilizar el valor booleano de otros objetos para determinar si corresponde filtrar o no. Esto significa que la función podría devolver algún otro tipo de dato que no sea `bool` y luego Python analiza si el valor booleano es verdadero o falso. Por ejemplo, en Python el número 0, una lista vacía, una cadena vacía, son considerados `False` al evaluar su representación booleana.

Analicemos otro ejemplo integrando otros de los conceptos funcionales que vimos hasta ahora. Imaginemos que necesitamos obtener una lista con los _outliers_ de una muestra, es decir aquellos elementos que son significativamente distintos al resto de las observaciones. Para nuestro caso utilizaremos la técnica de detección mediante el cálculo de [Z-score](https://es.wikipedia.org/wiki/Unidad_tipificada) de cada observación y marcando aquellas que superan 3 desvíos de la media.

```python
import numpy as np
from pymonad.tools import curry
from pymonad.reader import Compose

@curry(3)
def zscore(media: float, desvio: float, valor: float) -> float:
    return (valor - media) / desvio

def es_outlier(z_score: float, limite :float = 3) -> bool:
    return z_score > limite or z_score < (limite * -1)

# Generamos muestra random
muestra = np.random.normal(0, 5, 1000)
# Aplicamos parcialmente argumentos a zscore
zscore_muestra = zscore(muestra.mean(), muestra.std())
# Generamos nueva función predicado mediante la composición
filtro_outlier = Compose(zscore_muestra).then(es_outlier)

list(filter(filtro_outlier, muestra))   # lista con outliers
```
Debido a que el cálculo de _z-score_ de una observación se basa en la media y desvío estándar de la muestra (`(x - media) / desvio std`), podemos **currificar** la función que lo obtiene generando una nueva función `zscore_muestra` con esos argumentos ya aplicados, lo cual produce una función de cálculo de _z-score_ propio de la muestra particular. Esta operación no es de tipo predicado, necesitamos aplicar luego una operación que determine si ese valor _z-score_ corresponde a un _outlier_ o no. Dado que la operación `filter` requiere una función que se aplica a cada elemento, necesitamos crear una función nueva llamada `filtro_outlier` componiendo `zscore_muestra` y `es_outlier`. Entonces tendremos lo siguiente: `filtro_outlier = es_outlier(zscore_muestra(<elemento>))`, lo cual es válido para utilizar como función predicado para el filtrado.

> Al igual que vimos con `map`, en Python se recomienda utilizar el filtrado de colecciones a través de [expresiones generadoras](#evaluación-perezosa).

El siguiente ejemplo produce el mismo resultado que el código previo utilizando una expresión generadora.
```python
[ x for x in muestra if es_outlier(zscore_muestra(x)) ]
```
También podríamos haber utilizado `filtro_outlier`, pero en este caso ya no es necesario porque podemos aplicar `zscore_muestra` a cada elemento en la condición de la expresión.

### reduce
La operación [`reduce`](https://docs.python.org/3/library/functools.html#functools.reduce) representa el concepto funcional denominado [fold](https://en.wikipedia.org/wiki/Fold_(higher-order_function)), donde **se produce un valor** a partir de la aplicación de una **función acumuladora/combinadora/reductora** sobre una estructura iterable. Ya hemos visto algo al respecto con [Streams de Java](https://github.com/mapreu/algoritmos1/blob/main/11_interfaces_funcionales/README.md#reducci%C3%B3n).

> En esta sección nos referimos por el mismo nombre a función reductora, acumuladora o combinadora. A su vez también nos referimos a lo mismo con valor reducido, acumulado o combinado.

La idea de esta operación se resume en estos pasos:

0. Obtener un valor inicial que será valor acumulado/reducido.
1. Si el iterable no tiene elementos por iterar, devolver valor acumulado, sino avanzar al paso siguiente.
2. Aplicar una función reductora sobre el valor acumulado y el elemento actual del iterable.
3. Repetir el paso 1 usando el retorno del paso 2 como nuevo valor acumulado.

> La **función reductora** recibe como argumentos al **valor acumulado** y al **elemento actual** del iterable.

Veamos un ejemplo sencillo:
```python
from functools import reduce

def contar_letras(acumulado: int, elemento: str) -> int:
    return acumulado + len(elemento)

reduce(contar_letras, ['casa', 'puente', 'ojo'], 0)     # 13
```
En este caso nuestra **función reductora** es `contar_letras` que recibe como primer argumento la cantidad de letras contadas hasta el momento y como segundo argumento una palabra. El **iterable** es una lista de cadenas y el **valor inicial** es `0`. El primer paso es asignar al 0 como valor reducido para invocar luego la función `contar_letras(0, 'casa')`. El resultado de esa invocación es `4` y se asigna como valor reducido. Luego se invoca nuevamente la función `contar_letras(4, 'puente')` y así sucesivamente como la siguiente secuencia:
```python
valor_reducido = 0
    contar_letras(0, 'casa')            # valor_reducido: 4
        contar_letras(4, 'puente')      # valor_reducido: 10
            contar_letras(10, 'ojo')    # valor_reducido: 13
```

Mencionamos algunos ejemplos de reducciones que ya vienen incorporados en algunas clases de colecciones de datos, como el `max()` o `sum()`, pero veamos cómo podríamos hacerlo a través de la función `reduce`.

```python
from functools import reduce

xs = [3, 4, 1, 0, 11, 7, 5, 6]

# sum(xs)
reduce(lambda x, y: x + y, xs, 0)   # 37

# max(xs)
reduce(lambda x, y: x if x > y else y, xs)  # 11
```
El caso de la suma puede que resulte más claro al principio, vamos acumulando la suma en el primer parámetro `x`. El caso del máximo puede resultar más confuso pero es el mismo concepto, vamos acumulando o guardando el elemento de mayor valor cuando comparamos de a dos elementos. Es análogo al siguiente bucle:
```python
maximo, *resto = xs
for x in resto:
    if x > maximo:
        maximo = x
```
El `*` que figura en la primera línea se refiere a la sintaxis de [desempaquetado de iterables en Python](https://peps.python.org/pep-3132/).

Observemos que la operación `reduce` está **sobrecargada** con un **parámetro opcional**. Podemos utilizarla con 2 o 3 argumentos. La versión que realiza la suma de elementos utiliza 3 argumentos: la función acumuladora que suma, la lista y el **valor inicial**. La segunda versión que realiza la obtención del máximo utiliza 2 argumentos, sólo la función acumuladora y la lista. En esta última, se asume como valor inicial al primer elemento de la lista `xs[0]`. 

Veamos la firma de `reduce` según la documentación.

```python
functools.reduce(function, iterable[, initializer])
```
Si omitimos el inicializador o valor inicial, se utiliza el **primer elemento del iterable**, pero **si está vacío se produce un error**.

Analicemos algo interesante sobre los tipos de datos de los argumentos de la función acumuladora. En ambos ejemplos vemos que la expresión lambda acumuladora acepta 2 argumentos de tipo `int` para producir uno nuevo también de tipo `int`. Lo importante aquí es comprender que el primer argumento `x` corresponde al **valor acumulado** de la reducción, mientras que el argumento `y` es el **elemento actual** de la iteración. Esto se visualiza mejor con el código análogo que se muestra en la documentación:

```python
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value
```
Por lo tanto, no siempre tendremos el **mismo tipo de dato para ambos argumentos** de la función combinadora o reductora, sino que el primer parámetro puede ser de otro tipo, pero siempre **debe coincidir con el tipo de dato de retorno**, porque el retorno de un paso previo es el valor del primer argumento de la próxima invocación.

> El módulo [`operator`](https://docs.python.org/3/library/operator.html) ofrece un conjunto de funciones que pueden resultar útiles para usar en funciones de orden superior como las que vimos en esta sección.

> El módulo [`itertools`](https://docs.python.org/3/library/itertools.html) contiene un conjunto de funciones útiles para construir **iteradores** que permiten mejorar la eficiencia de las iteraciones.

### Ejercicio: Conteo de elementos
Definir utilizando `reduce` una operación que dada una lista de cadenas devuelva un diccionario donde las claves sean cada elemento de la lista y los valores sean la cantidad de apariciones que tiene ese elemento en la lista.

Ejemplo: `contar(['a', 'b', 'c', 'a', 'a', 'c', 'b', 'd', 'c', 'a', 'e'])` -> `{'a': 4, 'b': 2, 'c': 3, 'd': 1, 'e': 1}`.

### Ejercicio: Ordenar con reduce
Utilizando la operación `reduce` definir una operación que ordene una lista de números enteros de menor a mayor.

> **Lectura de interés**: 
> - _Functional Python Programming, 3rd ed, Steven F. Lott_
>   - Chapter 1: Understanding Functional Programming
>   - Chapter 2: Introducing Essential Functional Concepts
>   - Chapter 3: Functions, Iterators, and Generators
>   - Chapter 5: Higher-Order Functions
>   - Chapter 7: Complex Stateless Objects
>   - Chapter 12: Decorator Design Techniques
>   - Chapter 13: The PyMonad Library
> - [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
> - [Python Style Guide](https://www.python.org/doc/essays/styleguide/)
