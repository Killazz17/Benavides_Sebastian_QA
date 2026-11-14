# Prueba Técnica — QA Automation Mobile (ShopGo)

Solución de la prueba técnica para la pasantía de QA Automation Mobile de QXD.
**Autor:** Sebastian Benavides Madrigal

| Parte | Entregable | Archivo(s) |
|---|---|---|
| 1. Casos de prueba | 12 casos de login (positivos, negativos, límite y mobile) | [`parte1_casos/casos_login.md`](parte1_casos/casos_login.md) |
| 2. Pruebas automatizadas | `validar_password` y `calcular_envio` + 41 pruebas pytest | [`shopgo/validaciones.py`](shopgo/validaciones.py), [`tests/test_validaciones.py`](tests/test_validaciones.py) |
| 3. Script de UI mobile | Page Object `LoginPage` con Appium y esperas explícitas | [`pages/login_page.py`](pages/login_page.py), [`tests/conftest.py`](tests/conftest.py), [`tests/test_login.py`](tests/test_login.py) |
| 4. Reporte de bug | Cantidad del carrito que se pierde al rotar | [`parte4_bug/reporte_bug.md`](parte4_bug/reporte_bug.md) |
| Notas | Suposiciones, uso de IA y tiempo invertido | [`NOTAS.md`](NOTAS.md) |

## Requisitos

- Python **3.10 o superior** (`python --version`)
- Git (opcional, para clonar)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Killazz17/Benavides_Sebastian_QA.git
cd Benavides_Sebastian_QA
```

### 2. Crear y activar el entorno virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

### Parte 2 — pruebas de validaciones

```bash
pytest tests/test_validaciones.py
```

Resultado esperado: `41 passed`. Para ver el nombre de cada caso, agregue `-v`:

```bash
pytest tests/test_validaciones.py -v
```

### Toda la suite

```bash
pytest
```

Resultado esperado: `41 passed, 2 skipped`. Las 2 pruebas de UI de la Parte 3 se **saltan a propósito**: necesitan un servidor Appium y un dispositivo, y el enunciado indica que no hace falta ejecutarlas.

### Parte 3 — pruebas de UI (opcional, requiere Appium)

Para ejecutarlas contra un emulador real con la app instalada:

1. Iniciar Appium 2 con el driver UiAutomator2 (`appium driver install uiautomator2` y luego `appium`).
2. Iniciar un emulador Android (por defecto `emulator-5554`).
3. Ejecutar con la opción `--run-ui`:

```bash
pytest tests/test_login.py --run-ui
```

Variables de entorno opcionales:

| Variable | Valor por defecto | Uso |
|---|---|---|
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` | URL del servidor Appium |
| `DEVICE_NAME` | `emulator-5554` | Dispositivo o emulador a usar |

## Estructura del proyecto

```
Benavides_Sebastian_QA/
├── README.md                  cómo crear el entorno, instalar y ejecutar
├── NOTAS.md                   suposiciones, uso de IA y tiempo invertido
├── requirements.txt           pytest, Appium-Python-Client
├── pytest.ini                 configuración de pytest y marcador `ui`
├── parte1_casos/
│   └── casos_login.md         Parte 1: casos de prueba
├── shopgo/
│   ├── __init__.py
│   └── validaciones.py        Parte 2: validar_password, calcular_envio
├── pages/
│   ├── __init__.py
│   └── login_page.py          Parte 3: Page Object
├── tests/
│   ├── conftest.py            Parte 3: fixture del driver y opción --run-ui
│   ├── test_validaciones.py   Parte 2
│   └── test_login.py          Parte 3
└── parte4_bug/
    └── reporte_bug.md         Parte 4: reporte de bug
```

## Extras

- **Integración continua (GitHub Actions):** cada push y pull request a `main` ejecuta `pytest` en Python 3.10, 3.11 y 3.12. El resultado se ve en la pestaña *Actions* del repositorio.
- **Pruebas de UI opcionales:** se saltan por defecto y se ejecutan con `--run-ui`.

Más detalle en [`NOTAS.md`](NOTAS.md#extras-fuera-de-lo-solicitado).

## Decisiones técnicas

- **TDD en la Parte 2:** cada regla se escribió primero como prueba que falla y luego se implementó; el historial de commits muestra los ciclos *RED → GREEN → REFACTOR*. Cobertura de líneas y ramas de `shopgo/validaciones.py`: 100 %.
- **Valores límite y partición de equivalencias:** las pruebas cubren justo afuera, en y justo adentro de cada borde (7/8/9 y 19/20/21 caracteres; ₡24 999,99 / ₡25 000 / ₡25 000,01).
- **Page Object sin asserts:** `LoginPage` expone acciones y lecturas; las pruebas deciden qué es correcto.
- **Esperas explícitas:** `WebDriverWait` + `expected_conditions`, sin `time.sleep`.
- **Pruebas de UI opt-in:** el marcador `ui` y la opción `--run-ui` evitan que la suite falle donde no hay Appium.
