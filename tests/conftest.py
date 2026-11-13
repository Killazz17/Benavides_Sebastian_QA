"""Configuración compartida de pytest (Parte 3): driver de Appium y opción --run-ui.

pytest carga este archivo automáticamente; los fixtures definidos aquí están
disponibles en todas las pruebas de la carpeta sin necesidad de importarlos.
"""

import os
from collections.abc import Iterator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver

from pages.login_page import LoginPage

# URL del servidor Appium 2 (por defecto, el puerto estándar en la máquina local).
# Se puede cambiar sin tocar código: APPIUM_SERVER_URL=http://otra-maquina:4723
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")


# ---------------------------------------------------------------------------
# Opción --run-ui: las pruebas de UI solo corren cuando se piden explícitamente
# ---------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-ui",
        action="store_true",
        default=False,
        help="Ejecuta las pruebas marcadas con @pytest.mark.ui (requiere Appium).",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Salta las pruebas de UI si no se pasó --run-ui.

    Sin esto, `pytest` a secas fallaría con un error de conexión al no haber
    servidor Appium ni emulador, y ocultaría el resultado de la Parte 2.
    """
    if config.getoption("--run-ui"):
        return

    saltar_ui = pytest.mark.skip(
        reason="Prueba de UI: requiere servidor Appium y dispositivo (usar --run-ui)."
    )
    for item in items:
        # get_closest_marker busca solo el marcador `ui`; item.keywords también
        # coincidiría con pruebas o módulos cuyo nombre contenga "ui".
        if item.get_closest_marker("ui"):
            item.add_marker(saltar_ui)


# ---------------------------------------------------------------------------
# Fixtures del driver y de los Page Objects
# ---------------------------------------------------------------------------


def crear_capabilities() -> UiAutomator2Options:
    """Capabilities de ejemplo para abrir ShopGo en un emulador Android.

    Las capabilities le dicen al servidor Appium qué dispositivo usar, qué app
    abrir y con qué motor de automatización (UiAutomator2 en Android).
    Los valores de la app son ficticios porque ShopGo no existe.
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.getenv("DEVICE_NAME", "emulator-5554")
    options.app_package = "com.shopgo.app"
    options.app_activity = ".ui.login.LoginActivity"
    # no_reset=False: limpia el estado de la app en cada sesión para que
    # cada prueba empiece desde la pantalla de login, sin datos de la anterior.
    options.no_reset = False
    options.new_command_timeout = 60
    return options


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Abre una sesión de Appium por prueba y la cierra al terminar.

    Lo anterior al `yield` es el setup; lo posterior es el teardown y se
    ejecuta aunque la prueba falle, así no quedan sesiones abiertas.
    """
    appium_driver = webdriver.Remote(APPIUM_SERVER_URL, options=crear_capabilities())
    try:
        yield appium_driver
    finally:
        # finally garantiza el cierre incluso ante errores durante el teardown.
        appium_driver.quit()


@pytest.fixture
def login_page(driver: WebDriver) -> LoginPage:
    """Entrega la pantalla de login lista para usar en la prueba."""
    return LoginPage(driver)
