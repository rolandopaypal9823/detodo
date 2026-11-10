# Landing de la Comunidad · clase todos los días a las 19:00 (Argentina)

`index.html` es la versión B (VSL) de la masterclass del 27/10 (`landing-siempre-on/masterclass-27-octubre/version-b-vsl.html`, en la rama `claude/nueva-landing-form-7ajo0h`), con dos cambios:

1. **Reloj diario.** El contador y todas las fechas apuntan siempre a la próxima clase de las 19:00 de Argentina:
   - antes de las 19 dice "Hoy" y cuenta hasta las 19 de hoy;
   - a las 19 en punto se reinicia solo, aunque la página esté abierta, y pasa a "Mañana";
   - el contador no tiene casilla de días, porque siempre falta menos de uno.

   No hay fecha que cambiar en el `CONFIG`. Para dejar unos minutos después de las 19 en que siga mostrando la clase de hoy, se usa `MINUTOS_DE_GRACIA`.
2. **Edición:** `UTM_CLASE: 'comunidad-clase-diaria'`. Viaja al form como `edicion` y como `utm_campaign` si el lead llega sin UTM. `clase_fecha` lleva el día de la clase a la que se anotó.

Lo que va en GHL es lo que está entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ». El pixel de Meta va adentro, como siempre.

## Redirección a la sala de espera (se hace en GHL)

La redirección no está en el código de la landing: el form es un iframe de GHL y la decide el form.

En GHL: Sites → Forms → **"Form Webinar Comunidad"** (`ib4zw3gRec1D9D3kxyUv`) → Options (o Settings) → On submit → **Open URL / Redirect to URL**:

```
https://clase-instituto-productividad.netlify.app/sala.html
```

Ese mismo form lo usa `landing-siempre-on/masterclass-27-octubre/index.html`, así que el cambio también aplica a esa landing.

## Probado

En Chromium headless, con el reloj del navegador simulado, en celular (390 px) y escritorio (1366 px), sin errores de JS ni scroll horizontal:

| Hora en Argentina | Muestra | Contador |
|---|---|---|
| 18:00 | Hoy, martes 10 de noviembre · 19:00 hs | 00 h 59 min |
| 19:30 | Mañana, miércoles 11 de noviembre · 19:00 hs | 23 h 29 min |
| 18:59:50 y pasan 15 s | se reinicia a "Mañana" | 23 h 59 min |
