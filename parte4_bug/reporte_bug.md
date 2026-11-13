# Parte 4 — Reporte de bug

## BUG-001: La cantidad de un producto en el carrito se restablece a 1 al rotar la pantalla

| Campo | Valor |
|---|---|
| **Componente** | Carrito de compras |
| **Reportado por** | Usuario final (reporte de soporte), reproducción pendiente por QA |
| **Estado** | Nuevo — pendiente de reproducir |
| **Severidad** | Alta |
| **Prioridad** | Alta |

### Entorno

| Dato | Valor |
|---|---|
| Dispositivo | Samsung — modelo por confirmar (ver preguntas abiertas) |
| Sistema operativo | Android 13 (One UI: versión por confirmar) |
| Versión de la app | Por confirmar |
| Red | Por confirmar |

### Descripción

Un usuario tenía 3 unidades de un producto (camisa) en el carrito. Al girar el teléfono, la cantidad volvió a 1. El usuario pierde la cantidad que había elegido sin hacer ninguna acción sobre ella.

### Precondiciones

1. App ShopGo instalada en un dispositivo Samsung con Android 13.
2. Usuario con sesión iniciada.
3. Rotación automática de pantalla habilitada en el dispositivo.

### Pasos para reproducir

1. Agregar una camisa al carrito.
2. Abrir el carrito con el teléfono en orientación vertical.
3. Aumentar la cantidad de la camisa de 1 a 3 con el control de cantidad.
4. Verificar que el carrito muestra cantidad 3 y el subtotal correspondiente.
5. Girar el teléfono a orientación horizontal.
6. Observar la cantidad y el subtotal de la camisa.
7. *(Variante)* Volver a vertical y observar de nuevo.

### Resultado esperado

La cantidad sigue en **3** y el subtotal no cambia, en cualquier orientación. Rotar la pantalla no modifica el contenido del carrito.

### Resultado actual

La cantidad vuelve a **1** después de girar el teléfono (según el reporte del usuario).

### Severidad: Alta

Se pierden datos que el usuario ingresó en el flujo de compra. Si no lo nota, puede comprar menos unidades de las que quería, o calcularse mal el subtotal y el envío (el umbral de envío gratis es ₡25 000).

### Prioridad: Alta

Rotar el teléfono es una acción común y el carrito es el paso previo al pago, así que el bug afecta directamente las ventas y la confianza en la app.

### Evidencia que se adjuntaría

- **Video** de la pantalla durante la reproducción (grabador de Android o `adb shell screenrecord`), mostrando la cantidad antes y después de girar.
- **Capturas** del carrito en vertical (cantidad 3) y en horizontal (cantidad 1).
- **Logs** del dispositivo durante la reproducción: `adb logcat` filtrado por el paquete de la app, para ver si la Activity o el Fragment se recrea.
- **Datos de la sesión:** versión de la app, ID del usuario de prueba y hora exacta, para cruzar con los logs del backend (¿se envió una actualización de cantidad al servidor?).

### Análisis inicial (hipótesis para desarrollo)

En Android, rotar la pantalla es un *cambio de configuración* que por defecto destruye y recrea la Activity. Si la cantidad vive solo en la vista o en una variable de la Activity, y no en un `ViewModel`, en `SavedStateHandle` o en el estado del carrito del servidor, se pierde y se vuelve al valor inicial (1). Es una hipótesis: se confirma con los logs.

### Preguntas abiertas

1. ¿Qué modelo de Samsung y qué versión de la app usa el usuario?
2. ¿Se reproduce en otros dispositivos Android, en otras versiones (12, 14) y en iOS?
3. ¿Pasa solo con la cantidad, o se pierden también otros datos del carrito (productos, cupones)?
4. ¿La cantidad se pierde solo en la pantalla, o también en el carrito guardado? Por ejemplo, ¿al cerrar y abrir la app aparece 3 o 1?
5. ¿Ocurre también con otros cambios de configuración: modo oscuro, tamaño de fuente, pantalla dividida, plegables?
6. ¿Ocurre al enviar la app a segundo plano y volver (posible pérdida de estado por el mismo motivo)?
7. ¿La cantidad se cambió con los botones +/− o escribiendo el número?

### Casos de prueba sugeridos tras la corrección

- Rotar con cantidades límite: 1, 2, 9 y 10 (rango permitido de 1 a 10).
- Rotar varias veces seguidas y con varios productos en el carrito.
- Verificar que el subtotal y el costo de envío se mantienen tras rotar.
- Agregar una prueba automatizada de regresión: con Appium, `driver.orientation = "LANDSCAPE"` y luego verificar la cantidad.
