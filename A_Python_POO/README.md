# POO en Python
Esta sección provee una introducción básica sobre ciertos aspectos del lenguaje referidos al **paradigma orientado a objetos** que hemos visto en [Algoritmos 1](https://github.com/mapreu/algoritmos1/tree/main/01_introduccion#conceptos-b%C3%A1sicos-de-la-programaci%C3%B3n-orientada-a-objetos-poo).

## Convención de nombres
En primer lugar, siempre es útil recordar que cada lenguaje tiene una convención de estilos para definir nombres de variables, clases, constantes, etc. En Python podemos consultar la [guía de estilos](https://peps.python.org/pep-0008/).

Recordemos estilos comunes y en qué casos se aplican para Python.

| Estilo | Descripción | Usado para | Ejemplos |
|---|---|---|---|
| Snake Case | Palabras en minúsculas separadas por guión bajo. | variables, funciones, parámetros, módulos | mi_variable, calcular_costo() |
| Pascal Case | Palabras con primera letra en mayúscula sin separación. | clases, variables de tipo, excepciones | MiClase, Colegio, LogEnDisco |
| Mayúsculas con guión | Palabras en mayúsculas separadas con guión bajo. | constantes | LONGITUD_LISTA, CANTIDAD_NROS |

## Objetos
En Python las variables **no tienen asociado un tipo de dato**, es un lenguaje de **tipado dinámico**, conocido comúnmente como _ducktyping_. Gracias al uso de [_type hints_](../B_Python_Type_Hints/README.md) de tipo en nuestro código, podemos utilizar librerías no nativas que permiten hacer una verificación de tipos, similar a un type checker de un lenguaje tipado como Java. De todas formas, esta verificación no es parte del lenguaje y por lo tanto no es forzada por el mismo.

Como consecuencia, **una variable en Python es simplemente una etiqueta a una referencia** en memoria. Esta referencia en memoria es básicamente la **dirección donde se aloja una instancia u objeto**. Por tal motivo una variable no tiene asociado un tipo de dato, esa información **está asociada al objeto en memoria**.

> Recordemos que en Python **todo es un objeto**: clases, instancias de clases, funciones, módulos...

Cuando se genera una variable a través de la asignación `=`, estamos asociando esta etiqueta (nombre de la variable) al objeto asignado. A partir de ese momento, podemos acceder al objeto en memoria a través de esta etiqueta que lo referencia en nuestro código. Si la variable luego se asigna a otro nuevo objeto y no quedan variables que referencien al objeto previo, el [recolector de basura](https://docs.python.org/3/glossary.html#term-garbage-collection) se encargará de liberar de la memoria a ese objeto.

```python
nombre = 'Emma'
nombre2 = nombre
id(nombre)          # 2365055303536
id(nombre2)         # 2365055303536
```
Notemos que ambas variables `nombre` y `nombre2` referencian al mismo objeto en memoria, son un simple _alias_ al mismo objeto que puede accederse desde cualquiera de las dos.

### Identidad de Objetos
Similar a otros lenguajes, cada objeto tiene asociado un identificador de identidad que es exclusivo y lo distingue del resto de los objetos. Dependiendo de la implementación de Python, este identificador suele ser la **dirección de memoria** donde vive el objeto. Podemos consultarlo con la operación [`id()`](https://docs.python.org/3/library/functions.html#id).

```python
id(33)                      # 140721232205608
id('Esto es una cadena')    # 2365055278640
x = 5.5
id(x)                       # 2365048316752
```
**La identidad de un objeto no puede cambiar luego de ser instanciado.**

### Tipo de datos
El tipo de un objeto se desprende de la **clase** desde la cual se instancia y define qué operaciones podemos realizar sobre este objeto, por lo cual provee [encapsulamiento](https://github.com/mapreu/algoritmos1/blob/main/01_introduccion/README.md#conceptos-b%C3%A1sicos-de-la-programaci%C3%B3n-orientada-a-objetos-poo). Podemos consultarlo con la operación [`type()`](https://docs.python.org/3/library/functions.html#type).

```python
type('Esto es una cadena')  # <class 'str'>
type(33)                    # <class 'int'>
type([1,2])                 # <class 'list'>
type(len)                   # <class 'builtin_function_or_method'>
```
El valor devuelto por la operación `type()` corresponde al atributo especial [`__class__`](https://docs.python.org/3/library/stdtypes.html#instance.__class__).

```python
'Esto es una cadena'.__class__  # <class 'str'>
```
A diferencia de la identidad de un objeto, el atributo `__class__` podría ser modificado manualmente en tiempo de ejecución, pero **no es recomendable** hacerlo.

## Clases
En Python, al igual que en otros lenguajes OO, las clases son una manera de organizar y estructurar nuestro código. Permiten definir un conjunto de atributos y métodos que describen las características y el comportamiento de un objeto en particular. La sintaxis para definir una clase en Python es la siguiente:

```python
class NombreClase:
    # Definición de atributos y métodos de la clase
```

### Instanciación vs inicialización
La instanciación es el proceso de **crear un objeto** a partir de una clase. Cuando se **instancia** una clase, se reserva espacio en la memoria para el objeto **con el método especial `__new__()`**, el cual retorna una instancia de esa clase y luego **se inicializa el objeto utilizando el método especial `__init__()`**.  Podemos decir que ambos métodos conforman el **constructor de la clase**.

Veamos un ejemplo de definición de una clase junto con su constructor.

```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
```
El método inicializador `__init__()` recibe como primer argumento la instancia (**por convención se lo nombra siempre `self`**), y luego recibe los argumentos necesarios para inicializar el objeto. Los atributos `self.nombre` y `self.edad` son propios de esa instancia.

Para instanciar un objeto de la clase que definimos anteriormente, simplemente llamamos al nombre de la clase seguido de paréntesis y los argumentos definidos en el `__init__()`:
```python
juana = Persona("Juana", 23)    
print(juana)                    # <__main__.Persona at 0x1d2bd5b1750>
print(hex(id(a_mayusculas)))    # 1d2bd5b1750
print(juana.nombre)             # Juana
print(juana.edad)               # 23
```
El objeto `juana` se inicializa con sus atributos a través del constructor. Veamos que si imprimimos el valor de un objeto, por ejemplo con `print(juana)`, nos indica que de qué clase se instanció (`Persona`) y su **dirección de memoria** en valor hexadecimal. Esto se produce debido a que se invoca el método especial [`__repr__()`](#__repr__) heredado de object.

> En Python, las clases son _invocables_ por defecto, por lo cual al ejecutar un objeto de tipo clase se invoca el método especial `__new__(cls[, ...])` que devuelve una instancia de esa clase (primer argumento), que luego invoca su método `__init__()` para inicializarla utilizando los argumentos opcionales de `__new__()`.

### Miembros de instancia y miembros de clase
Recordemos que los [miembros de una clase](https://github.com/mapreu/algoritmos1/tree/main/01_introduccion#miembros-de-clase-vs-instancia) pueden ser de dos tipos: miembros de clase y miembros de instancia.

#### Atributos

Los **atributos de clase** son compartidos por todas las instancias de la clase. Estos miembros **se definen fuera de cualquier método de la clase y se accede a ellos utilizando el nombre de la clase**. Se pueden utilizar para almacenar datos que son comunes a todas las instancias de la clase.

Los **atributos de instancia** son específicos de cada objeto individual y **se definen dentro del método `__init__()` utilizando el parámetro self**. Cada instancia de la clase tiene sus propias copias de los atributos de instancia.

```python
class Persona:
    contador_personas = 0

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        Persona.contador_personas += 1

juana = Persona("Juana", 23)
hugo = Persona("Hugo", 33)

juana.nombre                # 'Juana
hugo.edad                   # 33
Persona.contador_personas   # 2
juana.contador_personas     # 2
hugo.contador_personas      # 2
```
En este ejemplo `contador_personas` es un **miembro de clase** que se utiliza para llevar la cuenta de cuántas instancias de la clase Persona se generaron, mientras que nombre y edad son **miembros de instancia** ya que se definieron con `self`. Para acceder a miembros se utiliza el punto `.` (_dot notation_).

#### Métodos
Así como podemos definir atributos de clase o instancia, también podemos aplicar el mismo criterio para los métodos. Las funciones definidas dentro de una clase son **métodos de instancia** y tienen la particularidad que **el primer parámetro siempre es la instancia actual**.

> Por convención, en Python utilizamos el nombre `self` para el parámetro de la instancia actual.

```python
class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'

juana = Persona("Juana", "Lopez")
juana.nombre_completo()             # 'Juana Lopez'
```
El método `nombre_completo` es un **método de instancia** ya que consume o accede a atributos de instancia.

Cuando deseamos modelar un comportamiento propio de una clase y no de una instancia, podemos definir un [método de clase](https://docs.python.org/3/howto/descriptor.html#class-methods). Estos métodos **sólo pueden acceder a atributos de clase**, ya que el primer parámetro es necesariamente la clase. Por convención se nombra a ese parámetro como `cls` y para definirlo se utiliza el [decorador](#decoradores) `@classmethod`.

```python
class Persona:
    contador_personas = 0

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        Persona.contador_personas += 1

    @classmethod
    def personas_creadas(cls):
        return cls.contador_personas

juana = Persona("Juana", "Lopez")
Persona.personas_creadas()          # 1
juana.personas_creadas()            # 1
```
EL método `personas_creadas()` es un método de clase, recibe como primer argumento a la clase `Persona` para poder acceder a sus miembros. Recordando que **una instancia puede acceder a miembros de instancia y miembros de clase**, podemos acceder a este método mediante `Persona.personas_creadas()` o `juana.personas_creadas()`.

> En situaciones donde no necesitamos acceder a miembros de clase ni de instancia, en Python existe lo que se denomina [método estático](https://docs.python.org/3/howto/descriptor.html#static-methods), que no debe confundirse con el método de clase como sucede en Java. **Un método estático no puede acceder a ningún tipo de miembro**.

Para definir un método estático utilizamos el decorador `@staticmethod`.

```python
class Persona:
    # Implementación de Persona...

    @staticmethod
    def a_minusculas(cadena):
        return cadena.lower()

Persona.a_minusculas('Probando Método Estático')  # 'probando método estático'
```
Notemos que, al igual que con los métodos de clase, no es necesario instanciar un objeto de tipo `Persona` para invocar a un método estático. Simplemente se lo llama con los argumentos correspondientes. Estos métodos **son buenos candidatos para modelar comportamiento de ayuda** (_helpers_).

### Métodos especiales
En Python existen [métodos especiales](https://docs.python.org/3/reference/datamodel.html#specialnames) que son invocados implícitamente para ejecutar cierta operación sobre un tipo de dato. Estos métodos tienen una particularidad respecto a su nombre: **comienzan y terminan con doble guión bajo `__`**. Así podemos definir un comportamiento diferente para nuestras clases respecto a los operadores del lenguaje, de alguna forma logrando **sobrecarga de operadores**. También se los conoce como métodos **dunder** o **mágicos**.

Veamos algunos métodos especiales que resultan interesantes:
#### `__new__`
El método [`object.__new__(cls[, ...])`](https://docs.python.org/3/reference/datamodel.html#object.__new__) crea una nueva instancia de la clase que recibe como primer argumento. Es necesariamente un método estático. Los argumentos restantes se pasan al inicializador de la clase (`__init__()`) junto con la instancia creada como primer argumento. Retorna la instancia creada.
> Es muy poco frecuente sobreescribir este método en la práctica.

#### `__init__`
El método [`object.__init__(self[, ...])`](https://docs.python.org/3/reference/datamodel.html#object.__init__) es invocado luego de la creación de la instancia realizada en `__new__()` y ambos actúan como **constructor** de la clase.
> Si definimos un método `__init__()` en una clase que hereda de otra que tiene definido su propio `__init__()`, debemos invocarlo explícitamente con `super().__init__()` con los argumentos necesarios.

#### `__repr__`
El método [`object.__repr__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__repr__) actúa como la **representación _formal_** del objeto. **Devuelve una cadena** que debería representar el estado del objeto, de forma que provea información completa para poder recrearlo. Se invoca también si no está definido el método `__str__()`.

```python
class Persona:
    # resto de la implementación de Persona...
    
    def __repr__(self):
        return f'{self.__class__.__name__}("{self.nombre}","{self.edad}")'

juana = Persona("juana", 23)    # Persona("juana","23")
```

#### `__str__`
El método [`object.__str__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__str__) actúa como la **representación _informal_** del objeto. Similar al `__repr__()`, **devuelve una cadena** que representa el estado de forma _amigable_. Es utilizado cuando se utiliza al objeto como argumento en las funciones [`format()`](https://docs.python.org/3/library/functions.html#format) y [`print()`](https://docs.python.org/3/library/functions.html#print).

```python
class Persona:
    # resto de la implementación de Persona...
    
    def __str__(self):
        return f'Nombre: {self.nombre}, Edad: {self.edad} años'

juana = Persona("juana", 23)    # Nombre: juana, Edad: 23 años
```

#### `__eq__`
El método [`object.__eq__(self, other)`](https://docs.python.org/3/reference/datamodel.html#object.__eq__) define la **comparación de igualdad** entre objetos. Es invocado cuando se utiliza el operador **`==`**.

En el ejemplo previo de `Persona`, si realizamos esta comparación veremos que utilizamos el `__eq__()` definido en `object`, el cual sólo verifica si ambos son la misma instancia.

```python
juana = Persona("juana", 23)
juana2 = Persona("juana", 23)
juana == juana2     # False
```
Ahora implementamos nuestro propio comparador de igualdad sobreescribiendo `__eq__()`.
```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def __eq__(self, otro):
        return isinstance(otro, Persona) and self.nombre == otro.nombre and self.edad == otro.edad
juana = Persona("juana", 23)
juana2 = Persona("juana", 23)

juana == juana2     # True
```

#### `__hash__`
El método [`object.__hash__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__hash__) es invocado cuando pasamos como argumento a un objeto en la función [`hash()`](https://docs.python.org/3/library/functions.html#hash). Retorna un **número entero** que identifica al objeto y es utilizado en estructuras indexadas. Similar al contrato del método [`hashCode()` de Java](https://github.com/mapreu/algoritmos1/tree/main/04_igualdad_orden_copia#el-m%C3%A9todo-hashcode), si definimos nuestro propio comparador de igualdad sobreescribiendo `__eq__()`, debemos también definir el método `__hash__()` de forma que si dos objetos son iguales, deben tener retornar el mismo número _hash_.

Así como definimos el `__eq__()` en ejemplo previo, debemos también asegurarnos que implementamos correctamente el `__hash__()`. La documentación oficial recomienda **devolver el valor _hash_ de la tupla con los atributos utilizados en el `__eq__()`**.
```python
def __eq__(self, otro):
    return isinstance(otro, Persona) and self.nombre == otro.nombre and self.edad == otro.edad
def __hash__(self):
    return hash((self.nombre, self.edad))
```
Dado que definimos la igualdad de `Persona` basada en el valor de los atributos `nombre` y `edad`, también nos apoyamos en el valor _hash_ de la tupla que contiene dichos atributos.

#### `__bool__`
El método [`object.__bool__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__bool__) se invoca cuando se utiliza la instancia en una expresión booleana, representa el _valor de verdad_ del objeto. Debe devolver `True` o `False`. Si no se define, se invoca al método `__len__()` y devuelve `True` si es distinto de `0`. Si tampoco tiene definido ese método, todas las instancias devuelven `True`.

```python
juana = Persona("juana", 23)

bool(juana) # True
if juana:
    print(juana)    # <__main__.Persona object at 0x000001D2BD60FAD0>
```
Si sobreescribimos el método así:
```python
class Persona:
    # resto de la implementación de Persona...
    
    def __bool__(self):
        return False

juana = Persona("juana", 23)

bool(juana) # False
if not juana:
    print(juana)    # <__main__.Persona object at 0x000001D2BD60FAD0>
```

#### `__len__()`
El méodo [`object.__len__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__len__) **devuelve un número entero** indicando la **longitud del objeto**. Se suele implementar para **colecciones** y si devuelve el valor `0` se considera que es `False` en un contexto booleano. Es invocado cuando se solicita la longitud, por ejemplo con el comando `len()`.

```python
class MiContenedor:
    def __init__(self):
        self.elementos = []

    def __len__(self):
        return len(self.elementos)
    
contenedor = MiContenedor()
len(contenedor)     # 0
```

#### `__call__`
El método [`object.__call__(self[, args...])`](https://docs.python.org/3/reference/datamodel.html#object.__call__) es invocado **cuando se llama directamente a una instancia de objeto**. La idea es agregar un comportamiento general o por defecto a un objeto, sin la necesidad de especificar un método particular, de forma que lo convierte en un **objeto invocable** (_callable_). Esto se puede verificar mediante `callable(<objeto>)`.

Existen numerosos ejemplos de usos de este método en Python, podemos encontrarlo en: objetos de clase, objetos de funciones, objetos de métodos, objetos de expresiones lambda, etc. También es popular su uso en algunas librerías como [PyTorch](https://pytorch.org/). Toda instancia de una clase que tenga definido este método **se comporta como si fuera una función**.

```python
class FormateadorMayusculas:
    def __init__(self):
        self.texto = ''

    def __call__(self, texto: str) -> str:
        return texto.upper()
    
a_mayusculas = FormateadorMayusculas()
a_mayusculas('esto es una prueba')      # 'ESTO ES UNA PRUEBA'
```
La variable `a_mayusculas` tiene la referencia de una instancia de tipo `FormateadorMayusculas`, luego invocamos directamente la instancia (objeto) con un argumento, lo cual invoca al método `__call__()` definido en esa clase.

### Accesibilidad a miembros de clase
En Python recordemos que no disponemos de un mecanismo que nos permita modificar la visibilidad de los elementos de una clase, tal como teníamos en Java con los modificadores de acceso `private`, `protected`, etc. En general se distingue sólo entre miembros públicos y no públicos, estos últimos definidos usualmente mediante una [convención del nombre](https://www.python.org/dev/peps/pep-0008/#method-names-and-instance-variables).

> Un miembro de una clase con un nombre que comienza con `_`, se asume es **no público**. Si bien Python **no restringe el acceso desde afuera**, es una señal a quien consume la clase que **no debe accederlo directamente**.

Por otra parte, también existe otra forma de nombrar miembros no públicos mediante el prefijo de doble guión bajo `__`. En este caso, el intérprete modifica internamente el nombre del miembro anteponiendo como prefijo `_NombreClase`.

```python
class MiClase:
    def __init__(self):
        self.x = 1
        self._y = 2
        self.__z = 3

mi_objeto = MiClase()
print(dir(mi_objeto))           # ['_MiClase__z', ..., '_y', 'x']
print(mi_objeto.x)              # 1
print(mi_objeto._y)             # 2
print(mi_objeto._MiClase__z)    # 3
mi_objeto._MiClase__z = 9
print(mi_objeto._MiClase__z)    # 9
```
Similar al caso de nombres con prefijo `_`, cuando definimos nombres con prefijo `__` podríamos accederlos si quisiéramos, aunque no sería posible accederlo como al resto con `mi_objeto.__z` porque es renombrado por el intérprete. La función [`dir()`](https://docs.python.org/3/library/functions.html#dir) nos permite visualizar los miembros válidos del objeto, donde aparecen todos los atributos definidos. Incluso podríamos modificar cualquiera de los atributos.

> El uso de [doble guión bajo como prefijo](https://peps.python.org/pep-0008/#method-names-and-instance-variables) debe utilizarse sólo cuando necesitemos evitar algún problema de conflicto de nombre en subclases, de lo contrario **es preferible utilizar la convención de un único guión bajo para atributos no públicos**.

#### Atributos -> Propiedades
Una alternativa interesante que ofrece Python para mejorar el encapsulamiento y consistencia de nuestras clases es a través de la conversión de los atributos en [_propiedades_](https://docs.python.org/3/library/functions.html#property). Esta funcionalidad que viene incorporada en el lenguaje permite definir [getters y setters](https://github.com/mapreu/algoritmos1/blob/main/01_introduccion/README.md#getters-y-setters) para operar con la estructura interna. Si bien no provee estrictamente ocultamiento de información porque estamos publicando en cierta forma nuestros atributos, es una opción válida para definir precisamente cómo accederlos o modificarlos.

Veamos un ejemplo utilizando `property()` como un [decorador](#decoradores):
```python
class Punto:
    def __init__(self, x: int | float, y: int | float) -> None:
        self._x: int | float = x
        self._y: int | float = y

    @property
    def x(self) -> int | float:
        return self._x

    @x.setter
    def x(self, valor: int | float) -> None:
        self._x = Punto._validar(valor)

    @property
    def y(self) -> int | float:
        return self._y

    @y.setter
    def y(self, valor: int | float) -> None:
        self._y = Punto._validar(valor)

    @staticmethod
    def _validar(valor: int | float) -> int | float:
        if not isinstance(valor, int | float):
            raise ValueError("Debe ser un número")
        return valor
    
p = Punto(3, 2)
p.x                 # 3
p.x = 11            # Invoca al setter de x
p.x                 # 11
p.x = 'a'           # ValueError: Debe ser un número
```
En nuestra clase decidimos _ocultar_ los atributos con la convención de nombre y luego los convertimos en propiedades para accederlos y modificarlos desde métodos. La conversión se realiza utilizando el decorador `@property` sobre un método con el mismo nombre del atributo que devuelve el valor, sería el _getter_. Luego es posible agregar otro método, también con mismo nombre que el atributo, que acepta como parámetro un valor para modificarlo y tiene un decorador `@<nombre_atributo>.setter`.

Entonces, la forma básica de definir _getters_ y _setters_ con `property()` sería así:

```python
# getter
@property
def nombre_atributo(self):
    return self._nombre_atributo

# setter
@nombre_atributo.setter
def nombre_atributo(self, valor):
    self._nombre_atributo = valor
```

Veamos que podemos agregar lógica tanto al momento de acceder un atributo como al momento de modificarlo, como resulta del ejemplo en los _setters_ de `Punto` que validan el nuevo valor. En ese caso decidimos utilizar un [método estático](#métodos) `_validar` dentro de la clase para unificar y reutilizar la lógica de validación.

> Podemos generar propiedades de sólo lectura si no definimos su método _setter_, de tal forma si deseamos modificarla obtendremos un error del tipo `AttributeError: property '<nombre_atributo>' of '<NombreClase>' object has no setter`.

> También podríamos generar propiedades de sólo escritura si definimos nuestro _getter_ de forma que devuelva una excepción: `raise AttributeError("x es un atributo de solo lectura")`, en lugar del valor del atributo.

## Herencia
El concepto de [herencia](https://github.com/mapreu/algoritmos1/tree/main/02_herencia) que hemos visto en Java, también puede aplicarse en Python. La herencia se realiza mediante la declaración de una clase derivada o **subclase** que hereda de una clase extendida o **superclase**. Entonces, la subclase hereda todos los atributos y métodos de la superclase. Veamos la sintaxis para Python.

```python
class Persona:
    pass
    
class Estudiante(Persona):
    pass

juana = Estudiante()
isinstance(juana, Estudiante)   # True
isinstance(juana, Persona)      # True
isinstance(juana, object)       # True
```
En este caso `Persona` es una superclase que implícitamente hereda de `object`, mientras que `Estudiante` es una subclase de ella. Un objeto de tipo `Estudiante` será entonces también de tipo `Persona` y de tipo `object`.

A diferencia de Java, en Python **podemos heredar de múltiples clases a la vez**, separando las superclases con comas.
```python
class UserCampus(Estudiante, Docente):  # Ejemplo de herencia múltiple
    pass
```

### Constructor heredado
Cuando extendemos una clase debemos tener presente los argumentos que recibe su método inicializador `__init__()`, ya que **si la superclase y subclase tienen un inicializador definido, debemos invocar al primero explícitamente en el inicializador de nuestra subclase**.

```python
class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
    
class Estudiante(Persona):
    def __init__(self, nombre, apellido, matricula):
        super().__init__(nombre, apellido)  # Invoca inicializador de Persona
        self.matricula = matricula

juana = Estudiante("Juana", "Lopez", 1234)
```
Para invocar un miembro de la superclase debemos accederlo con la referencia `super()`. En este caso, dado que `Persona` y `Estudiante` tienen inicializadores definidos, debemos invocar al inicializador de `Persona` desde el de `Estudiante`.

### Sobreescritura
**Una subclase hereda todos los miembros de la superclase**, por lo cual podemos invocar los métodos de la superclase como si fueran propios. En caso que necesitáramos **adaptar el comportamiento heredado** a una subclase, podemos hacer uso de la [sobreescritura](https://github.com/mapreu/algoritmos1/tree/main/02_herencia#sobreescritura) de métodos.

```python
class Persona:
    # Implementación de Persona...
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Estudiante(Persona):
    # Implementación de Estudiante...

    def __str__(self):
        return f'Estudiante {super().__str__()}'
    
juana = Estudiante("Juana", "Lopez", 1234)
print(juana)        # Estudiante Juana Lopez
```
En este ejemplo, `Estudiante` hereda el método `__str__()` de `Persona`, pero lo sobreescribe con su propia versión que casualmente invoca explícitamente el método heredado con `super().__str__()`.

Veamos un último ejemplo sencillo combinando los conceptos vistos.

```python
class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def mostrar_info(self):
        print(f'Vehículo: {self.marca} {self.modelo}')

    def acelerar(self):
        print('Acelerando')

    def frenar(self):
        print('Frenando')

class Auto(Vehiculo):
    def __init__(self, marca, modelo, color):
        super().__init__(marca, modelo)
        self.color = color

    def mostrar_info(self):
        super().mostrar_info()
        print(f'Color: {self.color}')

    def acelerar(self):
        print('Auto acelerando')

class Moto(Vehiculo):
    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self.cilindrada = cilindrada

    def mostrar_info(self):
        super().mostrar_info()
        print(f'Cilindrada: {self.cilindrada}')

    def frenar(self):
        print('Moto frenando')

class Bicicleta(Vehiculo):
    def __init__(self, marca, modelo, tipo):
        super().__init__(marca, modelo)
        self.tipo = tipo

    def mostrar_info(self):
        super().mostrar_info()
        print(f'Tipo: {self.tipo}')


auto = Auto("Toyota", "Corolla", "Rojo")
moto = Moto("Zanella", "ZT", "150cc")
bicicleta = Bicicleta("Vairo", "XR 3.5", "Montaña")

auto.mostrar_info()         # Vehículo: Toyota Corolla
                            # Color: Rojo
auto.acelerar()             # Auto acelerando
auto.frenar()               # Frenando

moto.mostrar_info()         # Vehículo: Zanella ZT
                            # Cilindrada: 150cc
moto.acelerar()             # Acelerando
moto.frenar()               # Moto frenando

bicicleta.mostrar_info()    # Vehículo: Vairo XR 3.5 
                            # Tipo: Montaña
bicicleta.frenar()          # Frenando
```
En este ejemplo definimos una clase base `Vehiculo` con ciertos atributos comunes como marca y modelo, junto con un comportamiento general. Luego las subclases sobreescriben parte del comportamiento heredado, por ejemplo `Auto` lo hace con su propio `mostrar_info()` y `acelerar()`, otorgando así [polimorfismo de inclusión o subtipo](https://github.com/mapreu/algoritmos1/blob/main/03_polimorfismo/README.md#herencia).

> Los miembros no públicos que se nombran con el prefijo [`__`](#accesibilidad-a-miembros-de-clase) son los únicos que **no son heredados** por subclases, ya que son renombrados internamente por Python.

### Clases abstractas
Recordando la definición de [clase abstracta](https://github.com/mapreu/algoritmos1/tree/main/05_interfaces_y_clases_abstractas#clases-abstractas) que vimos en Java, en Python podemos definir este tipo de clases a través del módulo [`abc`](https://docs.python.org/3/library/abc.html), llamadas **Abstract Base Classes**.

Para definir nuestra propia clase abstracta, simplemente debemos **heredar de la clase abc.ABC**.

```python
from abc import ABC

class MiClaseAbstracta(ABC):
    pass
```
Se debe tener en cuenta que en Python no tenemos un mecanismo por el cual evitar instanciar una clase abstracta, para forzar este comportamiento debemos agregar al menos un **método abstracto** utilizando el decorador `@abstractmethod`.

```python
from abc import ABC, abstractmethod

class Vehiculo(ABC):
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    @abstractmethod
    def mostrar_info(self):
        raise NotImplementedError

vehiculo = Vehiculo("Toyota", "Corolla")    # TypeError: Can't instantiate abstract class Vehiculo with abstract method mostrar_info
```
Si no definimos el método `mostrar_info()` como abstracto, entonces podríamos instanciar a `Vehiculo` a pesar de modelarla como una clase abstracta.

## Comparadores
En Python podemos definir el comportamiento de comparación entre objetos utilizando métodos especiales. Estos métodos nos permiten **sobrecargar los operadores de comparación**, como `==`, `!=`, `<`, `>`, `<=` y `>=`, para nuestros propios tipos de datos personalizados. Ya hemos visto el [comparador de igualdad](#__eq__), veamos los [restantes](https://docs.python.org/3/reference/datamodel.html#object.__lt__).

- `__ne__(self, other)`: Se invoca cuando se utiliza el operador de desigualdad (!=) para comparar dos objetos, por defecto utiliza `__eq__()` invirtiendo su valor retornado.
- `__lt__(self, other)`: Se invoca cuando se utiliza el operador menor que (<) para comparar dos objetos. Se puede apoyar en `__gt__()` invirtiendo su resultado.
- `__gt__(self, other)`: Se invoca cuando se utiliza el operador mayor que (>) para comparar dos objetos. Se puede apoyar en `__lt__()` invirtiendo su resultado.
- `__le__(self, other)`: Se invoca cuando se utiliza el operador menor o igual que (<=) para comparar dos objetos. Se puede apoyar en `__ge__()` invirtiendo su resultado.
- `__ge__(self, other)`: Se invoca cuando se utiliza el operador mayor o igual que (>=) para comparar dos objetos. Se puede apoyar en `__le__()` invirtiendo su resultado.

Supongamos que queremos crear una clase `Punto` que represente un punto en un plano cartesiano, y queremos que los puntos se puedan comparar entre sí en función de sus coordenadas x e y.

```python
class Punto:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __eq__(self, otro: "Punto"):
        return self.x == otro.x and self.y == otro.y

    def __lt__(self, otro: "Punto"):
        return self.x < otro.x or self.y < otro.y

    def __le__(self, otro: "Punto"):
        return self == otro or self.x < otro.x or self.y < otro.y
    
p1 = Punto(1, 3)
p2 = Punto(1, 4)

p1 == p2    # False
p1 != p2    # True
p1 > p2     # False
p1 < p2     # True
p1 <= p2    # True
p1 >= p2    # False
```
Vemos que nos podemos apoyar en sólo 3 métodos comparadores para sobrecargar los 6 operadores.

## Organización del código
Así como podemos organizar nuestro código en funciones o clases dentro de un archivo fuente, también podemos apoyarnos en **módulos** y **paquetes** para facilitar la organización. Comencemos por los primeros.

### Módulos
En Python, un archivo que contiene código fuente es sencillamente un **módulo**. Entonces, si un archivo se llama `mi_app.py`, podemos decir que es un módulo con nombre `mi_app`. Por lo tanto, si quisiéramos utilizar una clase definida dentro de ese archivo desde un segundo archivo (un segundo módulo), en ese último deberíamos importarla utilizando el nombre de módulo `mi_app`.

Veamos el ejemplo donde tenemos dos módulos: `modulo1` y `móoulo2`. En el primer módulo definimos `ClaseA` y `ClaseB`. En el segundo módulo definimos una función `funcion2`. Consideremos que ambos archivos `modulo1.py` y `modulo2.py` se encuentran en la misma carpeta en nuestro sistema operativo.

```python
# Archivo modulo2.py
from modulo1 import ClaseA

def funcion2():
    clasea = ClaseA()   # ok, importada desde modulo1
    claseb = ClaseB()   # error, no se importó desde modulo1
```
Analizando el contenido de `modulo2.py` vemos que podemos importar a través de la instrucción `import` las definicioes que se encuentran en otro módulo (archivo). En este caso particular, se utiliza una forma de importar más específica, donde solicitamos traer sólo la definición de `ClaseA` con la instrucción `from`. Lo interesante de esta opción es que podemos consumir lo importado sin agregar el prefijo del módulo como veremos a continuación.

```python
# Archivo modulo2.py
import modulo1

def funcion2():
    clasea = ClaseA()   # error, no reconoce ClaseA sin especificar el módulo
    clasea = modulo1.ClaseA()   # ok
    claseb = modulo1.ClaseB()   # ok
```
Ahora importamos directamente el módulo completo con todas sus definiciones, donde se crea el _namespace_ `modulo1`. La diferencia es que entonces debemos consumirlas con su nombre completo (_fully qualified name_) agregando el prefijo `<nombre_modulo>.` para indicar el _namespace_ del módulo desde donde se importan.

En el primer caso no era necesario utilizar el nombre completo porque se importaba `ClaseA` **directamente al _namespace_ del módulo actual**. Esta forma suele ser la **recomendada**, porque **reduce el acoplamiento innecesario entre módulos y documenta** en cierta forma qué es lo que realmente consumimos de otro lugar. Por otro lado, esto puede generar conflictos de nombres si hay definiciones con mismo nombre en el módulo donde se está importando, lo cual se puede resolver agregando un alias a lo importado así:

```python
# Archivo modulo2.py
from modulo1 import ClaseA as MiClaseA

def funcion2():
    clasea = MiClaseA()   # ok, importada desde modulo1 con otro nombre
```

> Al momento de importar un módulo, Python busca un archivo con el mismo nombre y extensión `.py` en el directorio local o en los directorios de paquetes instalados. Si no se encuentra, se produce error de importación.



## Funciones internas
Las funciones definidas dentro de otras funciones se conocen como **funciones internas o funciones anidadas**. Son aquellas que están definidas dentro del cuerpo de otra función. Estas funciones **tienen acceso al ámbito local de la función externa**, lo que significa que **pueden acceder a las variables locales y los parámetros de la función externa**. Las funciones internas pueden ser utilizadas para modularizar el código y encapsular la lógica que solo es relevante dentro del contexto de la función externa.

```python
def funcion_externa():
    def funcion_interna():
        return "Esta es una funcion interna."

    return funcion_interna()

print(funcion_externa())  # "Esta es una funcion interna."
print(funcion_interna())  # NameError: name 'funcion_interna' is not defined
```
En este ejemplo definimos una función llamada `funcion_externa()` que dentro de su implementación tiene definida otra función `funcion_interna()`, por lo cual esta última sólo existe en el ámbito local (_local scope_) de la primera. Es por ello que no podemos invocarla desde afuera directamente.

Veamos algunos beneficios en el uso de funciones internas.

### Funciones de ayuda (helpers)
En ciertos casos puede que nos encontremos escribiendo código repetido, lo cual viola el principio [DRY](https://es.wikipedia.org/wiki/No_te_repitas). Si bien podemos modularizar esa lógica en una **operación de ayuda**, si sólo se consume desde cierto lugar puede que sea conveniente modularizarla allí y evitar publicarla para acceder desde afuera. Sería una forma de modularizar dentro de lo modularizado, de forma que se mejore la interpretación y mantenimiento del código.

Si esta operación de ayuda se consume sólo desde cierta clase, se podría definir simplemente un método privado (posiblemente estático) que sea accedido sólo desde dentro de la clase. Si la operación de ayuda sólo se consumirá desde cierta función o método, entonces una buena opción es definirla como **función interna**.

```python
def calcular_medias(*args: list[int]) -> list[float]:
    def media(xs: list[int]) -> float:
        return sum(xs) / len(xs) if len(xs) > 0 else 0
    
    medias: list[float] = []
    for lista in args:
        medias.append(media(lista))
    
    return medias

calcular_medias([1,2,3], [4,5,6], [7,8,9,10,11])    # [2.0, 5.0, 9.0]
```
Al definir una función interna `media()` escribimos en un único lugar la lógica del cálculo de la media para ser utilizado dentro de la función externa y facilitamos la lectura y mantenibilidad.

### Encapsulamiento
Este concepto clave de la POO también puede aplicarse para combinar funcionalidad, otorgando así también el ocultamiento de cómo se resuelve internamente. Mediante el uso de funciones internas podemos encapsular funcionalidades dentro de una función externa. Esto es útil cuando deseamos **restringir el acceso de cierta función interna al ámbito de la función externa**. 

Claramente, el ejemplo previo provee encapsulamiento de la función `media()` dentro de `calcular_medias()`. Veamos otro caso.

```python
def procesar_datos(datos: list[str]) -> list[int]:
    def filtrar_negativos(numeros: list[int|None]) -> list[int]:
        return [num for num in numeros if num is not None and num >= 0]
    
    def limpiar_no_enteros(textos: list[str]) -> list[int|None]:
        return list(map(lambda x: int(x) if x.isdigit() else None, textos))
    
    filtrados = limpiar_no_enteros(datos)
    return filtrar_negativos(filtrados)

procesar_datos(['1', 'a', '2.4', '-3', 'x', '4', '9']) # [1, 4, 9]
```
Nuestra función `procesar_datos()` consume internamente funcionalidad parcial para producir el resultado, la cual se encapsula y modulariza en las operaciones `filtrar_negativos()` y `limpiar_no_enteros()`.

> Una desventaja de utilizar funciones internas es que probablemente reducen la cohesión de la función externa.

### Clausura
Una clausura o cerradura es la **combinación de una función con el ámbito en el que fue creada**, incluso después de que ese ámbito haya dejado de existir. Esto significa que una función interna aún puede acceder y hacer referencia a las variables locales y los parámetros de la función externa, incluso después de que la función externa haya terminado su ejecución.

> Una clausura nos permite acceder al ámbito desde el cual fue definida una función al momento de su creación.

Por el momento no nos preocuparemos en cómo se implementa internamente, ya que es dependiente de cada lenguaje. En Python nos encontramos con una clausura cuando **una función devuelve una instancia de una función interna**. Este objeto retornado no sólo tiene asociada la definición de la función interna, sino también el **ámbito con el cual fue creada**. Entonces, ahora la función retornada mantiene el estado del ámbito mencionado aún cuando ya finalizó la invocación de la función externa que la devuelve.

Veamos un ejemplo.

```python
def funcion_externa(parametro_externo):
    def funcion_interna(parametro_interno):
        return f'Parametro externo: {parametro_externo}, Parametro interno: {parametro_interno}'
    
    return funcion_interna

clausura = funcion_externa(1)
print(clausura(2))  # Parametro externo: 1, Parametro interno: 2
```
Notemos que cuando definimos `funcion_interna()` no le damos como parámetro el `parametro_externo`, sino que lo consume directamente como si fuera una variable global (en realidad es **nonlocal**). Esto es posible porque al momento de crearla Python retiene en la clausura el estado de ese ámbito local de `funcion_externa`. Entonces, cuando se crea con `clausura = funcion_externa(1)`, internamente se almacena el estado `parametro_externo=1` para que cuando se invoca `clausura(2)` se pueda evaluar.

> Un caso común donde se utiliza este concepto de clausura es en la [currificación](../01_paradigma_funcional/README.md#currificación).

Veamos otro ejemplo de clausura:
```python
def crear_contador():
    contador = 0
    
    def valor_actual():
        nonlocal contador
        return contador

    def incrementar():
        nonlocal contador
        contador += 1
        return contador
    
    def decrementar():
        nonlocal contador
        contador -= 1
        return contador

    return valor_actual, incrementar, decrementar

valor_actual, incrementar, decrementar = crear_contador()

print(valor_actual()) # 0
print(incrementar())  # 1
print(incrementar())  # 2
print(incrementar())  # 3
print(decrementar())  # 2
```
La palabra reservada [`nonlocal`](https://docs.python.org/3/reference/simple_stmts.html#grammar-token-python-grammar-nonlocal_stmt) permite identificar que esa variable accedida o modificada se refiere a la definida en el ámbito de la función externa más inmediata. El comportamiento es similar al de [`global`](https://docs.python.org/3/reference/simple_stmts.html#grammar-token-python-grammar-global_stmt), sólo que este último hace referencia al ámbito global del módulo.

Al momento de invocar `crear_contador()` se generan 3 clausuras. Lo interesante es que las 3 comparten el mismo ámbito no local, donde vive la referencia de `contador`. Estas clausuras retienen así el estado de ese ámbito aún cuando `crear_contador()` finalizó retornando la tupla de funciones.

> Veremos que el concepto de funciones internas es clave cuando definimos [decoradores](#decoradores).

## Decoradores
La idea de los [decoradores en Python](https://peps.python.org/pep-0318/) es **aplicar cierta transformación a una función** al momento de definirla, extender de alguna forma su funcionalidad. En principio puede parecer algo redundante ya que también podríamos extender la función con la transformación deseada en su propio cuerpo, pero veremos que es una herramienta poderosa para _adaptar_ la funcionalidad base de forma sencilla, sobre todo cuando la transformación es replicable no sólo a una sino varias funciones.

> Si bien existe un patrón de diseño denominado [_Decorator Pattern_](https://web.archive.org/web/20031204182047/http://patterndigest.com/patterns/Decorator.html), un decorador de python **no es** precisamente una implementación de este patrón. Comparten la idea de incorporar funcionalidad a algo previamente definido, pero el patrón lo hace dinámicamente en tiempo de ejecución.

Los decoradores son funciones que reciben otra función como argumento y retornan una nueva función con la transformación aplicada. Así es posible **incoporar funcionalidad antes y despúes** de la evaluación de la función pasada como argumento.

Imaginemos que necesitamos transformar cierta función sin modificar su cuerpo y con la posibilidad de reutilizar ese tipo de transformación para otras operaciones. Una opción sería hacer una nueva función decoradora y reasignar el identificador (variable) a una nueva función _decorada_. Sería algo así:
```python
def mi_funcion(texto: str) -> str:
    return texto

mi_funcion = decorador(mi_funcion)  # decorador sería la función decoradora
```
En Python podemos hacer eso mismo a través de la sintaxis de decoradores `@` que preceden la definición de la función.
```python
@decorador
def mi_funcion(texto: str) -> str:
    return texto
```
El decorador entonces transforma lo que era `mi_funcion` original en una nueva función extendida **en el momento de la defición**. Incluso podríamos agregar varios decoradores a una función, logrando así **múltiples transformaciones encadenadas**.

Veamos un ejemplo, si quisiéramos hacer un decorador que agregue un caracter '#' al principio y al final de una cadena, podríamos hacer lo siguiente:
```python
from collections.abc import Callable

def add_numerales(funcion_original: Callable[..., str]) -> Callable[..., str]:
    def add_numerales_inner(*args: Any, **kwargs: Any) -> str:
        return '#' + funcion_original(*args, **kwargs) + '#'
    return add_numerales_inner

@add_numerales
def concat_cadenas(c1: str, c2: str) -> str:
    return c1 + c2

concat_cadenas('abc', 'def')    # Salida: '#abcdef#'
```
Podemos notar que el resultado de invocar `concat_cadenas('abc', 'def')` es el mismo que si hubiéramos hecho `add_numerales(concat_cadenas)('abc', 'def')` sin usar `@add_numerales`. Esto es posible porque recordemos que **una función decoradora siempre devuelve una función**, que es la que _decora_ la función original. Se puede corroborar consultando el nombre real de la función así:
```python
print(concat_cadenas.__name__)  # Salida: add_numerales_inner
```
El atributo especial `__name__` nos dice que en realidad esa etiqueta `concat_cadenas` apunta ahora a un objeto de tipo función que es en realidad la función interna `add_numerales_inner`, porque esta función es la que transforma la original en nuestro decorador. Si quisiéramos preservar la información de la función original, debemos utilizar el decorador [`functools.wraps`](https://docs.python.org/library/functools.html#functools.wraps) en nuestra función interna. Nuestro decorador quedaría así:

```python
from functools import wraps

def add_numerales(funcion_original: Callable[..., str]) -> Callable[..., str]:
    @wraps(funcion_original)
    def add_numerales_inner(*args: Any, **kwargs: Any) -> str:
        return '#' + funcion_original(*args, **kwargs) + '#'
    return add_numerales_inner
```
De esta forma `concat_cadenas.__name__` mantiene el nombre `concat_cadenas` de la función original, como así también otra información como argumentos, tipos, etc.

> Suele ser recomendable utilizar siempre el decorador `functools.wraps()` para la función interna de un decorador.

Veamos otro ejemplo clásico, puede resultar útil medir el tiempo que tarda en ejecutarse una función, por lo cual podemos definir un decorador que incorpore esta funcionalidad.

```python
import time
from functools import wraps

def medir_tiempo(funcion: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(funcion)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        inicio: float = time.time()
        resultado: Any = funcion(*args, **kwargs)
        print(f'Tiempo de ejecución: {time.time() - inicio} segs')
        return resultado
    return wrapper

@medir_tiempo
def test():
    time.sleep(1)

test()      # Tiempo de ejecución: 1.0011136531829834 segs
```
Nuestro decorador `medir_tiempo` ahora agrega una impresión en consola con los segundos requeridos para ejecutar cualquier función donde se lo utilice.

### Parametrizando decoradores
Podemos incorporar parámetros a nuestras funciones decoradoras, el truco está en que ahora la función decoradora deberá devolver una nueva función decoradora que incorpore el o los argumentos recibidos. Por lo tanto, estamos agregando un nuevo nivel de abstracción que se evidencia como un nuevo nivel de función interna.

Veamos cómo podríamos extender el decorador previo para que le podamos indicar si deseamos registrar el tiempo de ejecución en nanosegundos en lugar de segundos.

```python
import time
from functools import wraps

def medir_tiempo(en_ns: bool = False) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def medir_tiempo_deco(funcion: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(funcion)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            inicio: float = time.time_ns() if en_ns else time.time()
            resultado: Any = funcion(*args, **kwargs)
            fin: float = time.time_ns() if en_ns else time.time()
            print(f'Tiempo de ejecución: {fin - inicio} {"ns" if en_ns else "segs"}')
            return resultado
        return wrapper
    
    return medir_tiempo_deco

@medir_tiempo(en_ns=True)
def test():
    time.sleep(1)

test()      # Tiempo de ejecución: 1000562400 ns
```
Notemos que ahora la función decoradora `medir_tiempo` devuelve una nueva función decoradora `medir_tiempo_deco` que es la que recibe como argumento `bool` si se desea generar el registro en segundos o nanosegundos. Es por eso que cuando la utilizamos, debemos **invocarla** para que genere la expresión de la función decoradora final y esa eventualmente se aplique como decoradora de la función `test()`. Esta invocación también se puede ver si queremos usar la versión decoradora por defecto que devuelve en segundos:
```python
@medir_tiempo()
def test():
    time.sleep(1)

test()      # Tiempo de ejecución: 1.0010230541229248 segs
```
Entonces, cuando decoramos a `test` con `@medir_tiempo()`, en realidad estamos decorándola con la función interna `medir_tiempo_deco` que tiene definido el parámetro `en_ns` en `False`, porque esa función es el retorno de la evaluación de `medir_tiempo()`.

Es importante que verifiquemos que el tipo de dato de retorno de una función decoradora con parámetros debe ser una función (`Callable`) que reciba como parámetro una función con los parámetros y retorno de la que vamos a decorar, y retorne la misma firma de esa función. Puede resultar confuso el uso de type hints en estos casos, pero suele ser útil para prevenir errores y comprender mejor cómo funcionan los decoradores.
```python
def asteriscos(p: int) -> Callable[[Callable[[float], str]], Callable[[float], str]]:
    def asteriscos_deco(f: Callable[[float], str]) -> Callable[[float], str]:
        def wrapper(x: float) -> str:
            return p * '*' + f(x) + p * '*'
        return wrapper
    return asteriscos_deco
```
En este ejemplo definimos un decorador para adaptar funciones con firma `float -> str` para incorporarles `*` repetidos al principio y final de la cadena resultante. La función decoradora `asteriscos` recibe un argumento de tipo `int` y devuelve una función decoradora `asteriscos_deco`, la cual acepta como argumento a una función a decorar (coincide con la firma de `wrapper`) y devuelve la misma firma de esa última. Veamos cómo se aplica:
```python
@asteriscos(3)
def float_to_str(x: float) -> str:
    return '{:.4f}'.format(x)

float_to_str(2.4)   # '***2.4000***'
```

## Excepciones
Las [excepciones](https://github.com/mapreu/algoritmos1/tree/main/07_excepciones) son **eventos que ocurren durante la ejecución de un programa que interrumpen el flujo normal de ejecución**. Python proporciona un mecanismo robusto para manejar excepciones, lo que nos permite detectar y responder a errores de manera elegante y controlada. Cuando se produce una excepción, se detiene el flujo normal de ejecución y Python busca un manejador de excepciones adecuado para procesarla.

Python proporciona una variedad de excepciones incorporadas que representan diferentes tipos de errores. Algunos ejemplos comunes de excepciones incluyen `TypeError`, `ValueError`, `ZeroDivisionError`, `IOError`, entre otros. Cada tipo de excepción está diseñado para manejar un tipo específico de error.

Similar a otros lenguajes, el manejo de excepciones se realiza utilizando bloques `try`, `except` y opcionalmente `finally`. La sintaxis básica es la siguiente:

```python
try:
    # Código que puede generar una excepción
    # ...
except ValueError as excep1:
    # Manejar excepción de tipo ValueError pasada en la variable excep1
    # ...
except TypeError as excep2:
    # Manejar excepción de tipo TypeError pasada en la variable excep2
    # ...
except:
    # Manejar cualquier otro tipo de excepción. Se debe evitar esta forma!
    # ...
else:
    # Se ejecuta si no se produce ninguna excepción en el bloque try
    # ...
finally:
    # Se ejecuta siempre, independientemente de si se produce una excepción o no
    # ...
```
El tratamiento o captura de excepciones se realiza con los bloques `try-except`, donde cada _manejador_ o _handler_ se define en cada `except`. Si el tipo de la excepción lanzada dentro del bloque `try` coincide con el tipo de excepción definida en un `except`, entonces se continúa la ejecución en el cuerpo de ese _handler_. Si existiera un bloque `finally`, se ejecutarían sus instrucciones y finalmente continúa la ejecución del programa.

### Lanzamiento de excepciones
El lanzamiento de una excepción se realiza mediante la instrucción [`raise`](https://docs.python.org/3/reference/simple_stmts.html#raise) seguida por la expresión de la excepción. Si se ignora la expresión, se relanza la excepción que se está manejando en el momento (excepción activa). Esto nos permite indicar que ha ocurrido un error en una determinada parte de nuestro código.

```python
def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError('No se puede dividir por cero')
    return a / b

try:
    resultado = dividir(10, 0)
except ZeroDivisionError as e:
    print('Error:', e)              # Error: No se puede dividir por cero
```
En este ejemplo, la función `dividir()` lanza una excepción `ZeroDivisionError` si el divisor es cero. Luego, en el bloque `except` capturamos y manejamos esa excepción, imprimiendo un mensaje de error informativo.

### Jerarquía de excepciones
En Python, todas las excepciones heredan de la clase [`BaseException`](https://docs.python.org/3/library/exceptions.html), la cual provee atributos donde se almacena información del contexto donde se lanzó la excepción.

> Si deseamos definir nuestras **propias excepciones**, debemos heredar explícitamente desde `BaseException` o alguna de sus subclases. En particular, **se recomienda heredar de la clase `Exception`**.




> **Lectura de interés**: 
> - [Python Documentation](https://docs.python.org/3/contents.html)
> - [Python Style Guide](https://www.python.org/doc/essays/styleguide/)
