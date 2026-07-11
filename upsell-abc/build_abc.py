# -*- coding: utf-8 -*-
"""El ABC del Alto Rendimiento — página de curso estilo 'classroom' (tema oscuro neuronal).

Director de arte (skill awesome-design):
- ESQUELETO: Mintlify (layout de aprendizaje: sidebar de navegación + panel principal;
  item activo resaltado; densidad legible).
- PIEL: NFM en su versión OSCURA — fondo abismo #06192b con red neuronal animada (canvas),
  Naranja Acción #ff6602 como único acento, Montserrat + Open Sans + JetBrains Mono (labels),
  marco de video con glow y esquinas. Estética tomada de la Masterclass de Neurociencia.

Comportamiento: el sidebar lista los 5 módulos con sus lecciones; al hacer clic en una
lección, su video (Loom/YouTube) se carga en el reproductor principal. Progreso por módulo
y global, "marcar visto", prev/next, recuerda la última lección vista.

Uso:  python3 build_abc.py   →  index.html (autocontenido; logo embebido en base64)
"""
import os
import re
import json
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_WHITE = os.path.join(HERE, "assets", "logo-blanco.png")

# ---- Contenido (inventario del classroom) -----------------------------------
# lesson: (título, tipo, id/url, es_apunte📒)   tipo ∈ {loom, yt}
# recurso: (título, tipo, url|None)             tipo ∈ {pdf, yt, ig, book, test, link}
MODULES = [
    {
        "emoji": "🧠", "title": "Mindset",
        "tagline": "La mentalidad que sostiene todo lo demás.",
        "sections": [
            {"name": "Mentalidad de crecimiento", "lessons": [
                ("La importancia del Mindset", "loom", "80a07d9f14444d5abf6e73471a1191c5", True),
                ("El lenguaje no es inocente", "loom", "5cae3c64ec744a49b177f2354782855b", True),
            ]},
            {"name": "Tips", "lessons": [
                ("El Observador", "loom", "8f6c57e9bda34b88b818753bfc8dd20f", True),
                ("Parálisis por análisis", "loom", "2bb1130d54c54567a639b1b4205b171c", False),
            ]},
        ],
        "recursos": [("Entregable N° 2 — Mindset", "pdf",
            "https://files.skool.com/f/4dca09fb7b19431287f225e6d0625278/293842b474374a4d9542f0f8c7fabc29aebdbcbe3f5442ad9d7202d754dab9e7?Expires=1783823005&Signature=HdYPfm7Pnax06PSADrphwnOfKhddPPTHMPSc~Amr0GvPl9Z1DUkufv5CsmI5-fMVWKSzz2IQzaCnEZ1ZKTfDJ1WBmxHnovNUnusSyqE0AIFtF2pvA0NkdG8KwCJUUcVzI7UVXzFQsKfHe9po4ILJNGl3z4dezE7H0BhENcQrFValNYu0b4l1gFj6oNod9ppUu-~C5a9g3H5y8fhLDl-vYVunXZmyxi8Koyv7L3HWqnYTbg1Fa5lPkamFm1cz4gmlDSNgcVAq83vAW0PxOLaDVTX4qSbC~C-4tQWHxQuE3wcPd2MJ4iD0osU~OFn5K-2ju~1b3EaTvnuTUzDTMdmTQQ__&Key-Pair-Id=K1UMNJVTUVQ48Y")],
    },
    {
        "emoji": "🔁", "title": "Hábitos",
        "tagline": "Tus acciones definen tu futuro.",
        "sections": [
            {"name": "Introducción", "lessons": [
                ("Tus acciones definen tu futuro", "loom", "42eb232d7ea84e3a99caaf2ff6aa3181", False),
            ]},
            {"name": "¿Cómo se forman los hábitos?", "lessons": [
                ("¿Por qué se forman los hábitos?", "loom", "33c174cfc47e41ea80eb92529241255c", False),
                ("Señal · Rutina · Recompensa", "loom", "4b72a1950eb947fb90160bb85b883c2b", False),
            ]},
            {"name": "Y ahora..?", "lessons": [
                ("¿Cómo mantener los hábitos?", "loom", "fafe046896ac4253b0d769a67e2bf1e3", False),
                ("Vision Board", "loom", "c54a1b7d94a04c03a1f4ec7d4c7f4cce", True),
            ]},
        ],
        "recursos": [
            ("Planillas Hábitos", "pdf",
             "https://files.skool.com/f/4dca09fb7b19431287f225e6d0625278/70b49578a0784ecdabaf41052871048b0b3d3fd57d864720ae70adc06238867d?Expires=1783823283&Signature=ErHZIRySc967woxJ~ByDBTwy3iya4U1t-wEWLqeTBeBFyUFrbOkC4kEWo9MlBhWLaSyx6~e6DGdz68mcJ2fLiCa1qv2EGhSZ3HPS3Th9tbLu1hdawa5VZznrCWIIf50m5fsDaxVvHKewGXDI-tSKEr1weNT74cnPwb4cBwVRdXnbkTZ8OcDpSNXQn0g2JmBBmRNIfVoTfjhBsgIwBjmOgfVz6aaQLRT7PPD0fxZ5d4WcUvNy1nICRiyk0rlWxulOrXqNEKTGPiW26icxegSQsWgGMmjN9jMxpYUz~gr~o5sTk~qBEBnVOgc9zuye5jRHsZI1hagRNQrM4qKNlbPFnA__&Key-Pair-Id=K1UMNJVTUVQ48Y"),
            ("Cómo crear imágenes con IA", "yt", "https://www.youtube.com/watch?v=Azvtojs11Tg"),
        ],
    },
    {
        "emoji": "😴", "title": "Sueño y Descanso",
        "tagline": "Dormís mejor, rendís mejor. No es negociable.",
        "sections": [
            {"name": "Introducción", "lessons": [
                ("Píldora Mágica", "loom", "0e75571cc9ad45aca7bebe38ba163832", False),
                ("¿Para qué dormimos?", "loom", "f05f4595c4c1420bb4323cf262e40fdf", False),
                ("¿Y si duermo menos?", "loom", "199a77d9a9764aa38a730cfe51d186f0", False),
                ("Cantidad y calidad", "loom", "a5e4cccff8334fbc925790ef98c8860f", False),
            ]},
            {"name": "¿Cómo duermo mejor?", "lessons": [
                ("Rutina nocturna", "loom", "7e274053b4064cca80f5884a1ac09f47", False),
                ("Rutina matutina", "loom", "87a97912bbc648f3b6c94fb49bf4e794", False),
            ]},
            {"name": "Para tener en cuenta", "lessons": [
                ("Dormir aumenta la productividad marginal", "loom", "584ca1a08b37433983b0e8d4672c20df", False),
            ]},
        ],
        "recursos": [
            ("Modo noche en iOS", "yt", "https://www.youtube.com/watch?v=75ei1QWSgEc"),
            ("Modo noche en Android", "yt", "https://www.youtube.com/shorts/D-OHiqpYKqQ"),
            ("Descanso profundo · NSDR", "yt", "https://www.youtube.com/watch?v=jPvBJh--AXY"),
            ("HIIT · Rutinas de ejercicios (canal)", "yt", "https://www.youtube.com/@PFAlejoMarino"),
            ("Entregable N° 6 — Sueño y Descanso", "pdf",
             "https://files.skool.com/f/4dca09fb7b19431287f225e6d0625278/cdd70587791248b9b78851edb40eff961e47f08eb15342a9a47c68e86484b3f6?Expires=1783823211&Signature=SF6hRdKkRub7Wch4gtvMXnEe8GnCG-on7lDOX9mebOJNdIETefebDIqh-EF9LgOQHt~Mqami4uVHd45am2RJfs1mQfoloBup~KU5Q-spfstAGacdyM~oE0b7TNOoUUuXlHBLvjYQbTv6UuB6ujYjDeqLKm~DnBnPrsPpii8m6Szgj~ABzmvvhCI3LbunGxpF3Vy1x8VaBRFmtMtvLvTdHleM1RfQE59Xm15oM8ASUjPwc5XsbAdJ7GpgHnlZdBDqetMiVTT0jW-Rrg2EpQsRZDb2uNPj5IECjz-WfgXghnOH~CsbnLqnKCJkFz20fATEtyaGB6VnWQr7CcExWyk3hw__&Key-Pair-Id=K1UMNJVTUVQ48Y"),
        ],
    },
    {
        "emoji": "🍎", "title": "Ejercicio y Alimentación",
        "tagline": "El cuerpo es el envase del cerebro.",
        "sections": [
            {"name": "Alimentación", "lessons": [
                ("Alimentación y productividad", "loom", "352b83cc02c84fcb88cc523276c0eefb", False),
                ("El método de la glucosa", "loom", "c4495b75439f4479bab97226fcb585df", False),
                ("¿Y cómo funciona?", "loom", "536f1445d7524b6c8e2ef57c8a0a63de", False),
                ("¿Cuáles son los efectos?", "loom", "d698af731108472cbf82dda5214e592f", False),
                ("¿Cómo disminuirlos?", "loom", "954de4db93f347d5bff728bd9facc244", False),
            ]},
            {"name": "Ejercicio", "lessons": [
                ("No todo es lectura!", "loom", "456683ba632d4d3085f4275a76afc463", False),
                ("A moverse", "loom", "9d7294088dbe4b118908c4e92e39b81c", False),
            ]},
        ],
        "recursos": [
            ("Entregable N° 7 — Ejercicio y Alimentación", "pdf",
             "https://files.skool.com/f/4dca09fb7b19431287f225e6d0625278/89185f014ba247a7a1e9f0a2f0927c24d4420a8ea74c46c2ad56a65c99b133b4?Expires=1783823253&Signature=EDiHN4E5aPEhSXJ6PJXwACe62BHAL~gMqRu79AGT8fAZfLqVvfpxIIDZ1ssZdjFmnocc5qqL0jZcLGwjTepZ~7LLwta80s7h6Hhbu80E4yYY2dnUggCkzSV4B6O2ZmnNVU~GNQA32hAZABQoHJVrfe7iPBmHE~kp4~jKVOvGonexmEPYddOj0j-jZ5RcM0x3ov~gULM~wLiv~RSCuuPWirKREncgVfe2yvE8JMIsXTquUZftQ0OcNIIcUkNTjpG89x9-QJhpvf~cPrpD7hACXcP1yrTkXTut8RWnZPlOvdvNDloqCU-ewL~RBmzH2i-MB2WI~~Qsdy~i04UqMtUp-w__&Key-Pair-Id=K1UMNJVTUVQ48Y"),
            ("Instagram · La diosa de la glucosa", "ig", "https://www.instagram.com/glucosegoddess/"),
            ("Instagram · Dr. Marcelo Suárez", "ig", "https://www.instagram.com/doctormarcelosuarez/"),
            ("Libro · La Revolución de la Glucosa", "book", "https://www.mercadolibre.com.ar/"),
        ],
    },
    {
        "emoji": "🎯", "title": "Concentración",
        "tagline": "Entrená el foco como se entrena un músculo.",
        "sections": [
            {"name": "Concentración", "lessons": [
                ("Contribución marginal", "loom", "05ed09cc04254ad78fe1c78712b4ec71", False),
            ]},
            {"name": "Componentes de la concentración", "lessons": [
                ("¿De qué me sirve saber esto?", "loom", "990d98e9747a4b8f902099d194a9ec88", False),
                ("El estado de alerta", "loom", "64645f53e1f0486da8597e2207a25e29", False),
                ("¿Cómo gestionar tu estado de alerta?", "loom", "9a21d3ba57614c91bb52aa4024c79cc8", False),
                ("¿Y si estás exaltado?", "loom", "921dbc6026654579865ee7b19feb3daf", False),
                ("La orientación", "loom", "2fc80854caa348d0aa9d1b77b5279e6c", True),
                ("La capacidad ejecutiva", "loom", "dd531748927c4267a6d64e9f29492913", False),
            ]},
            {"name": "Tips", "lessons": [
                ("Perlitas de la concentración", "loom", "e8160959aeb1452889fdb7271f58dd53", False),
            ]},
        ],
        "recursos": [
            ("Test ciclo circadiano", "test", "https://www.um.es/cronobiologia/"),
            ("Test de cronotipo", "test", "https://sleepdoctor.com/sleep-quizzes/chronotype-quiz/"),
            ("Cómo bloquear aplicaciones (Android)", "yt", "https://www.youtube.com/watch?v=c8_S1T8_tPo"),
            ("Tiempo en pantalla (iPhone)", "yt", "https://www.youtube.com/watch?v=t_UfArksQJg"),
            ("StayFocusd · extensión de Chrome", "link", "https://chromewebstore.google.com/detail/laankejkbhbdhmipfmgcngdelahlfoji"),
            ("Pantalla en blanco y negro (iPhone)", "yt", "https://www.youtube.com/watch?v=tFCufew50Oo"),
            ("Pantalla en blanco y negro (Android)", "yt", "https://www.youtube.com/watch?v=jp9r64-JkBw"),
            ("Entregable N° 3 — Concentración", "pdf",
             "https://files.skool.com/f/4dca09fb7b19431287f225e6d0625278/7b5dd52050f748a6b01311154e8158fc40c93a33525b42a3bfe63b1902af0f39?Expires=1783823137&Signature=exEjpSgp722vpWIVjRAkYFykvDYIP92iRGsKr1~TLF41nJY3GBlz8u7ZaVORToeVczrQfgfICnC2QLcqQ6Wx101m1sPSV7ezTdaePtGKRhG-sT2~TZ5rTF-GVHg93jFAUm~6LoMIrhtIwLxSZCtmXRRBRMy4CBgfzKf4UBDLAbz7h5pXGhdfLvYRZIiVPaAScT-dzHJSoBT9mbMY6FjyFtzcEIMMgoAwawwIGw8wuhuJ8hs1YVf6s0UKIt2WAxve5jt1wvZ1p5YkTD36KvhLaSbABE8IvL5suO-RYGwChB5iM93UjnHJITLX3B9FItUcbtbdIQXm6kFcnTGFQ1abuQ__&Key-Pair-Id=K1UMNJVTUVQ48Y"),
        ],
    },
    {
        "emoji": "💾", "title": "Memoria",
        "tagline": "La metahabilidad: aprender a recordar.",
        "sections": [
            {"name": "Memoria", "lessons": [
                ("Metahabilidad", "loom", "69b46cdb65b34c7f8d50689974181ba1", False),
                ("La memoria se entrena", "loom", "6d64e9ab5572453fb52cb3db23d5fb55", False),
            ]},
            {"name": "Subprocesos", "lessons": [
                ("¿Qué es la memoria?", "loom", "a196bed22d63418c9881856c16341f01", False),
                ("La codificación de la información", "loom", "fe71f6d4121d4ee1b309c3f0bdfc620a", False),
                ("El almacenamiento de la información", "loom", "0e9f21d7c01044b6b059af682ce9f36d", False),
                ("La evocación de la información", "loom", "468a299434754ed0928fe46a4c8caca8", False),
            ]},
            {"name": "Tips", "lessons": [
                ("La regla de oro", "loom", "f0057f60aa22430aa4712f6b84e05adc", False),
                ("Cómo recordar el nombre de las personas", "loom", "894af9366bff4bdab11fb359580099d0", True),
                ("Técnicas de memorización", "loom", "6322ab4094384d7284d9537e7b58b238", True),
                ("Bonus · técnica de memoria", "yt", "TMIpkQvy2tM", False),
            ]},
        ],
        "recursos": [
            ("El mágico número 7 (inglés · PDF)", "pdf",
             "https://labs.la.utexas.edu/gilden/files/2016/04/MagicNumberSeven-Miller1956.pdf"),
            ("El mágico número 7 (español)", "link", "https://www.academia.edu/"),
            ("La curva del olvido", "yt", "https://www.youtube.com/watch?v=hrGbwutALpA"),
            ("Entregable N° 4 — Memoria", "pdf",
             "https://files.skool.com/f/4dca09fb7b19431287f225e6d0625278/54a06c2a64ed4233b9f92cbf7fe9364aaf4644384e534132a57069f5c31ae106?Expires=1783823177&Signature=iEYnQnvTyavrqyixNdORh92l~KoT6S3j8jBI49loXqrSqY9W2DYbjJ15gR9qjkZqQKC1RJZjfaxp305yy1OjHP9kAdhWbB9-xYQTsfvXkLzoQ83OjfrWeGeeZ7cty~QgWMSp4EagxWe4Ud867eoLsv84OYZ8TirNwdBLi4mX8hYNZxF1wPvGSE99EMGIjxt3kqCElzyNOVFZOuGupOGT0VFeJkO2gEjNmv-QLSzLfV3rd5KcIdJiEviUFtn0QnK1wLJfnMxApx4Vlmk~3Fs~6jrFkcdNkgVpoAcdyWyh4oEPKY5NBCiBmRcgm0MeV8uP-Dj~DUMEz-4imHoWehBZ3g__&Key-Pair-Id=K1UMNJVTUVQ48Y"),
        ],
    },
]

