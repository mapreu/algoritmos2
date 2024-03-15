from typing import Union, TypeAlias

__all__ = ['Nat', 'cero', 'division', 'es_cero', 'igual', 'mayor', 'mayor_igual', 'menor', 'menor_igual', 'nat_to_int', 'potencia', 'pred', 'producto', 'resta', 'suc', 'suma']

Nat: TypeAlias = Union["Cero", "Suc"]

# Clases constructoras de estructura
class Cero:
    def __repr__(self):
        return 'Cero'

    def __str__(self):
        return '0'

class Suc:
    def __init__(self, pred: Nat):
        self.pred = pred

    def __repr__(self):
        if isinstance(self.pred, Cero):
            return 'Suc(Cero)'
        else:
            return f'Suc({self.pred.__repr__()})'

    def __str__(self):
        return str(nat_to_int(self))

# Operaciones
def cero() -> Nat:
    return Cero()

def es_cero(n: Nat) -> bool:
    return isinstance(n, Cero)

def suc(n: Nat) -> Nat:
    return Suc(n)

def pred(n: Nat) -> Nat:
    if es_cero(n):
        raise ValueError('cero no tiene predecesor')
    else:
        return n.pred

def nat_to_int(n: Nat) -> int:
    if es_cero(n):
        return 0
    else:
        return 1 + nat_to_int(pred(n))

def suma(x: Nat, y: Nat) -> Nat:
    if es_cero(x):
        return y
    else:
        return suma(pred(x), suc(y))
    
def igual(x: Nat, y: Nat) -> bool:
    pass
    
def menor(x: Nat, y: Nat) -> bool:
    pass

def mayor(x: Nat, y: Nat) -> bool:
    pass

def menor_igual(x: Nat, y: Nat) -> bool:
    pass

def mayor_igual(x: Nat, y: Nat) -> bool:
    pass

def resta(x: Nat, y: Nat) -> Nat:
    pass
    
def producto(x: Nat, y: Nat) -> Nat:
    pass

def division(x: Nat, y: Nat) -> Nat:
    pass

def potencia(base: Nat, exponente: Nat) -> Nat:
    pass

if __name__ == '__main__':
    n1: Nat = cero()                # n1 = 0
    n2: Nat = suc(suc(suc(n1)))     # n2 = 3
    n3: Nat = suc(suc(n2))          # n3 = 5
    print(es_cero(n1))              # True
    n2 = pred(n2)                   # n2 = 2
    print(n2)                       # 2
    print(n3)                       # 5
    n4: Nat = suma(n2, n3)          # n4 = 7
    print(n4)                       # 7
    print(resta(n4, n2))            # 5
    print(repr(n4)) # Suc(Suc(Suc(Suc(Suc(Suc(Suc(Cero)))))))
    
    print(f'n2 < n4: {menor(n2, n4)}')
    print(f'n3 > n4: {mayor(n3, n4)}')
    print(f'producto(n2, n4): {producto(n2, n4)}')  # 14
    print(f'division(n4, n2): {division(n4, n2)}')  # 3