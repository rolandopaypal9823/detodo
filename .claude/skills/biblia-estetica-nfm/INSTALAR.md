# Instalar la skill `biblia-estetica-nfm`

Ya quedó instalada en este entorno (`~/.claude/skills/biblia-estetica-nfm/`) y versionada en el
repo (`.claude/skills/biblia-estetica-nfm/`). Esto es para instalarla en otro lado.

## En Claude Code (tu máquina)

**Global — disponible en todos tus proyectos:**

```bash
cp -r .claude/skills/biblia-estetica-nfm ~/.claude/skills/
```

**Solo para un proyecto:**

```bash
mkdir -p /ruta/al/proyecto/.claude/skills
cp -r .claude/skills/biblia-estetica-nfm /ruta/al/proyecto/.claude/skills/
```

En los dos casos, Claude Code la levanta al arrancar la sesión. Verificás con `/skills`.

## En claude.ai / Claude Desktop

Subí `biblia-estetica-nfm.zip` (está en la raíz del repo) en Configuración → Capacidades → Skills.
El zip ya tiene el `SKILL.md` en la raíz, que es lo que espera el uploader.

## Cómo se dispara

Sola, cuando el pedido tiene que ver con diseñar o mejorar una pieza de NFM. También podés
llamarla a mano:

```
/biblia-estetica-nfm
```

## Qué trae

```
biblia-estetica-nfm/
├── SKILL.md                        ← la regla de oro y los no negociables
├── references/
│   ├── tokens.md                   ← paleta, tipografía, escala, radios, sombras, motion, :root
│   ├── componentes.md              ← botones, cards, badges, stats, framer, marquee, cita
│   └── recetas.md                  ← azul elegante, red neuronal, shimmer, vidrio, reveals
└── assets/
    ├── biblia-estetica.html        ← la referencia viva (abrila en el navegador)
    ├── logo-nfm-navy.png
    └── logo-nfm-blanco.png
```