RES_ICON = {"pdf": "📄", "yt": "▶", "ig": "📷", "book": "📕", "test": "🧪", "link": "🔗"}


def yt_id(s):
    m = re.search(r"(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{6,})", s)
    return m.group(1) if m else s


def embed_url(kind, ref):
    if kind == "loom":
        return "https://www.loom.com/embed/" + ref
    if kind == "yt":
        return "https://www.youtube.com/embed/" + yt_id(ref)
    return ref


def count_videos(mod):
    return sum(len(s["lessons"]) for s in mod["sections"])


TOTAL_VIDEOS = sum(count_videos(m) for m in MODULES)


def b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def build_data():
    lessons = []
    sidebar_parts = []
    for mi, mod in enumerate(MODULES):
        nvid = count_videos(mod)
        sidebar_parts.append(
            f'<div class="s-mod open" data-mod="{mi}">'
            f'<button class="s-mhead" aria-expanded="true">'
            f'<span class="s-emoji">{mod["emoji"]}</span>'
            f'<span class="s-mtitle">{mod["title"]}</span>'
            f'<span class="s-mprog"><b class="s-seen">0</b>/{nvid}</span>'
            f'<span class="s-chev">⌄</span></button>'
            f'<div class="s-mbody">'
        )
        li = 0
        for sec in mod["sections"]:
            sidebar_parts.append(f'<div class="s-sec">{sec["name"]}</div>')
            for (title, kind, ref, note) in sec["lessons"]:
                lid = f"m{mi}-l{li}"
                li += 1
                emb = embed_url(kind, ref)
                lessons.append({
                    "id": lid, "m": mi, "mtitle": mod["title"], "emoji": mod["emoji"],
                    "sec": sec["name"], "title": title, "type": kind, "embed": emb, "note": note,
                })
                badge = '<span class="s-badge" title="Incluye apunte">📒</span>' if note else ""
                sidebar_parts.append(
                    f'<button class="s-lesson" data-id="{lid}">'
                    f'<span class="s-dot" data-seen="{lid}" title="Marcar como visto"></span>'
                    f'<span class="s-ltitle">{title}{badge}</span></button>'
                )
        sidebar_parts.append("</div></div>")
    return lessons, "".join(sidebar_parts)


