from typing import Generic, TypeVar

T = TypeVar('T')
S = TypeVar('S')

class ArbolH(Generic[T, S]):
    def __init__(self, dato: T | S):
        self._dato: T | S = dato
        self._subarboles: list[ArbolH[T, S]] = []
        self._tipo_hoja = type(dato)
        self._tipo_nodo = None
    
    @staticmethod
    def crear_nodo_y_hojas(dato_raiz: S, *datos_hojas: T) -> "ArbolH[T, S]":
        if not datos_hojas:
            raise ValueError("Se requiere al menos un dato para las hojas")
        if (not all([isinstance(dato, type(datos_hojas[0])) for dato in datos_hojas])):
            raise ValueError("Todos los datos de las hojas deben ser del mismo tipo")
        
        nuevo = ArbolH(dato_raiz)
        for dato in datos_hojas:
            subarbol = ArbolH(dato)
            subarbol._tipo_nodo = type(dato_raiz)
            nuevo._subarboles.append(subarbol)
        nuevo._tipo_nodo = type(dato_raiz)
        nuevo._tipo_hoja = type(datos_hojas[0])
        return nuevo

    def dato_hoja(self) -> T:
        if self.es_hoja():
            return self._dato
        raise ValueError("El nodo actual no es una hoja")

    def dato_nodo(self) -> S:
        if not self.es_hoja():
            return self._dato
        raise ValueError("El nodo actual es una hoja")
    
    @property
    def subarboles(self) -> "list[ArbolH[T,S]]":
        return self._subarboles

    def _insertar_subarbol_nocheck(self, subarbol: "ArbolH[T,S]") -> None:
        subarbol._tipo_nodo = self._tipo_nodo
        self.subarboles.append(subarbol)

    def insertar_subarbol(self, subarbol: "ArbolH[T,S]")-> None:
        if self.es_hoja():
            raise ValueError("No se pueden insertar subárboles en un nodo hoja")
        if not self._son_mismos_tipos(subarbol):
            raise ValueError("El árbol a insertar no es consistente con los tipos de datos del árbol actual")

        self._insertar_subarbol_nocheck(subarbol)

    def es_hoja(self) -> bool:
        return self.subarboles == []
    
    def __str__(self) -> str:
        def mostrar(t: ArbolH[T,S], nivel: int):
            tab = '.' * 4
            indent = tab * nivel
            if t.es_hoja():
                dato = f'[{t.dato_hoja()}]'
            else:
                dato = str(t.dato_nodo())
            out = f'{indent} {dato} \n'
            for subarbol in t.subarboles:
                out += mostrar(subarbol, nivel + 1)
            return out
            
        return mostrar(self, 0)

    def _son_mismos_tipos(self, otro: "ArbolH[T,S]") -> bool:
        return (
            isinstance(otro, ArbolH) and (
                self._tipo_nodo == otro._tipo_nodo or self.es_hoja() or otro.es_hoja()
            ) and self._tipo_hoja == otro._tipo_hoja
        )
    
    def es_valido(self) -> bool:
        pass
        

def main():
    nodo_b = ArbolH.crear_nodo_y_hojas('b', 6, 7)
    nodo_c = ArbolH.crear_nodo_y_hojas('c', 8, 9)
    arbol = ArbolH.crear_nodo_y_hojas('a', 1, 2, 3, 4, 5)
    arbol.insertar_subarbol(nodo_b)
    nodo_b.insertar_subarbol(nodo_c)
    nodo_c.insertar_subarbol(ArbolH(10))
    print(arbol)

    nodo_int = ArbolH.crear_nodo_y_hojas(1, 2, 3)
    # arbol.insertar_subarbol(nodo_int)  # Debería lanzar una excepción

if __name__ == '__main__':
    main()
