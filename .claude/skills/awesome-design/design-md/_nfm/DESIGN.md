---
version: 1.0
name: NFM-design-system
description: Sistema de diseño de Nicolás Fernández Miranda (NFM) / Instituto de Productividad. Marca de divulgación de neurociencia y alto rendimiento, anti-hype y anti-vendehumo, con rigor académico. El lenguaje visual se ancla en dos voltajes: Azul NFM (#0c3452) como base institucional seria — rigor, profundidad, salud mental — y Naranja Acción (#ff6602) como el único color de activación, reservado para CTAs y acentos que exigen atención inmediata (activación neuronal, energía, movimiento). El blanco es espacio de respiro y foco. Titulares en Montserrat Bold (impactante, moderno, legible, en mayúsculas o Title Case); cuerpo en Open Sans Regular (limpio, accesible). El idioma es español rioplatense. NUNCA usar dos naranjas ni saturar de naranja: es un acento, no un fondo. Elementos gráficos propios: Vector de Crecimiento (flechas ascendentes = siempre hay un nivel siguiente), marcos/encuadres (FRAMER), señaladores (POINTER) y texturas sutiles (TEXTURE).

colors:
  # Primarios oficiales
  primary: "#ff6602"            # Naranja Acción — CTAs, acentos, atención inmediata. ÚNICO color de activación.
  ink: "#0c3452"               # Azul NFM — textos principales, fondos institucionales, comunicación formal
  canvas: "#ffffff"            # Blanco NFM — espacios de respiro, fondo claro por defecto
  on-primary: "#ffffff"        # texto sobre naranja
  on-dark: "#ffffff"           # texto sobre azul/oscuro

  # Derivados sugeridos (mantienen la identidad sin inventar voltajes nuevos)
  primary-hover: "#e65a00"     # naranja un punto más profundo para hover/active
  primary-soft: "#fff1e8"      # naranja muy lavado para fondos de acento sutiles
  ink-hover: "#0a2a42"         # azul más profundo para hover sobre azul
  ink-700: "#1b4565"           # azul intermedio para superficies oscuras secundarias
  ink-300: "#5b7488"           # azul desaturado para texto secundario sobre claro
  body: "#3a4a57"              # gris-azulado para cuerpo de texto sobre blanco
  muted: "#6b7a86"             # texto terciario / metadatos
  hairline: "#e3e8ec"          # bordes y divisores sobre claro
  surface-soft: "#f5f7f9"      # superficie clara secundaria (cards, secciones)
  surface-dark: "#0c3452"      # superficie oscura = Azul NFM
  scrim: "#0c3452"             # overlays/scrims usan el azul, no negro puro

typography:
  # Titulares — Montserrat Bold
  display-xl:
    fontFamily: "'Montserrat', -apple-system, system-ui, sans-serif"
    fontWeight: 700
    fontSize: 56px
    lineHeight: 1.05
    letterSpacing: -0.02em
    case: "Title Case o MAYÚSCULAS"
  display-lg:
    fontFamily: "'Montserrat', sans-serif"
    fontWeight: 700
    fontSize: 40px
    lineHeight: 1.1
    letterSpacing: -0.015em
  heading:
    fontFamily: "'Montserrat', sans-serif"
    fontWeight: 700
    fontSize: 28px
    lineHeight: 1.2
    letterSpacing: -0.01em
  subheading:
    fontFamily: "'Montserrat', sans-serif"
    fontWeight: 600
    fontSize: 20px
    lineHeight: 1.3
  # Cuerpo — Open Sans Regular
  body-lg:
    fontFamily: "'Open Sans', -apple-system, system-ui, sans-serif"
    fontWeight: 400
    fontSize: 18px
    lineHeight: 1.6
  body:
    fontFamily: "'Open Sans', sans-serif"
    fontWeight: 400
    fontSize: 16px
    lineHeight: 1.6
  caption:
    fontFamily: "'Open Sans', sans-serif"
    fontWeight: 400
    fontSize: 13px
    lineHeight: 1.5
    color: "muted"
  cta-label:
    fontFamily: "'Montserrat', sans-serif"
    fontWeight: 700
    fontSize: 16px
    letterSpacing: 0.01em
    case: "Title Case"

radius:
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  pill: 999px      # botones CTA y badges suelen ir en pill

spacing:
  scale: "múltiplos de 4px (4, 8, 12, 16, 24, 32, 48, 64, 96)"
  section-padding: "96px vertical en desktop, 56px en mobile"
  content-max-width: "1120px"
  rhythm: "generoso — el blanco es un activo de marca, no rellenar por rellenar"

shadows:
  card: "0 1px 3px rgba(12,52,82,0.08), 0 8px 24px rgba(12,52,82,0.06)"   # sombras teñidas de azul, nunca negro puro
  cta: "0 8px 24px rgba(255,102,2,0.28)"                                   # glow naranja suave bajo el CTA principal
  elevated: "0 12px 40px rgba(12,52,82,0.12)"

motion:
  principle: "Movimiento con intención, nunca decorativo. Sugerir progreso ascendente (Vector de Crecimiento)."
  easing: "cubic-bezier(0.22, 1, 0.36, 1)  # ease-out expresivo"
  duration: "180–320ms en micro-interacciones; 600–900ms en entradas de sección"
  patterns:
    - "Fade + translate-Y ascendente en scroll-reveal (el contenido 'sube', refuerza el crecimiento)"
    - "CTA con glow naranja que respira sutilmente en hover"
    - "Contadores/números que cuentan hacia arriba al entrar en viewport"
    - "Líneas/flechas que se dibujan de abajo hacia arriba"

components:
  cta-primary:
    bg: "primary (#ff6602)"
    text: "on-primary (#ffffff)"
    radius: "pill"
    font: "cta-label (Montserrat 700)"
    shadow: "cta glow"
    hover: "bg primary-hover + leve scale(1.02) + glow más intenso"
    rule: "Solo UN CTA primario por pantalla/sección. Lo demás es secundario."
  cta-secondary:
    bg: "transparent"
    border: "1.5px solid ink"
    text: "ink"
    radius: "pill"
    hover: "bg ink, text on-dark"
  card:
    bg: "canvas o surface-soft"
    border: "1px solid hairline"
    radius: "lg (16px)"
    shadow: "card"
    accent: "borde o detalle naranja solo si la card es el foco"
  section-dark:
    bg: "ink (#0c3452) o surface-dark"
    text: "on-dark"
    use: "secciones de autoridad/cierre, citas, prueba social premium"
  badge:
    bg: "primary-soft"
    text: "primary"
    radius: "pill"
    font: "Montserrat 600, 12–13px"

brand_motifs:
  vector-de-crecimiento: "Flechas ascendentes / líneas que suben. Símbolo central: siempre hay un nivel siguiente."
  framer: "Marcos y encuadres que estructuran y jerarquizan el contenido."
  pointer: "Señaladores que dirigen la atención al elemento clave."
  texture: "Texturas sutiles que dan profundidad sin saturar; complementan fondos sólidos (sobre todo el azul)."

voice:
  language: "Español rioplatense (voseo)"
  tone: "Anti-hype, anti-vendehumo, científico pero conversacional. Rigor sin solemnidad."
  copy-rules:
    - "Nada que suene a IA ni a gurú de productividad."
    - "Nico = informal/comunidad; Nicolás Fernández Miranda = formal/prensa; NFM = interno."
    - "Vocabulario: 'plata' (no 'dinero'), 'laburo', 'accionables', 'cortito y al pie'."

hard_rules:
  - "El naranja #ff6602 es el ÚNICO color de activación. No inventar segundos naranjas ni gradientes naranja-a-otro-color como protagonista."
  - "No saturar de naranja: es acento (CTAs, un dato clave), nunca fondo de página completo."
  - "Sombras y scrims teñidos de Azul NFM, no negro puro."
  - "Titulares SIEMPRE Montserrat; cuerpo SIEMPRE Open Sans. No mezclar otras fuentes."
  - "El blanco/respiro es parte de la identidad: no llenar cada pixel."
