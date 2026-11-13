"""Reglas de validación de ShopGo (Parte 2 de la prueba técnica).

Las reglas provienen del enunciado:
- Contraseña: entre 8 y 20 caracteres, al menos una mayúscula,
  al menos un número y ningún espacio.
- Envío: gratis si el subtotal es de ₡25 000 o más; si no, cuesta ₡2 500.
"""

# Límites de longitud de la contraseña (ambos inclusivos).
PASSWORD_LONGITUD_MINIMA = 8
PASSWORD_LONGITUD_MAXIMA = 20


def validar_password(password: str) -> bool:
    """Indica si `password` cumple las reglas de contraseña de ShopGo.

    Args:
        password: Texto ingresado por el usuario.

    Returns:
        True si la contraseña es válida; False en caso contrario.
    """
    return PASSWORD_LONGITUD_MINIMA <= len(password) <= PASSWORD_LONGITUD_MAXIMA
