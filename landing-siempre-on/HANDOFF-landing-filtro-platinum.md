# Handoff · Landing de webinar para atraer al perfil Platinum

Fecha: 10/11/2026. Resume lo que se analizó y decidió en la conversación sobre los lanzamientos del 22/09 (bueno) y del 04/11 (flojo), para armar la landing de la próxima clase.

Informe completo con tablas: https://claude.ai/artifact/JYubrLS7rQcsc5FJzbmd2v (privado, se comparte desde el menú Compartir).

---

## 1. Qué se analizó

- **Formulario de GHL:** 6.227 registros del 04/11 y 3.151 del 22/09, cruzados por mail y teléfono con las llamadas del CRM y la tabla de cierres.
- **Fathom:** 178 transcripciones de llamadas con asistencia (cierres, reservas y no cierres de los dos lanzamientos) y 13 de octubre. Se leyó solo lo que dice el lead.
- **Meta:** configuración real de las campañas de cada lanzamiento (cuenta NFM USD) y su historial de cambios.
- **Landing:** la del 22/09 y la del 04/11 son prácticamente idénticas. Cambian solo las fechas y "cabeza" → "mente".

## 2. Hallazgos que importan para la landing

1. **La pregunta de etapa (A/B/C) filtra bien y NO se toca.** La etapa C dio 0 Platinum y 2 Gold en 5.432 registros; lo que compra es Comunidad.
2. **El que paga Platinum es dueño o socio con equipo propio.** Es el perfil con más Platinum: 6 de 12 en las llamadas, y el 19% de sus llamadas termina en Platinum. Tener cargo sin ser dueño no alcanza.
3. **En el formulario, Platinum se concentra en etapa A + nivel alto** (A con gente a cargo):
   - 4 Platinum en 859 registros (4,7 cada 1.000).
   - 14,8% de los que agendaron compró Platinum.
   - B alto: 1 Platinum en 1.332.
4. **El dolor de la landing no filtra.** "No tengo tiempo", "la cabeza no para", "no desconecto", procrastinar y dormir mal los dicen igual el que paga y el que se pierde por plata. Lo que separa es el contexto:
   - En el que paga, el incendio es la gente y las decisiones que pasan por él.
   - En el que no puede pagar, el incendio es la plata.
5. **Nadie citó el titular actual** ("el sobreprecio de ser productivo"). Lo que recuerdan es la clase, a Nico y herramientas concretas:
   - 45 minutos sin celular
   - luz solar a la mañana
   - anotar a la noche lo del día siguiente
   - bloques sin interrupciones
6. **Lo que más dicen los que se pierden por plata:** ganar más, despegar, conseguir clientes, independizarse, segundo ingreso, terminar la carrera, "no llego a fin de mes". Ninguno abre la llamada contando un equipo propio con facturación estable.
7. **La diferencia entre lanzamientos vino del tráfico, no de la landing.** El 04/11:
   - optimizó por CompleteRegistration enviado a A, B y C;
   - abrió ubicaciones baratas (Marketplace, búsqueda, Threads, notificaciones);
   - excluyó a todos los que ya se habían registrado alguna vez.

   El mismo anuncio trajo 35% de C en septiembre y 66% en noviembre.

## 3. Decisiones tomadas

- **Pregunta de etapa:** queda exactamente igual, sin cambiar una palabra.
- **Conversión para Meta:** solo etapa A y B. En GHL (workflow "Lead se registra/webhook/Api Meta"):
  - una sola FB Conversion API, dentro de la rama "Califica";
  - se saca la que estaba antes de la pregunta.

  Queda en evaluación mandar Lead solo para A + nivel alto, para optimizar hacia Platinum (ver punto 7).
- **Etapa C:** no va al grupo de WhatsApp ni a la clase. Se la manda a https://hackeatuvida.netlify.app/ (lead magnet para el lanzamiento del nuevo libro de Nico), con un mensaje.
- **Temática nueva y colores invertidos**, para que no parezca la misma landing.

## 4. Título (misma estructura que el que funcionó)

Estructura: arriba para quién es; titular "Dejá de [dolor]"; subtítulo con el objetivo y el mecanismo (neurociencia). El nombre del evento sigue siendo "Neurociencia para el Alto Rendimiento Profesional".

**Recomendado**
- Arriba: *Clase en vivo para dueños, socios y profesionales con equipo*
- H1: **Dejá de pagar el sobreprecio de que todo pase por vos.**
- Sub: Neurociencia para seguir haciendo crecer lo que construiste sin pagarlo con tu sueño, tu salud ni el tiempo con tu familia.

**Alternativas**
1. Dejá de pagar el sobreprecio de ser imprescindible. (La más corta, pero también le puede hablar a un gerente que no es dueño de nada.)
2. Dejá de pagar el sobreprecio de tener la mente en el negocio las 24 horas.
3. Dejá de pagar con tus vacaciones, tu sueño y tu familia el precio de que tu negocio funcione.

Regla de marca: "mente" o "cerebro", nunca "cabeza", en el copy firmado por Nico o el Instituto.

## 5. Cambios por sección

