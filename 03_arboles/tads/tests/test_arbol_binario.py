import pytest
from ..arbol_binario import ArbolBinario


@pytest.fixture
def arbol_vacio():
    return ArbolBinario()


@pytest.fixture
def arbol_un_nodo():
    return ArbolBinario.crear_nodo(1)


@pytest.fixture
def arbol_tres_nodos():
    tree = ArbolBinario.crear_nodo(1)
    tree.raiz.si = ArbolBinario.crear_nodo(2)
    tree.raiz.sd = ArbolBinario.crear_nodo(3)
    return tree


def test_es_vacio(arbol_vacio):
    assert arbol_vacio.es_vacio()


def test_no_es_vacio(arbol_un_nodo):
    assert not arbol_un_nodo.es_vacio()


def test_arbol_tres_nodos_dato(arbol_tres_nodos):
    assert arbol_tres_nodos.dato() == 1


@pytest.mark.parametrize("side,expected", [("si", 2), ("sd", 3)])
def test_arbol_tres_nodos_children(arbol_tres_nodos, side, expected):
    assert getattr(arbol_tres_nodos, side)().dato() == expected


def test_valida_es_vacio(arbol_vacio):
    with pytest.raises(TypeError):
        arbol_vacio._Decoradores.valida_es_vacio(lambda self: self.dato())(arbol_vacio)

def test_insertar_si(arbol_un_nodo):
    arbol_un_nodo.insertar_si(ArbolBinario.crear_nodo(2))
    assert arbol_un_nodo.si().dato() == 2

def test_insertar_sd(arbol_un_nodo):
    arbol_un_nodo.insertar_sd(ArbolBinario.crear_nodo(3))
    assert arbol_un_nodo.sd().dato() == 3

def test_altura(arbol_tres_nodos):
    assert arbol_tres_nodos.altura() == 2

def test_len(arbol_tres_nodos):
    assert len(arbol_tres_nodos) == 3

def test_inorder(arbol_tres_nodos):
    assert arbol_tres_nodos.inorder() == [2, 1, 3]

def test_es_hoja(arbol_un_nodo, arbol_tres_nodos):
    assert arbol_un_nodo.es_hoja()
    assert not arbol_tres_nodos.es_hoja()

@pytest.mark.parametrize('arbol,expected', [('arbol_vacio', 'AV\n'), ('arbol_un_nodo', '1\n....AV\n....AV\n')])
def test_str(request, arbol, expected):
    arbol = request.getfixturevalue(arbol)
    assert str(arbol) == expected

def test_copy(arbol_tres_nodos):
    copy = arbol_tres_nodos.copy()
    assert copy.inorder() == arbol_tres_nodos.inorder()

def test_espejo(arbol_tres_nodos):
    espejo = arbol_tres_nodos.espejo()
    assert espejo.inorder() == [3, 1, 2]

def test_sin_hojas(arbol_tres_nodos):
    arbol_tres_nodos.sin_hojas()
    assert arbol_tres_nodos.inorder() == [1]