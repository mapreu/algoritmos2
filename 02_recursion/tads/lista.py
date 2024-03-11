from typing import Generic, TypeVar, Optional
from copy import copy

T = TypeVar('T')

class Nodo(Generic[T]):
    def __init__(self, dato: T, sig: Optional["Lista"] = None):
        self.dato = dato
        if sig is None:
            self.sig= Lista()
        else:
            self.sig = sig

class Lista(Generic[T]):
    def __init__(self):
        self._head: Optional[Nodo] = None

    def es_vacia(self) -> bool:
        return self._head is None

    def head(self) -> T:
        if self.es_vacia():
            raise IndexError('lista vacia')
        else:
            return self._head.dato

    def tail(self) -> "Lista":
        if self.es_vacia():
            raise IndexError('lista vacia')
        else:
            return copy(self._head.sig)

    def insertar(self, dato: T):
        if self.es_vacia():
            self._head = Nodo(dato)
        else:
            actual = copy(self)
            self._head = Nodo(dato, actual)

    def eliminar(self, valor: T):
        if not self.es_vacia():
            if self.head() == valor:
                self._head = self._head.sig._head
            else:
                self._head.sig._eliminar_interna(self, valor)
    
    def _eliminar_interna(self, previo: "Lista", valor: T):
        if not self.es_vacia():
            if self.head() == valor:
                previo._head.sig = self._head.sig
            else:
                self._head.sig._eliminar_interna(self, valor)

    def ultimo(self) -> T:
        pass

    def concat(self, ys: "Lista") -> "Lista":
        pass
        
    def join(self, separador: str = '') -> str:
        pass
        
    def index(self, valor: T) -> int:
        pass
        
    def __repr__(self):
        pass
        

if __name__ == '__main__':
    xs: Lista[int] = Lista()
    
    print(f'xs es vacia? {xs.es_vacia()}')	# True
    
    # Operaciones basicas
    xs.insertar(4)
    xs.insertar(10)
    xs.insertar(20)
    ys = xs.tail()
    ys.insertar(9)
    ys.eliminar(10)
    ys.insertar(8)
    
    print(f'xs: {xs}')						# [20, 10, 4]
    print(f'ys: {ys}')						# [8, 9, 4]
    print(f'xs es vacia? {xs.es_vacia()}')	# False
    print(f'ultimo(xs): {xs.ultimo()}')		# 4
    print(f'len(xs): {len(ys)}')			# 3, ver __len__
    print(f'xs[1]: {xs[1]}')				# 10, ver __getitem__

    # Consumiendo como iterable
    for x in xs:
        print(x)	# 20 -> 10 -> 4

    # Otras operaciones
    print(f'xs.concat(ys): {xs.concat(ys)}')		# [20, 10, 4, 8, 9, 4]
    print(f'ys.join(" -> "): {ys.join(" -> ")}')	# 8 -> 9 -> 4
    print(f'xs.index(4): {xs.index(4)}')			# 2
    