| Sección | Cambio |
|---|---|
| Hero | Título del punto 4. Dice para quién es. |
| "Lo que este evento desarma" | Se saca (5 am, sacrificarse, otro curso: les habla a todos). Va un bloque con escenas en palabras de compradores (abajo). |
| Historia de Nico | Se mantiene, contada desde el estudio y las empresas que asesoraba. Valoran "es contador" y "vivió lo mismo". Se acorta lo de "venir de abajo", que engancha al que no califica. |
| Qué vas a aprender | Herramientas concretas: celular, luz, sueño, bloques sin interrupciones, delegar sin que se caiga nada (5 de 7 Platinum de octubre nombran delegar). Sale "IA y Second Brain": ningún comprador lo mencionó. |
| Casos | Mismos casos de dueños, con el tamaño de lo que manejan (ej. "dueño de farmacia, 6 empleados"). Un lead que no calificaba dijo: «eran todos profesionales, no me van a tomar». |
| Bloque nuevo, corto | "Para quién es / para quién no es", sin hablar de plata. Ej.: "No es para vos si estás buscando tu primer cliente, un ingreso extra o arrancar un emprendimiento." |
| Seriedad | Una línea: sin soluciones mágicas ni promesas de facturación; equipo de psicólogos, nutricionistas y coaches. Los compradores lo destacan. |
| Quiz | Pregunta de etapa sin cambios. A y B siguen igual. C → mensaje + botón al lead magnet (punto 6). |

**Escenas para el bloque nuevo** (frases textuales de compradores Gold/Platinum):
- «yo salgo a vacaciones, pero atiendo celular»
- «apago la luz de la veterinaria y a veces incluso no me voy»
- «llevo dos semanas despertándome a las tres y media de la mañana con cosas en la cabeza» (citar como "con cosas en la mente" si va en voz de Nico)
- «si no estoy en todo, como que no va a funcionar»
- «yo puedo planificar lo que quiero planificar, pero el día también te llevo puesto»
- «todo lo que quise hacer lo fui logrando acá adentro, pero no lo disfruto»
- «atiendo gente, los veo, los pacientes, todo, pero, ¿y yo cuándo?»
- «no me va mal, ¿por qué entonces estoy tan pasada?»

**Evitar en el copy** (atrae al que se pierde por plata): ganar más, despegar, conseguir clientes, independizarse, segundo ingreso, terminar la carrera, "al jefe", "para estar mejor", procrastinación genérica como gancho principal, "priorizate", "tocaste fondo".

## 6. Etapa C

Al elegir C y tocar "Continuar", aparece:

> **Gracias por contarnos dónde estás.**
> Esta clase está pensada para quienes ya tienen un negocio o un equipo funcionando. Para tu momento, Nico preparó algo que te va a servir más.
> **[Quiero el regalo de Nico →]** → https://hackeatuvida.netlify.app/ con UTMs (utm_source=landing-clase, utm_medium=etapa-c, utm_campaign=<edición>)

- No habla de plata ni dice "no calificás".
- Ajustar el texto del botón cuando se sepa qué ofrece esa página. Desde la sesión anterior no se pudo abrir: la red la bloqueaba.

## 7. Colores

Invertir la lógica actual:
- **Hero y la mayoría de las secciones:** fondo blanco con títulos en azul marino (#0C3452).
- **Franjas de acción (quiz, botones, contador):** naranja (#FF6602).
- **Un solo bloque en azul oscuro:** el de los casos, para que resalte.

## 8. Pendiente (decisiones del usuario)

1. Elegir el título (recomendado o alternativa).
2. Qué ofrece la página del libro, para el mensaje y el botón de la C.
3. ¿La C completa primero el form de Comunidad y después va al lead magnet?
   - Sí: se sigue midiendo cuántos C trae cada anuncio, y hay que cambiar la redirección del form de Comunidad en GHL.
   - No: va directo a la página.
   - Recomendado: form primero.
4. Fecha y hora de la próxima clase.
5. (Meta) Si Lead pasa a ser solo A + nivel alto, rearmar las audiencias de exclusión "PP - Leads registrados 15D/30D" y "n8n — Leads registrados 180d" con CompleteRegistration. Hoy se arman con Lead.

## 9. Archivos de base

- **Landing actual (04/11):** `landing-siempre-on/clase-04-noviembre/index-popup.html` e `index.html`.
  - Salen de `clase-21-octubre/` con `build-desde-clase-21.py`.
  - El quiz está al final del archivo (`/* ─── QUIZ ─── */`). El ruteo usa `resp.etapa`; los forms de GHL están en `CONFIG.FORM_ID` (A/B) y `CONFIG.FORM_COMUNIDAD_ID` (C).
- **Thank you de registro:** `nfm-clase-paga/thankyou-oto.html`. Solo dispara PageView; la conversión la manda GHL por CAPI.
- **Píxel de Meta:** 1203017011123382, adentro del bloque de custom code, con guarda para no duplicar.
- **Pasos de cada clase nueva:** `landing-siempre-on/clase-04-noviembre/LEEME.md` (fecha, UTM, grupo de WhatsApp, calendario, portal de beneficios).
