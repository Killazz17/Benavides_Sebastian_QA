# Parte 1 — Casos de prueba: inicio de sesión de ShopGo

**Alcance:** pantalla de inicio de sesión de la app ShopGo (Android e iOS).
**Técnicas:** partición de equivalencias, análisis de valores límite, pruebas de estado/transición (bloqueo de cuenta) y escenarios propios de mobile.

## Reglas bajo prueba

| Regla | Origen |
|---|---|
| R1. El correo debe tener formato válido (`nombre@dominio.com`). | Enunciado |
| R2. Contraseña de 8 a 20 caracteres, con al menos una mayúscula, al menos un número y ningún espacio. | Enunciado |
| R3. Con datos incorrectos aparece "Correo o contraseña incorrectos". | Enunciado |
| R4. Tras 3 intentos fallidos seguidos, la cuenta se bloquea 5 minutos. | Enunciado |
| R5. Con login exitoso se abre la pantalla principal con el título "Bienvenido". | Enunciado |

## Datos de prueba

| Dato | Valor |
|---|---|
| Usuario registrado | `qa.tester@shopgo.com` |
| Contraseña correcta | `Shopgo2026` |
| Contraseña de 8 caracteres (válida) | `Shopgo26` |
| Contraseña de 20 caracteres (válida) | `Shopgo2026Shopgo2026` |
| Contraseña de 7 caracteres | `Shopg26` |
| Contraseña de 21 caracteres | `Shopgo2026Shopgo20261` |

## Casos de prueba

