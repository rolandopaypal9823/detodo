# Quiz de bienvenida · Comunidad Productiva

Circuito: compra (Circle o Mercado Pago) → n8n → FunnelChat (plantilla de bienvenida con el link del quiz) → quiz → califica: agenda con un asesor · no califica: libro Hackea tu cerebro.

## En GHL

Se pega lo que está entre `DESDE ACÁ` y `HASTA ACÁ` de `index.html` en el custom code de una página.

`CONFIG` (dentro del script):

| Campo | Qué va | Estado |
|---|---|---|
| `WEBHOOK_URL` | El webhook de n8n que recibe las respuestas. Vacío = no se manda nada. | **Falta** |
| `AGENDA_URL` | La agenda con un asesor: `https://calendly.com/d/dz7s-rkk-z6b`. Se abre adentro del quiz. | Listo |
| `LIBRO_URL` | La compra de Hackea tu cerebro: `https://comunidadproductiva.circle.so/hackea-tu-cerebro`. | Listo |

El video de la invitación (para los que califican) se pega entre `<template id="q-video-invitacion">` y `</template>`. Si queda vacío, no se muestra.

## El link que manda FunnelChat

```
https://[página del quiz]?nombre={{nombre}}&telefono={{telefono}}&email={{email}}&cid={{id del contacto}}
```

- Si FunnelChat solo deja una variable en el botón, alcanza con `?telefono={{1}}`: el quiz saluda sin nombre y n8n cruza por teléfono.
- `nombre` y `email` llegan precargados a Calendly.
- También lee `name`, `first_name`, `phone` y `contact_id`.

## Lo que recibe n8n

Un POST de formulario (`application/x-www-form-urlencoded`) por evento.

**Eventos (`evento`):**
- `quiz_completo`: al ver el resultado.
- `clic_agenda`: tocó "Acepto la invitación".
- `agendo`: reservó en el Calendly de adentro del quiz. Si agenda por el link alternativo ("¿No ves la agenda?"), este evento no llega: para eso conviene el webhook propio de Calendly.
- `clic_libro`: tocó el botón del libro.

**Contacto:** `nombre`, `telefono`, `email`, `cid`.

**Respuestas:**
- `momento`: A, B o C. Es la misma etapa del form del 7/10, dicha más simple.
- `equipo`: A, B o C.
- `dedicacion`.
- `s1_pendientes`, `s2_cosas_para_despues`, `s3_interrupciones`, `s4_se_apaga`, `s5_mente_encendida`: 2 = "Sí, soy yo", 1 = "A veces", 0 = "No me pasa".
- `peso`: del 1 al 10, cuánto le pesa la semana.
- `probado`: lista separada por comas.
- `seguimiento`.
- `objetivo`.
- `cerca`: del 1 al 10, qué tan cerca está de la semana que quiere.
- `pendiente`: texto libre (puede venir vacío).
- `urgencia`.

**Resultado:** `perfil`, `carga` (0 a 10), `califica` (si/no), `nivel` (alto/medio/bajo), `destino` (agenda/libro).

## Cómo decide

- **Califica**: momento A o B y quiere el cambio este mes o en los próximos 3 meses.
- **Nivel**: alto = A/B con gente a cargo · medio = A/B sin gente a cargo · bajo = C.
- **Perfil**: la situación que más le pasa (Sostén de todos, Apagaincendios, Arranque fuerte, Mente encendida). Si no le pasa ninguna, Bases firmes.

La regla está en la función `calcular()` del script, por si hay que moverla.
