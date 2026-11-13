"""Pruebas de la Parte 2: reglas de contraseña y cálculo de envío de ShopGo.

Técnicas aplicadas:
- Análisis de valores límite: se prueba justo afuera, en y justo adentro
  de cada borde (p. ej. 7, 8, 9 ... 19, 20, 21 caracteres).
- Partición de equivalencias: un representante por cada grupo de entradas
  que el sistema debería tratar igual (sin mayúscula, sin número, etc.).
"""

import pytest

from shopgo.validaciones import calcular_envio, validar_password


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
    ids=[
        "8_minimo_exacto",
        "9_justo_sobre_minimo",
        "19_justo_bajo_maximo",
        "20_maximo_exacto",
    ],
)
def test_password_con_longitud_dentro_del_rango_es_valida(longitud: int) -> None:
    password = crear_password(longitud)
    assert len(password) == longitud  # protege contra un error en el helper

    assert validar_password(password) is True


@pytest.mark.parametrize(
    "longitud",
    [3, 7, 21, 50],
    ids=["3_muy_corta", "7_justo_bajo_minimo", "21_justo_sobre_maximo", "50_muy_larga"],
)
def test_password_con_longitud_fuera_del_rango_es_invalida(longitud: int) -> None:
    password = crear_password(longitud)
    assert len(password) == longitud

    assert validar_password(password) is False


# ---------------------------------------------------------------------------
# validar_password: reglas de composición (mayúscula, número, sin espacios)
# Todas las contraseñas tienen una longitud válida, para aislar la regla probada.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "password",
    ["Abcdefg1", "Shopgo2026", "Abc!@#12", "Ñandú123"],
    ids=[
        "minima_valida",
        "valida_tipica",
        "con_simbolos",
        "mayuscula_con_tilde_o_enie",
    ],
)
def test_password_que_cumple_todas_las_reglas_es_valida(password: str) -> None:
    assert validar_password(password) is True


def test_password_sin_mayuscula_es_invalida() -> None:
    assert validar_password("abcdefg1") is False


def test_password_sin_numero_es_invalida() -> None:
    assert validar_password("Abcdefgh") is False


def test_password_con_numero_que_no_es_digito_ascii_es_invalida() -> None:
    # "²" es un carácter numérico Unicode, pero no un dígito 0-9.
    # Suposición documentada en NOTAS.md: "número" significa dígito 0-9.
    assert validar_password("Abcdefg²") is False


@pytest.mark.parametrize(
    "password",
    [" Abcdef1", "Abc def1", "Abcdef1 ", "Abc\tdef1", "Abc\ndef1"],
    ids=[
        "espacio_al_inicio",
        "espacio_en_medio",
        "espacio_al_final",
        "tabulacion",
        "salto_de_linea",
    ],
)
def test_password_con_espacios_en_blanco_es_invalida(password: str) -> None:
    assert validar_password(password) is False


def test_password_vacia_es_invalida() -> None:
    assert validar_password("") is False


def test_password_compuesta_solo_por_espacios_es_invalida() -> None:
    assert validar_password(" " * 10) is False


@pytest.mark.parametrize(
    "valor",
    [None, 12345678, ["A", "b", "c", "d", "e", "f", "g", "1"]],
    ids=["none", "entero", "lista"],
)
def test_password_que_no_es_texto_es_invalida_sin_lanzar_excepcion(
    valor: object,
) -> None:
    # La firma promete devolver bool, así que una entrada inválida
    # se rechaza con False en lugar de romper con TypeError.
    assert validar_password(valor) is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# calcular_envio: valores límite (regla: envío gratis desde ₡25 000)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "subtotal",
    [0, 0.01, 24_999, 24_999.99],
    ids=[
        "cero",
        "un_centimo",
        "24999_justo_bajo_umbral",
        "24999_99_centimo_bajo_umbral",
    ],
)
def test_envio_cuesta_2500_cuando_el_subtotal_es_menor_a_25000(
    subtotal: float,
) -> None:
    assert calcular_envio(subtotal) == 2_500


@pytest.mark.parametrize(
    "subtotal",
    [25_000, 25_000.01, 25_001, 1_000_000],
    ids=[
        "25000_umbral_exacto",
        "25000_01_centimo_sobre_umbral",
        "25001_justo_sobre_umbral",
        "monto_alto",
    ],
)
def test_envio_es_gratis_cuando_el_subtotal_es_25000_o_mas(subtotal: float) -> None:
    assert calcular_envio(subtotal) == 0


@pytest.mark.parametrize("subtotal", [24_999, 25_000.0], ids=["pagado", "gratis"])
def test_calcular_envio_devuelve_un_entero(subtotal: float) -> None:
    # La firma indica -> int; se verifica el tipo, no solo el valor (0.0 == 0 es True).
    assert type(calcular_envio(subtotal)) is int


# ---------------------------------------------------------------------------
# calcular_envio: entradas inválidas
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "subtotal",
    [-0.01, -1, -25_000],
    ids=["centimo_negativo", "menos_uno", "negativo_igual_al_umbral"],
)
def test_subtotal_negativo_lanza_value_error(subtotal: float) -> None:
    # match= verifica además que el mensaje explique la causa del error.
    with pytest.raises(ValueError, match="negativo"):
        calcular_envio(subtotal)


@pytest.mark.parametrize(
    "subtotal",
    [float("nan"), float("inf"), float("-inf")],
    ids=["nan", "infinito_positivo", "infinito_negativo"],
)
def test_subtotal_no_finito_lanza_value_error(subtotal: float) -> None:
    # NaN e infinito no representan un monto real de carrito: sin control
    # explícito, NaN cobraría envío y +inf lo daría gratis.
    with pytest.raises(ValueError, match="número válido"):
        calcular_envio(subtotal)
