# Quiz de bienvenida · Comunidad Productiva

Circuito: compra (Circle o Mercado Pago) → n8n → FunnelChat (plantilla de bienvenida con el link del quiz) → quiz → califica: agenda con un asesor · no califica: libro Hackea tu cerebro.

## En GHL

Se pega lo que está entre `DESDE ACÁ` y `HASTA ACÁ` de `index.html` en el custom code de una página.

Antes de publicar, completar en `CONFIG` (dentro del script):

| Campo | Qué va |
|---|---|
| `WEBHOOK_URL` | El webhook de n8n que recibe las respuestas. Vacío = no se manda nada. |
| `AGENDA_URL` | La agenda de la sesión con un asesor. Hoy tiene el Calendly de las clases: confirmar. |
| `LIBRO_URL` | El link de compra de Hackea tu cerebro. |

El video de la invitación (para los que califican) se pega entre `<template id="q-video-invitacion">` y `</template>`. Si queda vacío, no se muestra.

## El link que manda FunnelChat

```
https://[página del quiz]?nombre={{nombre}}&telefono={{telefono}}&email={{email}}&cid={{id del contacto}}
```

`nombre` se usa para saludar y para precargar la agenda. Todos viajan a n8n.

## Lo que recibe n8n

Un POST de formulario (`application/x-www-form-urlencoded`) por evento:

- `evento`: `quiz_completo` al terminar, `clic_agenda` o `clic_libro` al tocar el botón final.
- Contacto: `nombre`, `telefono`, `email`, `cid`.
- Respuestas:
  - `momento`: A, B o C. Es la misma etapa del form del 7/10, dicha más simple.
  - `equipo`: A, B o C.
  - `dedicacion`.
  - `s1_pendientes`, `s2_cosas_para_despues`, `s3_interrupciones`, `s4_se_apaga`, `s5_mente_encendida`: 2 = me pasa mucho, 1 = algunos días, 0 = no me pasa.
  - `probado`: lista separada por comas.
  - `seguimiento`.
  - `objetivo`.
  - `pendiente`: texto libre.
  - `urgencia`.
- Resultado: `perfil`, `carga` (0 a 10), `califica` (si/no), `nivel` (alto/medio/bajo), `destino` (agenda/libro).

## Cómo decide

- **Califica**: momento A o B y quiere el cambio este mes o en los próximos 3 meses.
- **Nivel**: alto = A/B con gente a cargo · medio = A/B sin gente a cargo · bajo = C.
- **Perfil**: la situación que más le pasa (Sostén de todos, Apagaincendios, Arranque fuerte, Mente encendida). Si no le pasa ninguna, Bases firmes.

La regla está en la función `calcular()` del script, por si hay que moverla.