def build_resources_js():
    res = []
    for mod in MODULES:
        items = []
        for (t, kind, url) in mod.get("recursos", []):
            items.append({"t": t, "icon": RES_ICON.get(kind, "🔗"), "url": url,
                          "locked": url is None})
        res.append(items)
    return res


# ---- Fondo de red neuronal (canvas). Braces sin doblar: va como parámetro. ---
NEURAL_JS = r"""
(function(){
  try{
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var canvas = document.getElementById("neuralbg");
    if(canvas && !reduce){
      var ctx = canvas.getContext("2d");
      var dpr = Math.min(window.devicePixelRatio||1, 2);
      var LINK = 152, rand=function(a,b){return Math.random()*(b-a)+a;};
      var w,h,nodes=[],edges=[],signals=[],glows=[],rt;
      function build(){
        w=innerWidth; h=innerHeight;
        canvas.width=w*dpr; canvas.height=h*dpr; canvas.style.width=w+"px"; canvas.style.height=h+"px";
        ctx.setTransform(dpr,0,0,dpr,0,0);
        var count=Math.max(40, Math.min(150, Math.round(w*h/16000)));
        nodes=[];
        for(var i=0;i<count;i++){var x=Math.random()*w,y=Math.random()*h;
          nodes.push({x:x,y:y,bx:x,by:y,r:rand(1,2.2),flash:0,nbr:[]});}
        edges=[];
        for(var a=0;a<nodes.length;a++){for(var b=a+1;b<nodes.length;b++){
          var dx=nodes[a].bx-nodes[b].bx,dy=nodes[a].by-nodes[b].by,d=Math.hypot(dx,dy);
          if(d<LINK){edges.push([a,b,d]);nodes[a].nbr.push(b);nodes[b].nbr.push(a);}}}
        glows=[];
        for(var k=0;k<3;k++) glows.push({x:rand(.18,.82)*w,y:rand(.08,.5)*h,r:rand(300,480),ph:Math.random()*6.28,sp:rand(.05,.12)});
        signals=[];
      }
      function step(){
        requestAnimationFrame(step);
        ctx.clearRect(0,0,w,h);
        for(var g=0;g<glows.length;g++){ var G=glows[g]; G.ph+=G.sp*0.02;
          var gx=G.x+Math.cos(G.ph)*40, gy=G.y+Math.sin(G.ph*1.3)*30;
          var rg=ctx.createRadialGradient(gx,gy,0,gx,gy,G.r);
          rg.addColorStop(0,"rgba(18,68,108,0.20)"); rg.addColorStop(1,"rgba(18,68,108,0)");
          ctx.fillStyle=rg; ctx.beginPath(); ctx.arc(gx,gy,G.r,0,6.2832); ctx.fill(); }
        for(var n0=0;n0<nodes.length;n0++){ if(nodes[n0].flash>0) nodes[n0].flash-=0.035; }
        for(var e=0;e<edges.length;e++){ var A=nodes[edges[e][0]],B=nodes[edges[e][1]];
          var al=0.10*(1-edges[e][2]/LINK);
          ctx.strokeStyle="rgba(122,182,225,"+al.toFixed(3)+")"; ctx.lineWidth=1;
          ctx.beginPath(); ctx.moveTo(A.x,A.y); ctx.lineTo(B.x,B.y); ctx.stroke(); }
        for(var n=0;n<nodes.length;n++){ var N=nodes[n]; var fl=N.flash;
          ctx.fillStyle="rgba(150,196,232,"+(0.22+fl*0.6).toFixed(3)+")";
          ctx.beginPath(); ctx.arc(N.x,N.y,N.r+fl*1.6,0,6.2832); ctx.fill();
          if(fl>0.15){ var r=12+fl*16, hg=ctx.createRadialGradient(N.x,N.y,0,N.x,N.y,r);
            hg.addColorStop(0,"rgba(255,102,2,"+(fl*0.38).toFixed(3)+")"); hg.addColorStop(1,"rgba(255,102,2,0)");
            ctx.fillStyle=hg; ctx.beginPath(); ctx.arc(N.x,N.y,r,0,6.2832); ctx.fill(); } }
        for(var i=signals.length-1;i>=0;i--){ var s=signals[i]; s.p+=s.sp;
          var sa=nodes[s.from],sb=nodes[s.to]; if(!sa||!sb){signals.splice(i,1);continue;}
          var x=sa.x+(sb.x-sa.x)*s.p, y=sa.y+(sb.y-sa.y)*s.p;
          var pg=ctx.createRadialGradient(x,y,0,x,y,7);
          pg.addColorStop(0,"rgba(255,142,44,0.9)"); pg.addColorStop(.4,"rgba(255,102,2,0.5)"); pg.addColorStop(1,"rgba(255,102,2,0)");
          ctx.fillStyle=pg; ctx.beginPath(); ctx.arc(x,y,7,0,6.2832); ctx.fill();
          ctx.fillStyle="rgba(255,196,130,0.95)"; ctx.beginPath(); ctx.arc(x,y,1.6,0,6.2832); ctx.fill();
          if(s.p>=1){ sb.flash=1; signals.splice(i,1);
            if(s.gen<3 && Math.random()<0.72){ var nb=sb.nbr.filter(function(j){return j!==s.from;});
              if(nb.length) signals.push({from:s.to,to:nb[(Math.random()*nb.length)|0],p:0,sp:s.sp,gen:s.gen+1}); } } }
      }
      build();
      addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(build,180);});
      function spawnRandom(){
        if(!nodes.length || signals.length>8) return;
        var i=(Math.random()*nodes.length)|0; var nb=nodes[i].nbr;
        if(nb.length) signals.push({from:i,to:nb[(Math.random()*nb.length)|0],p:0,sp:rand(.005,.010),gen:0});
      }
      setInterval(spawnRandom, 1600);
      step();
    }
  }catch(err){ if(window.console) console.warn("neural bg:", err); }
})();
"""


