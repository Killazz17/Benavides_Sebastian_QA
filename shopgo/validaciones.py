"""Reglas de validación de ShopGo (Parte 2 de la prueba técnica).

Las reglas provienen del enunciado:
- Contraseña: entre 8 y 20 caracteres, al menos una mayúscula,
  al menos un número y ningún espacio.
- Envío: gratis si el subtotal es de ₡25 000 o más; si no, cuesta ₡2 500.
"""

import math
import string

# Límites de longitud de la contraseña (ambos inclusivos).
PASSWORD_LONGITUD_MINIMA = 8
PASSWORD_LONGITUD_MAXIMA = 20

# Montos de envío en colones (₡).
UMBRAL_ENVIO_GRATIS = 25_000
COSTO_ENVIO = 2_500


def validar_password(password: str) -> bool:
    """Indica si `password` cumple las reglas de contraseña de ShopGo.

    Args:
        password: Texto ingresado por el usuario.

    Returns:
        True si la contraseña es válida; False en caso contrario.
        Las entradas que no son texto (por ejemplo None) devuelven False
        en lugar de lanzar una excepción, porque la función promete un bool.
    """
    # Sin esta guarda, len() aceptaría listas u otros objetos de tamaño válido,
    # y None provocaría un TypeError.
    if not isinstance(password, str):
        return False

    if not PASSWORD_LONGITUD_MINIMA <= len(password) <= PASSWORD_LONGITUD_MAXIMA:
        return False

    # isupper() reconoce mayúsculas con tilde o eñe (É, Ñ), no solo A-Z.
    tiene_mayuscula = any(caracter.isupper() for caracter in password)
    # Se usa string.digits (0-9) en vez de isdigit(), que también acepta "²" o "٣".
    tiene_numero = any(caracter in string.digits for caracter in password)
    # isspace() cubre espacio, tabulación, salto de línea y otros espacios Unicode.
    tiene_espacios = any(caracter.isspace() for caracter in password)

    return tiene_mayuscula and tiene_numero and not tiene_espacios


def calcular_envio(subtotal: float) -> int:
    """Calcula el costo de envío de un pedido según su subtotal.

    Args:
        subtotal: Suma de los productos del carrito, en colones.

    Returns:
        0 si el subtotal es de ₡25 000 o más; 2500 si es menor.

    Raises:
        ValueError: Si el subtotal es negativo o no es finito (NaN o infinito).
        TypeError: Si el subtotal no es numérico (p. ej. None o texto),
            lo lanza math.isfinite al no poder interpretarlo como número.
    """
    # Los valores no finitos se revisan primero: cualquier comparación con NaN
    # da False (pasaría el control de negativos) y +inf daría envío gratis.
    if not math.isfinite(subtotal):
        raise ValueError(f"El subtotal debe ser un número válido: {subtotal}")
    if subtotal < 0:
        raise ValueError(f"El subtotal no puede ser negativo: {subtotal}")

    return 0 if subtotal >= UMBRAL_ENVIO_GRATIS else COSTO_ENVIO
