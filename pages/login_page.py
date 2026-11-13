"""Page Object de la pantalla de inicio de sesión de ShopGo (Parte 3).

Patrón Page Object: la clase encapsula *cómo* se encuentra cada elemento
(locators) y *qué* puede hacer el usuario en la pantalla (acciones). Las
pruebas solo usan las acciones, así que si un identificador cambia en la app
se corrige aquí, en un único lugar, y no en cada prueba.
"""

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Tipo de un locator: (estrategia, valor), p. ej. ("accessibility id", "btn_login").
Locator = tuple[str, str]

# Tiempo máximo (segundos) que se espera a un elemento antes de fallar.
# En mobile las transiciones y las llamadas de red hacen que los elementos
# no aparezcan al instante, por eso se usa una espera explícita y no sleep.
TIEMPO_ESPERA_POR_DEFECTO = 10


class LoginPage:
    """Representa la pantalla de inicio de sesión de la app móvil ShopGo."""

    # Locators: tuplas (estrategia, valor) que entienden find_element y las
    # expected_conditions de Selenium. Se usa ACCESSIBILITY_ID porque es el
    # mismo identificador en Android (content-desc) y en iOS
    # (accessibilityIdentifier), y no depende de textos ni de la jerarquía.
    INPUT_EMAIL = (AppiumBy.ACCESSIBILITY_ID, "input_email")
    INPUT_PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "input_password")
    BTN_LOGIN = (AppiumBy.ACCESSIBILITY_ID, "btn_login")
    TXT_ERROR = (AppiumBy.ACCESSIBILITY_ID, "txt_error")

    # El título pertenece a la pantalla principal. En un proyecto mayor iría en
    # su propio HomePage; aquí se incluye para respetar la estructura pedida y
    # porque es el resultado observable de un inicio de sesión exitoso.
    HOME_TITLE = (AppiumBy.ACCESSIBILITY_ID, "home_title")

    def __init__(
        self, driver: WebDriver, tiempo_espera: float = TIEMPO_ESPERA_POR_DEFECTO
    ) -> None:
        self.driver = driver
        # WebDriverWait reintenta la condición cada 0.5 s hasta cumplirse o hasta
        # agotar el tiempo (TimeoutException). Así la prueba avanza apenas el
        # elemento está listo, en lugar de dormir un tiempo fijo con time.sleep.
        self.wait = WebDriverWait(driver, tiempo_espera)

    # -- Esperas explícitas reutilizables ------------------------------------

    def _esperar_visible(self, locator: Locator) -> WebElement:
        """Espera a que el elemento exista y sea visible en pantalla."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _esperar_clickeable(self, locator: Locator) -> WebElement:
        """Espera a que el elemento sea visible y esté habilitado para tocarlo."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    # -- Acciones del usuario ------------------------------------------------
    # Las acciones devuelven `self` para poder encadenarlas (interfaz fluida):
    # login.ingresar_correo(...).ingresar_password(...).tocar_iniciar_sesion()

    def ingresar_correo(self, correo: str) -> "LoginPage":
        """Escribe el correo electrónico, reemplazando cualquier texto previo."""
        campo = self._esperar_visible(self.INPUT_EMAIL)
        campo.clear()
        campo.send_keys(correo)
        return self

    def ingresar_password(self, password: str) -> "LoginPage":
        """Escribe la contraseña, reemplazando cualquier texto previo."""
        campo = self._esperar_visible(self.INPUT_PASSWORD)
        campo.clear()
        campo.send_keys(password)
        return self

    def tocar_iniciar_sesion(self) -> "LoginPage":
        """Toca el botón "Iniciar sesión" cuando está habilitado."""
        self._esperar_clickeable(self.BTN_LOGIN).click()
        return self

    def iniciar_sesion(self, correo: str, password: str) -> "LoginPage":
        """Flujo completo: ingresa las credenciales y toca "Iniciar sesión"."""
        return (
            self.ingresar_correo(correo)
            .ingresar_password(password)
            .tocar_iniciar_sesion()
        )

    # -- Lecturas para las aserciones ---------------------------------------
    # El Page Object no hace asserts: solo expone lo que se ve en pantalla.
    # La prueba decide qué es correcto; así la clase sirve para casos
    # positivos y negativos por igual.
    # Nota: en Android `.text` lee el atributo text del elemento. Si la app
    # expusiera el texto solo en content-desc, habría que usar
    # get_attribute("content-desc"); se asume que los textos visibles usan text.

    def obtener_mensaje_error(self) -> str:
        """Devuelve el texto del mensaje de error cuando aparece."""
        return self._esperar_visible(self.TXT_ERROR).text

    def obtener_titulo_home(self) -> str:
        """Devuelve el título de la pantalla principal tras un login exitoso."""
        return self._esperar_visible(self.HOME_TITLE).text
