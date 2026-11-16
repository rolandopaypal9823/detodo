# Orden para armar mi reporte semanal (10 al 16/11)

**Tarea:** con el contexto de abajo, armá mi reporte semanal para el equipo y dirección. Va en cuatro partes:
1. Qué ejecuté.
2. Resultados y datos.
3. Criterios y aprendizajes para compartir.
4. Pendientes y próximos pasos, con dueño.

**Formato:** corto, con bullets y una o dos tablas. Español rioplatense, directo. Sin frases del tipo "no es X, es Y". Para Nico y el Instituto se dice "mente" o "cerebro", nunca "cabeza".

**Reglas de los datos:**
- Usá solo los números de abajo, sin inventar.
- Las proyecciones van marcadas como estimación.
- Lo que dice "a confirmar" preguntámelo antes de darlo por hecho.

---

## Contexto

Soy el responsable de marketing de Nicolás Fernández Miranda / Instituto de Productividad.

**Embudo:** anuncios de Meta → landing de registro → clase en vivo gratuita → agenda de llamada → llamada con un closer.

**Programas:**
- Gold: USD 1.500 a 1.800.
- Platinum: USD 3.600.
- Comunidad Productiva: plan barato.

El registro tiene una pregunta de etapa, A, B o C, y una pregunta de equipo a cargo, que define el nivel alto o medio.

## 1. Qué ejecuté

1. **Análisis de ventas de los lanzamientos del 22/09 (bueno) y el 04/11 (flojo).** Crucé tres fuentes:
   - 178 llamadas de Fathom, más 13 de octubre;
   - los registros del form de GHL;
   - la configuración real de Meta.
2. **Conversión de Meta:** solo cuentan las etapas A y B. GHL manda Lead por la API de Conversiones desde el "Form AGOSTO NUEVO", con una sola acción.
3. **Etapa C:** ya no entra a la clase. Va al lead magnet hackeatuvida.netlify.app, con UTMs, y el pixel manda un evento `EtapaC` solo para medir.
4. **Landing nueva para la clase del lunes 16/11:** "Dejá de sobrecargarte con todo y armá un sistema de neurociencia que lo sostenga", con la clase "Neurociencia para el Alto Rendimiento Profesional".
   - Bloques: para quién es y para quién no, historia de Nico en carrusel, la escalera "Armá tu sistema de productividad" (habilidades técnicas, bienestar físico, bienestar mental), casos y cierre.
   - El quiz de etapas quedó sin cambios.
5. **Piezas de apoyo de la clase:**
   - thank you sin asientos premium, con el grupo de WhatsApp nuevo;
   - link de Google Calendar y archivo .ics;
   - QR de Calendly con `utm_source=clase1611` y `clase1111`.
6. **Auditoría de la landing contra el perfil Platinum.** Cuánto aparece cada tema en las llamadas de compradores Platinum: foco 100%, vacaciones 94%, decisiones 83%, hábitos 83%, delegar 61%, IA 39%.
7. **Landing de la Comunidad (versión VSL):**
   - reloj diario hasta las 19:00 de Argentina, que se reinicia solo;
   - barra fija arriba con el contador;
   - redirección a la sala de espera (clase-instituto-productividad.netlify.app/sala.html), que se configura en el "Form Webinar Comunidad" de GHL.
8. **Análisis de los registros del 16/11**, comparativa con todas las clases desde que se usan las etapas, y un reporte visual para el equipo (`reportes/calidad-leads-etapas-16nov.png`).

## 2. Resultados y datos

**Por qué el 04/11 trajo peores leads:** el tráfico cambió y la landing era la misma.
- Meta optimizaba por CompleteRegistration, que se mandaba también para la C.
- Se abrieron ubicaciones baratas.
- Se excluyó a todos los que ya se habían registrado.
- El mismo anuncio pasó de 35% de C en septiembre a 66% en noviembre.

**Lo que dicen las ventas:**
- La etapa C dio 0 Platinum.
- El que paga Platinum es dueño o socio con equipo propio.
- De los A con equipo a cargo que agendan, el 14,8% compra Platinum.
- Los no cierres por plata fueron el 64% el 22/09 y el 81% el 04/11.

**Calidad de los registros A y B por clase** (sin duplicados ni pruebas):

| | 22/09 | 07/10 | 21/10 | 04/11 | **16/11** |
|---|---|---|---|---|---|
| Registrados | 1.634 | 2.935 | 1.984 | 2.129 | **1.959** |
| Con equipo a cargo | 71,5% | 64,3% | 61,8% | 58,8% | **75,3%** |
| Dueños que son A con equipo | 4,8% | 5,1% | 4,8% | 3,4% | **6,4% (126)** |
| Dueños y gerentes | 28,8% | 24,8% | 24,8% | 20,6% | **32,9%** |
| Docentes | 10,2% | 9,3% | 10,1% | 11,3% | **5,2%** |

- El 16/11 es la clase más calificada desde que usamos las etapas.
- La parte de A con equipo a cargo quedó igual que el 22/09 (27%). Lo que creció es B con equipo a cargo, que pasó del 35% al 48%.
- Las profesiones principales del 16/11 son gerentes y directores (20%) y dueños (13%). Después vienen arquitectura e ingeniería, administración, ventas y docentes.

**Proyección de la clase del 16/11 (estimación):**
- Embudo: 1.200 en el grupo de WhatsApp → 420 asisten (35%) → 63 agendan (15% de los que asisten) → 38 se presentan (60%) → 11 cierres (30%).
- Facturación según el ticket:
  - todo a ticket promedio USD 1.000: USD 11.340;
  - con 2 o 3 Platinum, que es lo esperable: USD 16.200 a 18.800;
  - techo con todo Platinum: USD 40.824.
- Es lo vendido, no lo cobrado.

## 3. Criterios para compartir

- **La calidad del lead la decide más el tráfico que la landing.** Meta tiene que optimizar por el evento que representa al cliente (A y B), nunca por cualquier registro.
- **La pregunta de etapa filtra bien y no se toca**, ni una palabra.
- **El copy filtra por contexto, no por dolor.**
  - Funciona nombrar el equipo, que todo pasa por vos y las vacaciones con el celular.
  - El dolor genérico (no tengo tiempo, procrastino) lo dicen igual el que paga y el que no puede.
- **Evitar el idioma del que no puede pagar:** ganar más, despegar, conseguir clientes, ingreso extra.
- **Medir la calidad por perfil**, como el porcentaje con equipo a cargo y los dueños A, y no por volumen de registros.
- **Un buen registro todavía no es una venta:** la prueba son las agendas y los cierres.

## 4. Pendientes

- Cargar las agendas, presentaciones y cierres del 16/11 y compararlos con el 22/09. **(Yo, esta semana)**
- Aplicar las 5 mejoras de la auditoría de la landing:
  - separar delegación de decisiones;
  - una línea de curiosidad;
  - usar las palabras de los leads en lugar de "multitasking";
  - "Tenés un equipo propio" en "Para quién es";
  - el aviso del quiz.
- Confirmar con Nico que la clase toca delegación e IA.
- **En GHL (a confirmar si ya quedó):**
  - un solo Lead por CAPI, verificado en Probar eventos;
  - la redirección del form de la Comunidad a la sala de espera;
  - el link de Zoom actualizado en zoom-nfm.netlify.app.
- **En Meta:**
  - mirar el evento `EtapaC` para contar cuántas C trae cada anuncio;
  - rearmar las audiencias de exclusión, que hoy se arman con Lead.
- Ajustar el mensaje para la C cuando sepamos qué ofrece la página del lead magnet.
