"""Pruebas de UI de la pantalla de inicio de sesión de ShopGo (Parte 3).

Requieren un servidor Appium y un dispositivo, por eso están marcadas con
`ui` y solo se ejecutan con: pytest tests/test_login.py --run-ui

Estructura de cada prueba (Arrange - Act - Assert):
- Arrange: el fixture `login_page` abre la app en la pantalla de login.
- Act: se usan las acciones del Page Object, nunca locators directamente.
- Assert: se compara lo que muestra la pantalla con el resultado esperado.
"""

import pytest

from pages.login_page import LoginPage

# Todas las pruebas de este módulo son de UI.
pytestmark = pytest.mark.ui

# Datos de prueba: usuario de QA registrado en el ambiente de pruebas (ficticio).
CORREO_REGISTRADO = "qa.tester@shopgo.com"
PASSWORD_CORRECTA = "Shopgo2026"
# Cumple el formato de contraseña, para que el rechazo sea por credenciales
# incorrectas y no por una validación de formato en el cliente.
PASSWORD_INCORRECTA = "Incorrecta99"

TITULO_HOME_ESPERADO = "Bienvenido"
MENSAJE_ERROR_ESPERADO = "Correo o contraseña incorrectos"


def test_login_exitoso_muestra_pantalla_principal_con_titulo_bienvenido(
    login_page: LoginPage,
) -> None:
    login_page.iniciar_sesion(CORREO_REGISTRADO, PASSWORD_CORRECTA)

    assert login_page.obtener_titulo_home() == TITULO_HOME_ESPERADO


def test_login_con_password_incorrecta_muestra_mensaje_de_error(
    login_page: LoginPage,
) -> None:
    login_page.iniciar_sesion(CORREO_REGISTRADO, PASSWORD_INCORRECTA)

    assert login_page.obtener_mensaje_error() == MENSAJE_ERROR_ESPERADO