def build():
    lessons, sidebar_html = build_data()
    resources = build_resources_js()
    logo_white = b64(LOGO_WHITE)

    html = PAGE.format(
        logo_white=logo_white,
        n_modules=len(MODULES), n_videos=TOTAL_VIDEOS,
        sidebar=sidebar_html,
        lessons_json=json.dumps(lessons, ensure_ascii=False),
        resources_json=json.dumps(resources, ensure_ascii=False),
        neural_js=NEURAL_JS,
    )
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK — {out}  ({len(MODULES)} módulos · {TOTAL_VIDEOS} lecciones)")


PAGE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>El ABC del Alto Rendimiento · NFM</title>
<meta name="description" content="Curso El ABC del Alto Rendimiento — Mindset, Hábitos, Ejercicio y Alimentación, Concentración y Memoria. Por Nico Fernández Miranda.">
<meta name="color-scheme" content="dark">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧠</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Open+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#06192b;--bg-2:#04111d;--abismo:#06192b;
  --navy:#0c3452;--navy2:#123f63;
  --orange:#ff6602;--orange-hi:#ff8124;--orange-hover:#ff7a1f;
  --hueso:#f3f7fb;--niebla:#9fb6c8;--niebla-2:#6f8aa1;
  --hair:rgba(255,255,255,.10);--hair-2:rgba(255,255,255,.16);
  --surface:rgba(255,255,255,.03);--surface-2:rgba(255,255,255,.05);
  --active:rgba(255,102,2,.13);--active-line:rgba(255,102,2,.5);
  --glow:rgba(255,102,2,.30);
  --shadow:0 24px 60px -20px rgba(0,0,0,.65);
  --ease:cubic-bezier(.16,1,.3,1);
  --topbar-h:60px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{font-family:'Open Sans',-apple-system,system-ui,sans-serif;color:var(--niebla);line-height:1.6;
  background:linear-gradient(180deg,#08243c 0%,var(--bg) 46%,var(--bg-2) 100%);min-height:100vh;overflow-x:hidden}}
h1,h2,h3,h4,.font-h{{font-family:'Montserrat',sans-serif}}
.mono{{font-family:'JetBrains Mono',monospace}}
a{{color:var(--orange);text-decoration:none}}
::selection{{background:var(--orange);color:#fff}}
/* ---------- fondo red neuronal ---------- */
#neuralbg{{position:fixed;inset:0;z-index:-3;display:block}}
#neural-mask{{position:fixed;inset:0;z-index:-2;pointer-events:none;
  background:radial-gradient(130% 100% at 50% 12%, transparent 34%, rgba(6,25,43,.86) 100%)}}
/* ---------- topbar ---------- */
.topbar{{height:var(--topbar-h);background:rgba(8,30,48,.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  position:sticky;top:0;z-index:60;display:flex;align-items:center;justify-content:space-between;padding:0 20px;border-bottom:1px solid var(--hair)}}
.topbar .left{{display:flex;align-items:center;gap:14px;min-width:0}}
.topbar img{{height:30px;display:block;filter:drop-shadow(0 2px 10px rgba(0,0,0,.4))}}
.topbar .crumb{{color:var(--niebla-2);font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-left:1px solid var(--hair);padding-left:14px}}
.topbar .right{{display:flex;align-items:center;gap:14px}}
.tp-prog{{display:flex;align-items:center;gap:9px}}
.tp-prog .track{{width:120px;height:7px;background:rgba(255,255,255,.12);border-radius:5px;overflow:hidden}}
.tp-prog .track i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--orange),var(--orange-hi));box-shadow:0 0 10px rgba(255,102,2,.5);transition:width .5s var(--ease)}}
.tp-prog .pct{{color:var(--hueso);font-family:'Montserrat';font-weight:800;font-size:.82rem;min-width:34px;text-align:right}}
.burger{{display:none;background:rgba(255,255,255,.04);border:1px solid var(--hair-2);color:var(--hueso);border-radius:8px;width:38px;height:34px;font-size:1.1rem;cursor:pointer}}
/* ---------- shell ---------- */
.shell{{display:flex;align-items:flex-start}}
/* ---------- sidebar ---------- */
.sidebar{{flex:0 0 308px;width:308px;border-right:1px solid var(--hair);height:calc(100vh - var(--topbar-h));position:sticky;top:var(--topbar-h);overflow-y:auto;
  background:rgba(7,26,43,.66);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);padding:20px 14px 40px;scrollbar-width:thin;scrollbar-color:var(--hair-2) transparent}}
