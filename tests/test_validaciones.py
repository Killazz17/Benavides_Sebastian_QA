"""Pruebas de la Parte 2: reglas de contraseña y cálculo de envío de ShopGo.

Técnicas aplicadas:
- Análisis de valores límite: se prueba justo afuera, en y justo adentro
  de cada borde (p. ej. 7, 8, 9 ... 19, 20, 21 caracteres).
- Partición de equivalencias: un representante por cada grupo de entradas
  que el sistema debería tratar igual (sin mayúscula, sin número, etc.).
"""

import pytest

from shopgo.validaciones import validar_password


def crear_password(longitud: int) -> str:
    """Genera una contraseña que cumple todas las reglas excepto, quizá, la longitud.

    Siempre incluye una mayúscula ("A") y un número ("1"); el resto se rellena
    con minúsculas. Así, si la prueba falla, la única causa posible es la longitud.
    """
    return "A1" + "a" * (longitud - 2)


# ---------------------------------------------------------------------------
# validar_password: valores límite de longitud (regla: 8 a 20 caracteres)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "longitud",
    [8, 9, 19, 20],
    ids=["8_minimo_exacto", "9_justo_sobre_minimo", "19_justo_bajo_maximo", "20_maximo_exacto"],
)
def test_password_con_longitud_dentro_del_rango_es_valida(longitud):
    password = crear_password(longitud)
    assert len(password) == longitud  # protege contra un error en el helper

    assert validar_password(password) is True


@pytest.mark.parametrize(
    "longitud",
    [3, 7, 21, 50],
    ids=["3_muy_corta", "7_justo_bajo_minimo", "21_justo_sobre_maximo", "50_muy_larga"],
)
def test_password_con_longitud_fuera_del_rango_es_invalida(longitud):
    password = crear_password(longitud)
    assert len(password) == longitud

    assert validar_password(password) is False
