# Notas

## Suposiciones

Reglas del enunciado que admiten más de una interpretación, y la decisión tomada en cada caso.

### Contraseña (Parte 2 y Parte 1)

| ID | Ambigüedad | Suposición | Dónde se refleja |
|---|---|---|---|
| S1 | "Entre 8 y 20 caracteres": ¿incluye los extremos? | Sí: 8 y 20 son válidos; 7 y 21 no. | `test_password_con_longitud_*`, TC-02, TC-03 |
| S2 | "Al menos una mayúscula": ¿solo A-Z? | Cualquier letra mayúscula según `str.isupper()`, incluidas `Ñ` y letras con tilde (`É`), por ser una app en español. | `mayuscula_con_tilde_o_enie` |
| S3 | "Al menos un número": ¿cualquier carácter numérico Unicode? | Solo dígitos `0-9`. Caracteres como `²` o `٣` no cuentan, porque el usuario espera "número" en el sentido común. | `test_password_con_numero_que_no_es_digito_ascii_es_invalida` |
| S4 | "Ningún espacio": ¿solo la barra espaciadora? | Ningún carácter de espacio en blanco: espacio, tabulación ni salto de línea (`str.isspace()`). | `test_password_con_espacios_en_blanco_es_invalida` |
| S5 | ¿Qué hace `validar_password(None)` o con un valor que no es texto? | Devuelve `False` sin lanzar excepción, porque la firma promete un `bool`. | `test_password_que_no_es_texto_*` |
| S6 | ¿Se permiten símbolos (`!@#`)? | Sí: el enunciado no los prohíbe. | `con_simbolos` |

### Envío (Parte 2)

| ID | Ambigüedad | Suposición | Dónde se refleja |
|---|---|---|---|
| S7 | ¿₡25 000 exactos tienen envío gratis? | Sí: "de ₡25 000 o más". | `25000_umbral_exacto` |
| S8 | ¿Subtotal 0 (carrito vacío)? | Se cobra ₡2 500: es menor que ₡25 000 y no es negativo. En la app real probablemente no se permitiría pagar un carrito vacío, pero eso no es responsabilidad de esta función. | `cero` |
| S9 | ¿Se admiten céntimos? | Sí: el parámetro es `float`. | `24999_99_centimo_bajo_umbral` |
| S10 | ¿NaN o infinito? | Lanzan `ValueError`, igual que un negativo: no representan un monto real. | `test_subtotal_no_finito_lanza_value_error` |
| S11 | ¿Un valor no numérico (texto, `None`)? | Lanza `TypeError` (comportamiento natural de Python); no se prueba porque la firma exige `float`. | Docstring de `calcular_envio` |

### Inicio de sesión (Parte 1 y Parte 3)

| ID | Ambigüedad | Suposición |
|---|---|---|
| S12 | ¿Qué mensaje se muestra con formato de correo inválido, contraseña sin requisitos o campos vacíos? | El enunciado solo define "Correo o contraseña incorrectos" para credenciales incorrectas. Se asume una validación previa en la app, con un mensaje junto al campo; su texto exacto no está definido. |
| S13 | ¿Cuentan para el bloqueo los intentos con formato inválido o sin conexión? | No: solo cuentan los intentos rechazados por credenciales incorrectas. |
| S14 | "3 intentos fallidos **seguidos**" | El contador es por cuenta y un inicio de sesión exitoso lo reinicia. |
| S15 | ¿Qué ve el usuario durante el bloqueo? | Un mensaje que informa del bloqueo; su texto no está definido en el enunciado. |
| S16 | Capabilities de la Parte 3 | Android con UiAutomator2, Appium 2 en `http://127.0.0.1:4723` y paquete ficticio `com.shopgo.app`, porque ShopGo no existe. |
| S17 | Textos de los elementos | `.text` devuelve el texto visible de `txt_error` y `home_title`. |

## Extras (fuera de lo solicitado)

| Extra | Qué aporta |
|---|---|
| **Integración continua con GitHub Actions** (`.github/workflows/tests.yml`) | En cada push y pull request a `main`, GitHub ejecuta automáticamente `pytest` en Python 3.10, 3.11 y 3.12 (las versiones que admite el enunciado). Si alguna prueba falla, se ve antes de integrar el cambio. |
| **Pruebas de UI opcionales** (`--run-ui` y marcador `ui`) | `pytest` a secas no falla por no tener un servidor Appium: las pruebas de la Parte 3 se saltan con un motivo claro, y se ejecutan con `pytest tests/test_login.py --run-ui`. |
| **Valores no finitos en `calcular_envio`** | Además de los negativos, NaN e infinito también lanzan `ValueError` (S10). |
| **Trabajo con ramas y pull requests** | Cada parte se desarrolló en su propia rama y se integró a `main` mediante un pull request, por lo que el historial muestra cómo se construyó cada entrega. |

## Uso de herramientas de IA

**Herramienta:** Claude Code (modelo Claude Opus), con el plugin ECC (flujos de TDD, git y revisión de código Python) y la skill UI/UX Pro Max (criterios de UX y accesibilidad mobile).

| Parte | Para qué se usó |
|---|---|
| Planificación | Desglosar el enunciado en fases y commits pequeños, y detectar reglas ambiguas. |
| Parte 1 | Proponer casos de prueba, incluidos los escenarios mobile y los criterios de accesibilidad (mensajes anunciados por TalkBack/VoiceOver, estado conservado al rotar). |
| Parte 2 | Generar las pruebas y el código con TDD (prueba que falla → implementación → refactor) y revisar el código con un agente revisor de Python. La revisión sugirió rechazar subtotales infinitos y cumplir el límite de 88 caracteres por línea; ambos cambios se aplicaron. |
| Parte 3 | Generar el Page Object, el fixture del driver y las pruebas. Se verificó la API de Appium-Python-Client 6.1.6 instalada (no de memoria) y una revisión automática sugirió filtrar por marcador y usar `try/finally` en el teardown. |
| Parte 4 | Redactar el reporte de bug y las preguntas abiertas. |
| Entrega | Redactar README y NOTAS, configurar la integración continua, crear las ramas y proponer los textos de commits y pull requests. Los commits, los pull requests y los merges los hice yo desde GitHub Desktop. |

**Qué revisé o cambié yo:**

El trabajo fue asistido con inteligencia artificial (Claude Code). Mi rol fue:

- **Planificación:** creé con Claude un plan de trabajo y lo adapté a lo que pide la prueba; por ejemplo, decidí trabajar cada parte en su propia rama, con su pull request, y hacer yo los commits.
- **Revisión del código:** revisé el código que se iba generando, apoyándome también en agentes y skills de revisión, y pedí la explicación de cada decisión para entenderla.
- **Control de versiones:** trabajé de forma ordenada, con commits pequeños que describen cada cambio y un pull request por parte, que hice y fusioné desde GitHub Desktop.
- **Verificación:** comprobé que se cumpliera todo lo que pide el enunciado y que todas las pruebas pasaran.

## Tiempo invertido

Aproximadamente **2 horas** en total, de las cuales unos 30–40 minutos fueron para analizar el plan: qué se iba a realizar y que cumpliera con lo que pide el enunciado.