.sidebar::-webkit-scrollbar{{width:8px}}
.sidebar::-webkit-scrollbar-thumb{{background:var(--hair-2);border-radius:8px}}
.s-head{{padding:6px 8px 16px}}
.s-kicker{{color:var(--orange);font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;font-weight:500}}
.s-title{{font-family:'Montserrat';font-weight:800;color:var(--hueso);font-size:1.12rem;line-height:1.2;margin:6px 0 12px}}
.s-gprog{{display:flex;align-items:center;gap:9px}}
.s-gprog .track{{flex:1;height:8px;background:rgba(255,255,255,.06);border-radius:5px;overflow:hidden;border:1px solid var(--hair)}}
.s-gprog .track i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--orange),var(--orange-hi));box-shadow:0 0 8px rgba(255,102,2,.5);transition:width .5s var(--ease)}}
.s-gprog .pct{{font-family:'Montserrat';font-weight:800;color:var(--orange);font-size:.8rem;min-width:34px;text-align:right}}
.s-mod{{margin-top:6px;border-radius:10px}}
.s-mhead{{width:100%;display:flex;align-items:center;gap:10px;background:none;border:none;cursor:pointer;padding:10px 8px;border-radius:9px;font:inherit;color:var(--hueso);text-align:left}}
.s-mhead:hover{{background:var(--surface-2)}}
.s-emoji{{flex:0 0 30px;height:30px;border-radius:8px;background:linear-gradient(145deg,var(--navy2),var(--navy));border:1px solid var(--hair);display:flex;align-items:center;justify-content:center;font-size:1rem}}
.s-mtitle{{flex:1;min-width:0;font-family:'Montserrat';font-weight:700;font-size:.92rem;line-height:1.15}}
.s-mprog{{font-size:.62rem;color:var(--niebla-2);font-weight:600;white-space:nowrap;font-family:'JetBrains Mono',monospace}}
.s-mprog b{{color:var(--hueso)}}
.s-chev{{color:var(--niebla-2);font-size:1.1rem;transition:transform .28s var(--ease)}}
.s-mod.open .s-chev{{transform:rotate(180deg)}}
.s-mbody{{display:none;padding:2px 0 8px}}
.s-mod.open .s-mbody{{display:block}}
.s-sec{{font-family:'JetBrains Mono',monospace;font-weight:500;color:var(--niebla-2);font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;padding:12px 10px 5px}}
.s-lesson{{width:100%;display:flex;align-items:center;gap:10px;background:none;border:none;cursor:pointer;padding:8px 10px;border-radius:8px;font:inherit;color:var(--niebla);text-align:left;line-height:1.3;position:relative}}
.s-lesson:hover{{background:var(--surface-2)}}
.s-lesson.active{{background:var(--active)}}
.s-lesson.active::before{{content:"";position:absolute;left:0;top:6px;bottom:6px;width:3px;border-radius:3px;background:var(--orange);box-shadow:0 0 8px rgba(255,102,2,.7)}}
.s-lesson.active .s-ltitle{{color:var(--hueso);font-weight:700}}
.s-dot{{flex:0 0 16px;height:16px;border-radius:50%;border:2px solid var(--niebla-2);transition:all .2s;display:flex;align-items:center;justify-content:center}}
.s-dot::after{{content:"✓";color:#fff;font-size:.6rem;opacity:0;font-weight:700}}
.s-lesson.seen .s-dot{{background:#16a34a;border-color:#16a34a}}
.s-lesson.seen .s-dot::after{{opacity:1}}
.s-lesson.seen .s-ltitle{{color:var(--niebla-2)}}
.s-ltitle{{flex:1;min-width:0;font-size:.86rem}}
.s-badge{{margin-left:5px;font-size:.85em}}
/* ---------- main ---------- */
.main{{flex:1;min-width:0}}
.main-inner{{max-width:900px;margin:0 auto;padding:30px 30px 60px}}
.crumbs{{display:flex;align-items:center;gap:8px;font-size:.66rem;color:var(--niebla-2);font-family:'JetBrains Mono',monospace;font-weight:500;letter-spacing:.06em;text-transform:uppercase;margin-bottom:16px;flex-wrap:wrap}}
.crumbs .sep{{opacity:.5}}
.crumbs .c-mod{{color:var(--orange)}}
/* marco de video con glow + esquinas */
.player-wrap{{position:relative;border-radius:18px;padding:10px;background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.01));border:1px solid var(--hair-2);box-shadow:var(--shadow);
  opacity:0;transform:translateY(16px);transition:opacity .6s var(--ease),transform .6s var(--ease)}}
.player-wrap.in{{opacity:1;transform:none}}
.player-wrap::before{{content:"";position:absolute;inset:-2px;border-radius:20px;background:radial-gradient(60% 60% at 50% 0%, var(--glow), transparent 70%);z-index:-1;filter:blur(18px);opacity:.9}}
.frame{{position:relative;width:100%;padding-bottom:56.25%;height:0;background:#000;border-radius:12px;overflow:hidden}}
.frame iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.corner{{position:absolute;width:18px;height:18px;border:2px solid var(--orange);opacity:.75;z-index:2}}
.corner.tl{{top:3px;left:3px;border-right:0;border-bottom:0;border-radius:8px 0 0 0}}
.corner.tr{{top:3px;right:3px;border-left:0;border-bottom:0;border-radius:0 8px 0 0}}
.corner.bl{{bottom:3px;left:3px;border-right:0;border-top:0;border-radius:0 0 0 8px}}
.corner.br{{bottom:3px;right:3px;border-left:0;border-top:0;border-radius:0 0 8px 0}}
.lhead{{display:flex;align-items:flex-start;gap:16px;margin:24px 0 4px}}
.lhead h1{{flex:1;min-width:0;font-size:1.72rem;font-weight:800;color:var(--hueso);line-height:1.15;letter-spacing:-.01em}}
.ltag{{flex:0 0 auto;font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--niebla);font-weight:500;border:1px solid var(--hair-2);border-radius:999px;padding:6px 12px;margin-top:5px}}
.lactions{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:20px 0 8px}}
.btn-seen{{position:relative;display:inline-flex;align-items:center;gap:9px;background:var(--orange);color:#fff;border:none;border-radius:999px;font-family:'Montserrat';font-weight:700;font-size:.92rem;padding:13px 26px;cursor:pointer;box-shadow:0 16px 34px -12px var(--glow);transition:transform .18s var(--ease),background .18s,box-shadow .3s}}
.btn-seen:hover{{transform:translateY(-2px);background:var(--orange-hi);box-shadow:0 22px 44px -12px var(--glow)}}
.btn-seen .ck{{width:19px;height:19px;border-radius:50%;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:.66rem}}
.btn-seen.done{{background:#16a34a;box-shadow:0 16px 34px -12px rgba(22,163,74,.5)}}
.btn-seen.done .ck{{background:#fff;color:#16a34a}}
.nav-btns{{display:flex;gap:10px;margin-left:auto}}
.nav-btn{{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.04);border:1.5px solid var(--hair-2);color:var(--hueso);border-radius:999px;font-family:'Montserrat';font-weight:700;font-size:.84rem;padding:11px 18px;cursor:pointer;transition:border-color .18s,background .18s}}
.nav-btn:hover:not(:disabled){{border-color:var(--orange);background:rgba(255,102,2,.08)}}
.nav-btn:disabled{{opacity:.35;cursor:not-allowed}}
/* recursos */
.resources{{margin-top:34px;border-top:1px solid var(--hair);padding-top:24px}}
.reslabel{{font-family:'JetBrains Mono',monospace;font-weight:500;color:var(--niebla);font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px}}
.reslist{{display:grid;gap:8px}}
.res{{display:flex;align-items:center;gap:12px;padding:13px 15px;border:1px solid var(--hair);border-radius:12px;color:var(--hueso);font-weight:600;font-size:.94rem;background:var(--surface);transition:border-color .15s,box-shadow .2s,transform .15s,background .2s}}
a.res:hover{{border-color:var(--hair-2);background:var(--surface-2);box-shadow:var(--shadow);transform:translateY(-2px)}}
.res .ricon{{flex:0 0 34px;height:34px;border-radius:9px;background:rgba(255,255,255,.05);border:1px solid var(--hair);display:flex;align-items:center;justify-content:center;font-size:1rem}}
.res .rtx{{flex:1;min-width:0}}
.res .rarrow{{color:var(--orange);font-weight:800;font-size:1.1rem}}
.res-locked{{color:var(--niebla-2)}}
.res-locked .rtag{{font-family:'JetBrains Mono',monospace;font-size:.55rem;letter-spacing:.08em;text-transform:uppercase;color:var(--niebla-2);border:1px solid var(--hair);border-radius:999px;padding:4px 9px;font-weight:500}}
/* backdrop mobile */
.backdrop{{display:none;position:fixed;inset:var(--topbar-h) 0 0;background:rgba(4,15,26,.6);backdrop-filter:blur(2px);z-index:40}}
/* footer */
footer{{border-top:1px solid var(--hair);padding:26px 20px;text-align:center;font-size:.8rem;color:var(--niebla-2);background:rgba(4,15,26,.4)}}
footer .q{{font-family:'Montserrat';font-weight:700;color:var(--hueso);margin-bottom:4px}}
/* responsive */
@media(max-width:940px){{
  .burger{{display:block}}
  .tp-prog .track{{width:78px}}
  .sidebar{{position:fixed;top:var(--topbar-h);left:0;bottom:0;height:auto;z-index:50;transform:translateX(-104%);transition:transform .3s var(--ease);box-shadow:8px 0 34px rgba(0,0,0,.5);width:300px;flex-basis:300px;background:rgba(6,22,38,.96)}}
  .sidebar.open{{transform:none}}
  .backdrop.show{{display:block}}
  .main-inner{{padding:22px 18px 50px}}
  .lhead h1{{font-size:1.4rem}}
}}
@media(max-width:560px){{
  .topbar .crumb{{display:none}}
  .nav-btns{{margin-left:0;width:100%}}
  .nav-btn{{flex:1;justify-content:center}}
}}
@media (prefers-reduced-motion: reduce){{
  *{{animation-duration:.001s!important;transition-duration:.001s!important}}
  #neuralbg{{display:none}}
  .player-wrap{{opacity:1;transform:none}}
}}
</style>
</head>
<body>
<canvas id="neuralbg" aria-hidden="true"></canvas>
<div id="neural-mask" aria-hidden="true"></div>

<div class="topbar">
  <div class="left">
    <button class="burger" id="burger" aria-label="Abrir módulos">☰</button>
    <img src="{logo_white}" alt="NFM — Instituto de Productividad">
    <span class="crumb">El ABC del Alto Rendimiento</span>
  </div>
  <div class="right">
    <div class="tp-prog"><span class="track"><i id="tpbar"></i></span><span class="pct" id="tppct">0%</span></div>
  </div>
</div>

<div class="shell">
  <aside class="sidebar" id="sidebar">
    <div class="s-head">
      <div class="s-kicker">Curso · {n_modules} módulos · {n_videos} lecciones</div>
      <div class="s-title">El ABC del Alto Rendimiento</div>
      <div class="s-gprog"><span class="track"><i id="sbar"></i></span><span class="pct" id="spct">0%</span></div>
    </div>
    {sidebar}
  </aside>
  <div class="backdrop" id="backdrop"></div>

  <main class="main"><div class="main-inner">
    <div class="crumbs" id="crumbs"></div>
    <div class="player-wrap" id="playerWrap">
      <div class="frame" id="frame"></div>
      <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>
    </div>
    <div class="lhead"><h1 id="lTitle">—</h1><span class="ltag" id="lTag"></span></div>
    <div class="lactions">
      <button class="btn-seen" id="btnSeen"><span class="ck">✓</span><span id="btnSeenTx">Marcar como visto</span></button>
      <div class="nav-btns">
        <button class="nav-btn" id="prevBtn">← Anterior</button>
        <button class="nav-btn" id="nextBtn">Siguiente →</button>
      </div>
    </div>
    <div class="resources" id="resources"></div>
  </div></main>
</div>

<footer>
  <div class="q">"No es motivación, es ciencia."</div>
  <div>El ABC del Alto Rendimiento · Nico Fernández Miranda · Instituto de Productividad</div>
</footer>

<script>{neural_js}</script>
<script>
(function(){{
  var LESSONS={lessons_json};
  var RES={resources_json};
  var TOTAL={n_videos};
  var SEEN_KEY='abc_seen_v2', LAST_KEY='abc_last_v2';
  var seen={{}}; try{{seen=JSON.parse(localStorage.getItem(SEEN_KEY)||'{{}}')}}catch(e){{}}
  var byId={{}}; LESSONS.forEach(function(l){{byId[l.id]=l}});
  var order=LESSONS.map(function(l){{return l.id}});
  var current=null;

  var frame=document.getElementById('frame');
  var pw=document.getElementById('playerWrap');

  function esc(s){{return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;')}}

  function renderResources(mi){{
    var box=document.getElementById('resources');
    var items=RES[mi]||[];
    if(!items.length){{box.innerHTML='';return}}
    var html='<div class="reslabel">📎 Recursos y entregables</div><div class="reslist">';
    items.forEach(function(r){{
      if(r.locked){{
        html+='<div class="res res-locked"><span class="ricon">'+r.icon+'</span><span class="rtx">'+esc(r.t)+'</span><span class="rtag">PDF · en Skool</span></div>';
      }}else{{
        html+='<a class="res" href="'+r.url.replace(/&/g,'&amp;')+'" target="_blank" rel="noopener"><span class="ricon">'+r.icon+'</span><span class="rtx">'+esc(r.t)+'</span><span class="rarrow">→</span></a>';
      }}
    }});
    box.innerHTML=html+'</div>';
  }}

  function select(id, scroll){{
    var l=byId[id]; if(!l) return;
    current=id;
    pw.classList.remove('in');
    frame.innerHTML='<iframe src="'+l.embed+'" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe>';
    void pw.offsetWidth; pw.classList.add('in');
    document.getElementById('lTitle').innerHTML=esc(l.title)+(l.note?' <span title="Incluye apunte" style="font-size:.8em">📒</span>':'');
    document.getElementById('lTag').textContent=(l.type==='loom'?'Loom':'YouTube');
    document.getElementById('crumbs').innerHTML=
      '<span class="c-mod">'+l.emoji+' '+esc(l.mtitle)+'</span><span class="sep">›</span><span>'+esc(l.sec)+'</span>';
    renderResources(l.m);
    document.querySelectorAll('.s-lesson').forEach(function(b){{b.classList.toggle('active',b.dataset.id===id)}});
    var active=document.querySelector('.s-lesson[data-id="'+id+'"]');
    if(active){{var mod=active.closest('.s-mod'); if(mod && !mod.classList.contains('open')){{mod.classList.add('open');mod.querySelector('.s-mhead').setAttribute('aria-expanded','true')}}
      active.scrollIntoView({{block:'nearest'}});}}
    var sb=document.getElementById('btnSeen');
    var done=!!seen[id];
    sb.classList.toggle('done',done);
    document.getElementById('btnSeenTx').textContent=done?'Visto ✓':'Marcar como visto';
    var idx=order.indexOf(id);
    document.getElementById('prevBtn').disabled=idx<=0;
    document.getElementById('nextBtn').disabled=idx>=order.length-1;
    try{{localStorage.setItem(LAST_KEY,id)}}catch(e){{}}
    if(scroll!==false){{document.querySelector('.main-inner').scrollIntoView({{block:'start',behavior:'smooth'}});}}
    closeDrawer();
  }}

  function save(){{try{{localStorage.setItem(SEEN_KEY,JSON.stringify(seen))}}catch(e){{}}}}
  function refresh(){{
    var done=0;
    document.querySelectorAll('.s-mod').forEach(function(mod){{
      var ls=mod.querySelectorAll('.s-lesson'),c=0;
      ls.forEach(function(b){{var s=!!seen[b.dataset.id];b.classList.toggle('seen',s);if(s)c++}});
      done+=c;
      var sc=mod.querySelector('.s-seen'); if(sc)sc.textContent=c;
    }});
    var pct=TOTAL?Math.round(done/TOTAL*100):0;
    ['sbar','tpbar'].forEach(function(idb){{var b=document.getElementById(idb);if(b)b.style.width=pct+'%'}});
    ['spct','tppct'].forEach(function(idp){{var p=document.getElementById(idp);if(p)p.textContent=pct+'%'}});
  }}
  function toggleSeen(id){{
    if(seen[id])delete seen[id]; else seen[id]=1;
    save();refresh();
    if(id===current){{
      var done=!!seen[id];
      document.getElementById('btnSeen').classList.toggle('done',done);
      document.getElementById('btnSeenTx').textContent=done?'Visto ✓':'Marcar como visto';
    }}
  }}

  document.querySelectorAll('.s-lesson').forEach(function(b){{
    b.addEventListener('click',function(e){{
      if(e.target.closest('.s-dot')){{toggleSeen(b.dataset.id);e.stopPropagation();return}}
      select(b.dataset.id);
    }});
  }});
  document.querySelectorAll('.s-dot').forEach(function(d){{
    d.addEventListener('click',function(e){{e.stopPropagation();toggleSeen(d.dataset.seen)}});
  }});
  document.querySelectorAll('.s-mhead').forEach(function(h){{
    h.addEventListener('click',function(){{
      var m=h.closest('.s-mod');var op=m.classList.toggle('open');
      h.setAttribute('aria-expanded',op?'true':'false');
    }});
  }});
  document.getElementById('btnSeen').addEventListener('click',function(){{if(current)toggleSeen(current)}});
  document.getElementById('prevBtn').addEventListener('click',function(){{var i=order.indexOf(current);if(i>0)select(order[i-1])}});
  document.getElementById('nextBtn').addEventListener('click',function(){{var i=order.indexOf(current);if(i<order.length-1)select(order[i+1])}});
  var sidebar=document.getElementById('sidebar'),backdrop=document.getElementById('backdrop');
  function closeDrawer(){{sidebar.classList.remove('open');backdrop.classList.remove('show')}}
  document.getElementById('burger').addEventListener('click',function(){{
    var op=sidebar.classList.toggle('open');backdrop.classList.toggle('show',op);
  }});
  backdrop.addEventListener('click',closeDrawer);

  refresh();
  var last=null; try{{last=localStorage.getItem(LAST_KEY)}}catch(e){{}}
  select((last&&byId[last])?last:order[0], false);
}})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