| ID | Título | Tipo | Precondiciones | Pasos | Resultado esperado | Prioridad |
|---|---|---|---|---|---|---|
| TC-01 | Inicio de sesión con credenciales válidas | Positivo | Usuario registrado con contraseña `Shopgo2026`; app instalada; conexión a internet | 1. Abrir la app.<br>2. Ingresar `qa.tester@shopgo.com` y `Shopgo2026`.<br>3. Tocar "Iniciar sesión". | Se muestra un indicador de carga y luego se abre la pantalla principal con el título "Bienvenido". | Alta |
| TC-02 | Contraseña en los límites válidos: 8 y 20 caracteres | Límite | Dos usuarios registrados: uno con `Shopgo26` (8) y otro con `Shopgo2026Shopgo2026` (20) | 1. Abrir la app.<br>2. Iniciar sesión con el usuario de contraseña de 8 caracteres.<br>3. Cerrar sesión.<br>4. Repetir con el usuario de contraseña de 20 caracteres. | Ambos inicios de sesión son exitosos y muestran "Bienvenido". El campo acepta los 20 caracteres sin truncarlos. | Alta |
| TC-03 | Contraseña fuera de rango: 7 y 21 caracteres | Límite | App instalada en la pantalla de login | 1. Ingresar un correo válido y `Shopg26` (7).<br>2. Tocar "Iniciar sesión".<br>3. Repetir con `Shopgo2026Shopgo20261` (21). | No se inicia sesión en ningún caso; se indica que la contraseña no cumple el requisito de longitud. Con 21 caracteres el campo no trunca en silencio el texto (si limita la entrada, lo hace en 20 de forma visible). | Alta |
| TC-04 | Campos vacíos | Negativo | App instalada en la pantalla de login | 1. Dejar correo y contraseña vacíos y tocar "Iniciar sesión".<br>2. Llenar solo el correo y tocar "Iniciar sesión".<br>3. Llenar solo la contraseña y tocar "Iniciar sesión". | No se envía la solicitud; cada campo vacío indica que es obligatorio. El intento no cuenta para el bloqueo (R4). | Alta |
| TC-05 | Correo con formato inválido | Negativo | App instalada en la pantalla de login | 1. Ingresar, uno a la vez, `nombre@`, `@dominio.com`, `nombre.dominio.com`, `nombre@dominio` y `nombre @dominio.com`, con una contraseña válida.<br>2. Tocar "Iniciar sesión" en cada caso. | No se inicia sesión; se indica que el formato del correo no es válido, junto al campo de correo. | Media |
| TC-06 | Contraseña que incumple las reglas de composición | Negativo | App instalada en la pantalla de login | 1. Con un correo válido, ingresar una a la vez: `shopgo2026` (sin mayúscula), `Shopgoshop` (sin número), `Shop go2026` (con espacio).<br>2. Tocar "Iniciar sesión" en cada caso. | No se inicia sesión en ningún caso; se indica qué requisito de contraseña no se cumple. | Media |
| TC-07 | Credenciales incorrectas muestran el mensaje de error | Negativo | Usuario `qa.tester@shopgo.com` registrado; cuenta sin intentos fallidos previos | 1. Ingresar `qa.tester@shopgo.com` y `Incorrecta99` (formato válido, contraseña errónea).<br>2. Tocar "Iniciar sesión".<br>3. Repetir con un correo no registrado `noexiste@shopgo.com` y `Shopgo2026`. | En ambos casos aparece exactamente "Correo o contraseña incorrectos" (el mensaje no revela cuál campo falló). Con TalkBack/VoiceOver activo, el mensaje se anuncia. El correo ingresado se conserva. | Alta |
| TC-08 | Bloqueo de cuenta tras 3 intentos fallidos seguidos | Negativo | Usuario registrado sin intentos fallidos previos | 1. Iniciar sesión con contraseña incorrecta 3 veces seguidas.<br>2. En el 4.º intento, ingresar la contraseña **correcta**. | Los intentos 1 y 2 muestran "Correo o contraseña incorrectos". Tras el 3.º, la cuenta queda bloqueada: el 4.º intento, aun con la contraseña correcta, no inicia sesión e informa del bloqueo. | Alta |
| TC-09 | Fin del bloqueo a los 5 minutos y reinicio del contador | Límite | Cuenta recién bloqueada según TC-08 | 1. A los 4 min 59 s del bloqueo, intentar con la contraseña correcta.<br>2. A los 5 min, intentar con la contraseña correcta.<br>3. En otra prueba: 2 fallos, 1 login exitoso, cerrar sesión y 1 fallo más. | 1. Sigue bloqueada.<br>2. Inicia sesión y muestra "Bienvenido".<br>3. No hay bloqueo: un login exitoso reinicia el contador de fallos "seguidos". | Media |
| TC-10 | Inicio de sesión sin conexión a internet | Mobile | Usuario registrado; modo avión activado | 1. Abrir la app.<br>2. Ingresar credenciales válidas.<br>3. Tocar "Iniciar sesión".<br>4. Desactivar el modo avión y volver a tocar "Iniciar sesión". | Paso 3: aparece un mensaje claro de falta de conexión (no "Correo o contraseña incorrectos") y el intento no cuenta para el bloqueo; la app no se cierra. Paso 4: inicia sesión normalmente. | Alta |
| TC-11 | Rotar la pantalla conserva los datos ingresados | Mobile | App en la pantalla de login; rotación automática habilitada | 1. Ingresar correo y contraseña.<br>2. Rotar a horizontal y luego volver a vertical.<br>3. Provocar un error de credenciales y rotar de nuevo. | El correo y la contraseña se conservan (la contraseña sigue oculta); el mensaje de error sigue visible tras rotar. En horizontal, el teclado no tapa el campo activo ni el botón "Iniciar sesión". | Media |
| TC-12 | Enviar la app a segundo plano durante el inicio de sesión | Mobile | Usuario registrado; red lenta simulada (p. ej. perfil 3G) | 1. Ingresar credenciales válidas y tocar "Iniciar sesión".<br>2. Mientras carga, ir a la pantalla de inicio del teléfono.<br>3. Esperar 10 s y volver a la app. | La app retoma el estado correcto: muestra "Bienvenido" si el login terminó, o sigue cargando; no se duplica la solicitud ni vuelve a un login vacío. | Media |

## Cobertura

| Regla | Casos |
|---|---|
| R1 — formato de correo | TC-05, TC-04 |
| R2 — reglas de contraseña | TC-02, TC-03, TC-06, TC-04 |
| R3 — mensaje de error | TC-07, TC-08 |
| R4 — bloqueo | TC-08, TC-09 (y verificación de que TC-04 y TC-10 no suman intentos) |
| R5 — login exitoso | TC-01, TC-02, TC-09 |
| Mobile | TC-10 (red), TC-11 (rotación), TC-12 (segundo plano) |

**Criterio de prioridad:** *Alta* = bloquea el acceso del usuario o afecta la seguridad de la cuenta; *Media* = afecta la experiencia o una regla secundaria, pero existe una alternativa para el usuario.

Las suposiciones sobre reglas ambiguas (mensajes de validación de formato, si los intentos sin conexión cuentan para el bloqueo, etc.) están en [`NOTAS.md`](../NOTAS.md).
