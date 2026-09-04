#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las 3 versiones de TSL del Instituto de Productividad."""
import json, io, os

BASE = "/home/user/detodo"
SCR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tsl-assets")
NEURAL = open(SCR + "/neural.html", encoding="utf-8").read()
CASOS  = json.load(open(SCR + "/casos.json", encoding="utf-8"))
QUIZ   = open(SCR + "/quiz.html", encoding="utf-8").read()

CALENDLY = "https://calendly.com/nicolasfernandezmiranda/sesion-de-claridad-sma-clon-clon?primary_color=ff4b00"

# ══════════════════════════════════════════════════════════════════ HEAD + CSS
HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="No te falta información: te falta un método que trabaje a favor de tu cerebro. Instituto de Productividad — acompañamiento de 6 meses con base en neurociencia y aval universitario.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Open+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* =========================================================================
   __ROTULO__
   TSL (carta de venta sin video) · Instituto de Productividad
   Autocontenida: se pega tal cual en un widget HTML de GoHighLevel.
   Lo único editable está en el bloque CONFIG (al final del archivo).
   ========================================================================= */
:root{
  --nfm-blue:#0c3452; --nfm-blue-dark:#061d30; --nfm-blue-light:#e7edf2;
  --nfm-orange:#ff6602; --nfm-orange-hi:#ff8124; --nfm-orange-text:#c04a00;
  --nfm-orange-wash:#fff7f2; --nfm-white:#ffffff;
  --ink:#0c3452; --muted:#33536b; --mono-grey:#5c7286; --mono-grey-soft:#6b8296;
  --hair:rgba(12,52,82,.10); --hair-2:rgba(12,52,82,.16); --glow:rgba(255,102,2,.30);
  --ease:cubic-bezier(.16,1,.3,1); --maxw:1120px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Open Sans',sans-serif;color:var(--ink);background:var(--nfm-white);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden;min-height:100vh;position:relative}
h1,h2,h3{font-family:'Montserrat',sans-serif}
p{text-wrap:pretty}
img{max-width:100%;display:block}
a{color:inherit}
::selection{background:var(--nfm-orange);color:#fff}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.section{padding:84px 0;position:relative;scroll-margin-top:80px}
.center{text-align:center}

/* ---------- FONDO RED NEURONAL ---------- */
#neuralbg{position:fixed;inset:0;z-index:0;display:block;pointer-events:none}
section,footer.foot{position:relative;z-index:2}
#neural-mask{position:fixed;inset:0;z-index:0;pointer-events:none;
  background:radial-gradient(120% 88% at 50% 8%, rgba(255,255,255,0) 40%, rgba(255,255,255,.80) 100%)}

/* ---------- BARRA DE CARGA ---------- */
#loadbar{position:fixed;top:0;left:0;right:0;height:3px;z-index:70;pointer-events:none;opacity:1;transition:opacity .55s ease .25s}
#loadbar.done{opacity:0}
#loadbar .lf{height:100%;width:0;background:linear-gradient(90deg,var(--nfm-orange),var(--nfm-orange-hi));box-shadow:0 0 14px rgba(255,102,2,.55);position:relative;transition:width 1.1s cubic-bezier(.22,1,.36,1)}
#loadbar .lf::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.7),transparent);transform:translateX(-100%);animation:lfsheen 1s linear infinite}
@keyframes lfsheen{to{transform:translateX(100%)}}

/* ---------- REVEAL ---------- */
.fade-up{opacity:0;transform:translateY(24px);animation:fadeUpEnter .85s var(--ease) forwards}
.d1{animation-delay:.05s}.d2{animation-delay:.14s}.d3{animation-delay:.23s}.d4{animation-delay:.32s}.d5{animation-delay:.41s}
@keyframes fadeUpEnter{to{opacity:1;transform:none}}

/* ---------- EYEBROW ---------- */
.eyebrow{display:inline-flex;align-items:center;gap:9px;font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.2em;font-size:11px;font-weight:500;color:var(--nfm-orange-text);background:var(--nfm-orange-wash);border:1px solid rgba(255,102,2,.22);padding:8px 15px;border-radius:100px;margin-bottom:20px}

/* ---------- TÍTULOS ---------- */
h1{font-family:'Montserrat',sans-serif;font-weight:900;font-size:clamp(32px,5.4vw,58px);line-height:1.03;letter-spacing:-.022em;color:var(--nfm-blue);margin-bottom:22px;text-wrap:balance}
h1 .hl,.shimmer{color:var(--nfm-orange)}
.h2{font-family:'Montserrat',sans-serif;font-weight:900;font-size:clamp(28px,4.4vw,46px);line-height:1.06;letter-spacing:-.015em;margin-bottom:22px;color:var(--nfm-blue);text-wrap:balance}
.h2 .hl{color:var(--nfm-orange)}
.lead-2{font-size:clamp(17px,2.2vw,21px);color:var(--muted);max-width:780px;line-height:1.62}
.center .lead-2{margin-left:auto;margin-right:auto}
.sub{font-size:clamp(17px,2.3vw,21px);color:var(--muted);max-width:62ch;line-height:1.62;margin-bottom:14px}
.sub b{color:var(--nfm-blue)}

/* ---------- BOTONES ---------- */
.btn{position:relative;display:inline-flex;align-items:center;gap:10px;justify-content:center;font-family:'Montserrat',sans-serif;font-weight:800;font-size:17px;padding:18px 34px;border-radius:12px;border:none;cursor:pointer;text-decoration:none;overflow:hidden;transition:transform .16s var(--ease),box-shadow .16s,background .16s;line-height:1.1;text-align:center}
.btn-primary{background:var(--nfm-orange);color:#fff;box-shadow:0 14px 36px rgba(255,102,2,.32)}
.btn-primary:hover{transform:translateY(-2px);background:var(--nfm-orange-hi);box-shadow:0 20px 48px rgba(255,102,2,.42)}
.btn-lg{font-size:19px;padding:20px 40px}
.btn-sm{font-size:14px;padding:11px 20px;border-radius:10px}
.btn .arrow{transition:transform .18s var(--ease)}
.btn:hover .arrow{transform:translateX(4px)}
/* bloque de CTA que va después de cada widget */
.cta-block{text-align:center;margin-top:44px}
.cta-block .fine{margin-top:14px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mono-grey)}
.section--navy .cta-block .fine{color:#8ba2b6}

/* ---------- TOPBAR ---------- */
.topbar{position:sticky;top:0;z-index:60;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 24px;background:rgba(255,255,255,.86);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--hair)}
.brand{display:inline-flex;align-items:center;gap:11px;text-decoration:none}
.brand__logo{height:38px;width:auto;display:block}
.brand__wordmark{display:flex;flex-direction:column;line-height:1.04}
.brand__top{font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--mono-grey)}
.brand__bottom{font-family:'Montserrat',sans-serif;font-weight:900;font-size:15px;letter-spacing:-.01em;color:var(--nfm-blue)}
.topbar__cta .lbl-short{display:none}

/* ---------- HERO ---------- */
.hero{padding:74px 0 76px;position:relative}
.hero .wrap{max-width:900px}

/* ---------- NAVY ELEGANTE ---------- */
.section--navy{position:relative;isolation:isolate;overflow:hidden;background:radial-gradient(120% 90% at 18% 10%, rgba(23,70,109,.55), transparent 55%),radial-gradient(90% 80% at 88% 104%, rgba(255,102,2,.06), transparent 60%),linear-gradient(180deg,#0e3352 0%,#0c3452 45%,#061d30 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.06);border-top:1px solid rgba(255,255,255,.08);border-bottom:1px solid rgba(255,255,255,.08)}
.neural-local{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:0;pointer-events:none}
.section--navy>*:not(.neural-local){position:relative;z-index:1}
.section--navy .eyebrow{color:#ffd0ac;background:rgba(255,102,2,.14);border-color:rgba(255,255,255,.16)}
.section--navy .h2{color:#fff}
.section--navy .h2 .hl{color:var(--nfm-orange)}
.section--navy .lead-2{color:#9fb6c8}
.section--navy .lead-2 b{color:#fff}

/* ---------- QUÉ INCLUYE ---------- */
.bcards{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:34px;text-align:left}
.bcard{background:#fff;border:1px solid var(--hair);border-radius:16px;overflow:hidden;box-shadow:0 12px 32px rgba(12,52,82,.06);display:flex;flex-direction:column;transition:transform .18s,box-shadow .18s}
.bcard:hover{transform:translateY(-3px);box-shadow:0 20px 44px rgba(12,52,82,.1)}
.bcard__ph{position:relative;aspect-ratio:4/3;background:linear-gradient(150deg,#eef3f7,#dae5ee);overflow:hidden}
.bcard__body{padding:16px 18px 20px}
.bcard__tag{font-family:'JetBrains Mono';font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--nfm-orange-text);font-weight:500}
.bcard__body h3{font-weight:800;font-size:15px;color:var(--nfm-blue);margin:6px 0 6px}
.bcard__body p{font-size:13px;color:var(--muted);line-height:1.5}
.incl-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:18px;max-width:760px;margin-left:auto;margin-right:auto;text-align:left}
.ic{background:#fff;border:1px solid var(--nfm-blue-light);border-radius:14px;padding:24px 22px;display:flex;gap:14px;align-items:flex-start;box-shadow:0 12px 32px rgba(12,52,82,.06)}
.ic .mk{font-family:'Montserrat';font-weight:900;font-size:19px;color:var(--nfm-orange);flex:0 0 auto;line-height:1;margin-top:2px}
.ic h3{font-weight:800;font-size:16px;margin-bottom:6px;color:var(--nfm-blue)}
.ic p{font-size:13.5px;color:var(--muted);line-height:1.5}
/* collage de fotos reales */
.photo-slot{position:relative;overflow:hidden}
.collage{position:absolute;inset:0;display:grid;gap:3px;background:#fff}
.collage img{width:100%;height:100%;min-width:0;min-height:0;object-fit:cover;display:block}
.collage--1{grid-template-columns:1fr}
.collage--2{grid-template-columns:1fr;grid-template-rows:1fr 1fr}
.collage--3{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
.collage--3 img:first-child{grid-row:1 / -1}
.collage--4{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
[data-img="coach"] .collage img{object-position:center 38%}

/* ---------- AVAL UNIVERSITARIO ---------- */
.incl-feature{display:grid;grid-template-columns:1.12fr .88fr;margin:38px 0 0;background:#fff;border:1px solid var(--hair);border-left:5px solid var(--nfm-orange);border-radius:18px;overflow:hidden;box-shadow:0 30px 66px -20px rgba(12,52,82,.24);text-align:left}
.incl-feature__body{padding:44px 44px 46px}
.feat-badge{display:inline-flex;align-items:center;gap:8px;font-family:'JetBrains Mono';font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--nfm-orange-text);background:var(--nfm-orange-wash);border:1px solid rgba(255,102,2,.25);padding:7px 14px;border-radius:100px;margin-bottom:20px;font-weight:500}
.feat-title{font-family:'Montserrat';font-weight:900;font-size:clamp(25px,3.5vw,38px);line-height:1.07;color:var(--nfm-blue);margin-bottom:16px;letter-spacing:-.015em}
.feat-title .hl{color:var(--nfm-orange)}
.feat-lead{font-size:clamp(16px,1.9vw,18px);color:var(--muted);margin-bottom:22px;line-height:1.6;max-width:54ch}
.feat-lead b{color:var(--nfm-blue);font-weight:700}
.feat-list{list-style:none;display:grid;gap:12px}
.feat-list li{position:relative;padding-left:32px;font-size:15.5px;color:var(--nfm-blue);font-weight:600;line-height:1.4}
.feat-list li::before{content:"✓";position:absolute;left:0;top:0;width:21px;height:21px;border-radius:50%;background:var(--nfm-orange);color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;line-height:1}
.feat-legal{margin-top:20px;padding-top:14px;border-top:1px dashed var(--hair-2);font-size:11px;line-height:1.6;color:#5a6b7a}
.incl-feature__photo{position:relative;min-height:300px;background:linear-gradient(150deg,#eef3f7,#dae5ee);border-left:1px dashed var(--hair-2)}

/* ---------- CASOS ---------- */
.casos-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:38px;text-align:left}
.caso{background:#fff;border:1px solid var(--hair);border-radius:16px;overflow:hidden;box-shadow:0 12px 32px rgba(12,52,82,.07);display:flex;flex-direction:column;transition:transform .18s,box-shadow .18s}
.caso:hover{transform:translateY(-3px);box-shadow:0 22px 48px rgba(12,52,82,.13)}
.caso__thumb{position:relative;aspect-ratio:16/9;background:#0c3452;cursor:pointer;overflow:hidden;border:0;padding:0;width:100%;display:block}
.caso__thumb img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s var(--ease)}
.caso:hover .caso__thumb img{transform:scale(1.04)}
.caso__thumb::after{content:"";position:absolute;inset:0;background:rgba(12,52,82,.26)}
.caso__play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:54px;height:54px;border-radius:50%;background:var(--nfm-orange);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(255,102,2,.45);z-index:2;transition:transform .2s var(--ease)}
.caso__thumb:hover .caso__play{transform:translate(-50%,-50%) scale(1.08)}
.caso__play::after{content:"";border-left:16px solid #fff;border-top:10px solid transparent;border-bottom:10px solid transparent;margin-left:4px}
.caso__thumb iframe{position:absolute;inset:0;width:100%;height:100%;border:0;z-index:3}
.caso__body{padding:18px 20px 22px}
.caso__name{font-family:'Montserrat';font-weight:800;font-size:17px;color:var(--nfm-blue)}
.caso__perfil{font-family:'JetBrains Mono';font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--nfm-orange-text);margin:5px 0 10px;line-height:1.5}
.caso__frase{font-size:14px;color:var(--muted);line-height:1.55;font-style:italic}
.section--navy .caso{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.12)}
.section--navy .caso__name{color:#fff}
.section--navy .caso__perfil{color:#ffb27a}
.section--navy .caso__frase{color:#a9bfd0}

/* ---------- DECK DE SLIDES (versión C) ---------- */
.deck{max-width:1000px;margin:0 auto;position:relative}
.deck__stage{position:relative;overflow:hidden;border-radius:18px;background:#fff;border:1px solid var(--hair);box-shadow:0 34px 80px -24px rgba(12,52,82,.4);aspect-ratio:16/9}
.deck__track{display:flex;height:100%;transition:transform .55s var(--ease)}
.slide{flex:0 0 100%;height:100%;padding:44px 56px;display:flex;flex-direction:column;justify-content:center;overflow:hidden;text-align:center}
.slide__eyebrow{display:inline-flex;align-self:center;font-family:'JetBrains Mono';font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--nfm-orange-text);background:var(--nfm-orange-wash);border:1px solid rgba(255,102,2,.24);padding:6px 13px;border-radius:100px;margin-bottom:16px}
.slide__title{font-family:'Montserrat';font-weight:900;font-size:clamp(22px,2.9vw,34px);line-height:1.1;letter-spacing:-.018em;color:var(--nfm-blue);margin-bottom:10px}
.slide__title .hl{color:var(--nfm-orange)}
.slide__lead{font-size:clamp(14px,1.5vw,16.5px);color:var(--muted);line-height:1.55;max-width:62ch;margin:0 auto 20px}
.slide__lead b{color:var(--nfm-blue)}
.slide__grid{display:grid;gap:12px}
.slide__grid--3{grid-template-columns:repeat(3,1fr)}
.slide__grid--2{grid-template-columns:repeat(2,1fr)}
.sitem{background:#fff;border:1px solid var(--nfm-blue-light);border-radius:12px;padding:15px 16px;display:flex;gap:11px;align-items:flex-start;text-align:left}
.sitem .mk{font-family:'Montserrat';font-weight:900;font-size:15px;color:var(--nfm-orange);flex:0 0 auto;line-height:1.1}
.sitem h4{font-family:'Montserrat';font-weight:800;font-size:14px;color:var(--nfm-blue);margin-bottom:3px;line-height:1.25}
.sitem p{font-size:12.5px;color:var(--muted);line-height:1.45}
.slide--cta{align-items:center;text-align:center;justify-content:center;background:radial-gradient(120% 90% at 18% 10%, rgba(23,70,109,.55), transparent 55%),linear-gradient(180deg,#0e3352 0%,#0c3452 45%,#061d30 100%)}
.slide--cta .slide__title{color:#fff}
.slide--cta .slide__lead{color:#9fb6c8;margin-left:auto;margin-right:auto}
.slide--cta .slide__lead b{color:#fff}
.slide--cta .slide__eyebrow{align-self:center;color:#ffd0ac;background:rgba(255,102,2,.14);border-color:rgba(255,255,255,.16)}
.slide--cta .steps{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin:0 0 26px}
.slide--cta .st{display:flex;align-items:center;gap:9px;font-family:'JetBrains Mono';font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:#9fb6c8}
.slide--cta .st .b{width:24px;height:24px;border-radius:50%;background:var(--nfm-orange);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-family:'Montserrat';font-size:12px}
.slide--aval .feat-list{text-align:left;max-width:58ch;margin:0 auto}
.slide--aval .feat-list li{font-size:14px}
.slide--aval .feat-legal{text-align:left;max-width:82ch;margin:14px auto 0;font-size:10px}
/* navegación */
.deck__nav{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;border:1px solid var(--hair-2);background:rgba(255,255,255,.94);color:var(--nfm-blue);font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:5;transition:all .18s var(--ease);box-shadow:0 6px 20px rgba(12,52,82,.18)}
.deck__nav:hover{background:var(--nfm-orange);color:#fff;border-color:var(--nfm-orange)}
.deck__nav:disabled{opacity:.28;cursor:default}
.deck__nav:disabled:hover{background:rgba(255,255,255,.94);color:var(--nfm-blue);border-color:var(--hair-2)}
.deck__nav--prev{left:14px}
.deck__nav--next{right:14px}
.deck__bar{height:4px;background:var(--nfm-blue-light);border-radius:0 0 3px 3px;overflow:hidden;margin-top:-4px;position:relative;z-index:6}
.deck__bar span{display:block;height:100%;background:var(--nfm-orange);transition:width .5s var(--ease);border-radius:0 3px 3px 0}
.deck__foot{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:16px}
.deck__dots{display:flex;gap:8px}
.deck__dot{width:9px;height:9px;border-radius:50%;border:none;background:rgba(12,52,82,.2);cursor:pointer;padding:0;transition:all .2s var(--ease)}
.deck__dot.on{background:var(--nfm-orange);width:26px;border-radius:100px}
.deck__count{font-family:'JetBrains Mono';font-size:11px;letter-spacing:.16em;color:var(--mono-grey)}
.deck__count b{color:var(--nfm-blue)}
.section--navy .deck__count{color:#8ba2b6}
.section--navy .deck__count b{color:#fff}
.section--navy .deck__dot{background:rgba(255,255,255,.25)}
.section--navy .deck__dot.on{background:var(--nfm-orange)}
.section--navy .deck__bar{background:rgba(255,255,255,.14)}
.deck__hint{text-align:center;margin-top:12px;font-family:'JetBrains Mono';font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mono-grey)}
.section--navy .deck__hint{color:#7d97ac}

/* ---------- FEED VERTICAL (version D · tipo TikTok) ---------- */
body.feed-mode{overflow:hidden}
body.feed-mode .topbar{position:fixed;top:0;left:0;right:0}
.feed{height:100vh;height:100dvh;overflow-y:scroll;scroll-snap-type:y mandatory;scroll-behavior:smooth;-webkit-overflow-scrolling:touch;position:relative;z-index:2}
body.agd-lock .feed{overflow:hidden}
.fslide{min-height:100vh;min-height:100dvh;scroll-snap-align:start;scroll-snap-stop:always;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:96px 20px 34px;position:relative;text-align:center}
.fslide__in{width:100%;max-width:560px;margin:0 auto}
.fslide--navy{position:relative;isolation:isolate;overflow:hidden;background:radial-gradient(120% 90% at 18% 10%, rgba(23,70,109,.55), transparent 55%),radial-gradient(90% 80% at 88% 104%, rgba(255,102,2,.06), transparent 60%),linear-gradient(180deg,#0e3352 0%,#0c3452 45%,#061d30 100%)}
.fslide--navy>*:not(.neural-local){position:relative;z-index:1}
.fslide--navy .h2,.fslide--navy h1{color:#fff}
.fslide--navy .lead-2,.fslide--navy .sub{color:#9fb6c8}
.fslide--navy .lead-2 b,.fslide--navy .sub b{color:#fff}
.fslide--navy .eyebrow{color:#ffd0ac;background:rgba(255,102,2,.14);border-color:rgba(255,255,255,.16)}
.fslide h1{font-size:clamp(28px,7.6vw,42px)}
.fslide .h2{font-size:clamp(24px,6.6vw,34px);margin-bottom:14px}
.fslide .sub,.fslide .lead-2{font-size:clamp(15px,4.1vw,17px);margin-left:auto;margin-right:auto}
.fslide .btn{margin-top:24px;width:100%;max-width:400px}
/* lista compacta dentro de un slide */
.flist{display:grid;gap:9px;margin-top:18px;text-align:left}
.flist .fi{background:#fff;border:1px solid var(--nfm-blue-light);border-radius:12px;padding:12px 14px;display:flex;gap:11px;align-items:flex-start}
.fslide--navy .flist .fi{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)}
.flist .mk{font-family:'Montserrat';font-weight:900;font-size:14px;color:var(--nfm-orange);flex:0 0 auto;line-height:1.2}
.flist h4{font-family:'Montserrat';font-weight:800;font-size:14px;color:var(--nfm-blue);line-height:1.3}
.flist p{font-size:12.5px;color:var(--muted);line-height:1.42;margin-top:2px}
.fslide--navy .flist h4{color:#fff}
.fslide--navy .flist p{color:#a9bfd0}
.fslide .feat-list{text-align:left;margin-top:16px}
.fslide .feat-list li{font-size:14px}
.fslide--navy .feat-list li{color:#fff}
.fslide .feat-legal{text-align:left;margin-top:14px;font-size:10px}
.fslide--navy .feat-legal{color:#8ba2b6;border-top-color:rgba(255,255,255,.14)}
/* slide de caso */
.fcaso__thumb{position:relative;width:100%;aspect-ratio:16/9;border-radius:14px;overflow:hidden;border:0;padding:0;cursor:pointer;background:#0c3452;display:block;box-shadow:0 18px 44px rgba(0,0,0,.3)}
.fcaso__thumb img{width:100%;height:100%;object-fit:cover;display:block}
.fcaso__thumb::after{content:"";position:absolute;inset:0;background:rgba(12,52,82,.26)}
.fcaso__thumb .caso__play{z-index:2}
.fcaso__thumb iframe{position:absolute;inset:0;width:100%;height:100%;border:0;z-index:3}
.fcaso__name{font-family:'Montserrat';font-weight:900;font-size:20px;color:#fff;margin-top:16px}
.fcaso__perfil{font-family:'JetBrains Mono';font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#ffb27a;margin:6px 0 10px;line-height:1.5}
.fcaso__frase{font-size:15px;color:#c3d4e1;line-height:1.55;font-style:italic}
/* barra de progreso del feed */
.feed-bar{position:fixed;top:0;left:0;right:0;height:3px;background:rgba(12,52,82,.12);z-index:65}
.feed-bar span{display:block;height:100%;width:0;background:var(--nfm-orange);transition:width .25s linear}
.feed-count{position:fixed;right:14px;bottom:14px;z-index:65;font-family:'JetBrains Mono';font-size:10px;letter-spacing:.14em;color:#fff;background:rgba(6,29,48,.6);backdrop-filter:blur(6px);padding:6px 11px;border-radius:100px;pointer-events:none}
.feed-hint{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);font-family:'JetBrains Mono';font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mono-grey);display:flex;flex-direction:column;align-items:center;gap:5px}
.fslide--navy .feed-hint{color:#8ba2b6}
.feed-hint .ar{font-size:15px;animation:fbounce 1.6s infinite}
@keyframes fbounce{0%,100%{transform:translateY(0)}50%{transform:translateY(5px)}}
@media(max-width:640px){
  .fslide{padding:88px 18px 30px}
  .fslide .flist p{font-size:12px}
}

/* ---------- CIERRE ---------- */
.apply{text-align:center}
.apply h2{font-weight:900;font-size:clamp(28px,4.6vw,48px);line-height:1.04;margin-bottom:20px;max-width:800px;margin-left:auto;margin-right:auto;color:var(--nfm-blue)}
.apply h2 .hl{color:var(--nfm-orange)}
.apply p{font-size:18px;color:var(--muted);max-width:640px;margin:0 auto 18px}
.apply p b{color:var(--nfm-blue)}
.apply .steps{display:flex;justify-content:center;gap:22px;flex-wrap:wrap;margin:30px 0 34px}
.apply .st{display:flex;align-items:center;gap:10px;font-family:'JetBrains Mono';font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.apply .st .b{width:26px;height:26px;border-radius:50%;background:var(--nfm-orange);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-family:'Montserrat'}
.section--navy.apply h2{color:#fff}
.section--navy.apply p{color:#9fb6c8}
.section--navy.apply p b{color:#fff}
.section--navy.apply .st{color:#9fb6c8}
.apply--wash{background:linear-gradient(180deg,#fff 0%,var(--nfm-orange-wash) 100%);border-top:1px solid var(--hair)}
/* el quiz de casos va sobre un tinte suave para separarse de la seccion clara de arriba */
.quiz-wrap{position:relative;z-index:2;background:linear-gradient(180deg,#fff 0%,#f2f6fa 55%,#eef3f8 100%);border-top:1px solid var(--hair)}

/* ---------- FOOTER ---------- */
.foot{background:rgba(255,255,255,.94);backdrop-filter:blur(6px);border-top:1px solid var(--hair);padding:42px 0;text-align:center}
.foot .brand{justify-content:center;margin-bottom:16px}
.foot small{font-size:11px;font-family:'JetBrains Mono';letter-spacing:.14em;text-transform:uppercase;color:#546a7e}

/* ---------- RESPONSIVE ---------- */
@media(max-width:980px){
  .bcards{grid-template-columns:repeat(2,1fr)}
  .casos-grid{grid-template-columns:repeat(2,1fr)}
  .incl-feature{grid-template-columns:1fr}
  .incl-feature__photo{min-height:220px;border-left:0;border-top:1px dashed var(--hair-2);order:-1}
  .incl-feature__body{padding:34px 28px 36px}
  .deck__stage{aspect-ratio:auto}
  .slide{padding:34px 30px}
  .slide__grid--3{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:640px){
  .section{padding:60px 0}
  .hero{padding:52px 0 56px}
  .bcards{grid-template-columns:1fr;max-width:420px;margin-left:auto;margin-right:auto}
  .casos-grid{grid-template-columns:1fr;max-width:420px;margin-left:auto;margin-right:auto}
  .incl-grid{grid-template-columns:1fr;max-width:420px}
  .topbar__cta .lbl-full{display:none}
  .topbar__cta .lbl-short{display:inline}
  .btn-lg{font-size:17px;padding:17px 26px;width:100%;max-width:420px}
  .slide{padding:28px 22px}
  .slide__grid--3,.slide__grid--2{grid-template-columns:1fr}
  .deck__nav{width:38px;height:38px;font-size:16px}
  .deck__nav--prev{left:8px}.deck__nav--next{right:8px}
  .slide--cta .steps{gap:12px}
}
</style>
</head>
<body id="top">

<div id="loadbar"><div class="lf"></div></div>
<canvas id="neuralbg" aria-hidden="true"></canvas>
<div id="neural-mask" aria-hidden="true"></div>

<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="ipNavy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#17466d"/><stop offset="1" stop-color="#0c3452"/></linearGradient>
    <linearGradient id="ipOrange" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#ff6602"/><stop offset="1" stop-color="#ff9440"/></linearGradient>
  </defs>
  <symbol id="ip-logo" viewBox="0 0 132 112">
    <ellipse cx="65" cy="99" rx="53" ry="4.5" fill="#0c3452" opacity=".10"/>
    <rect x="24" y="60" width="21" height="37" rx="4" fill="url(#ipNavy)"/>
    <rect x="53" y="44" width="21" height="53" rx="4" fill="url(#ipNavy)"/>
    <rect x="82" y="28" width="21" height="69" rx="4" fill="url(#ipNavy)"/>
    <path d="M16 84 C 40 92, 52 68, 68 54 C 84 40, 100 28, 114 16" fill="none" stroke="url(#ipOrange)" stroke-width="9" stroke-linecap="round"/>
    <path d="M114 16 L98 20 M114 16 L111 35" fill="none" stroke="url(#ipOrange)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
</svg>

<header class="topbar">
  <a href="#top" class="brand">
    <svg class="brand__logo" viewBox="0 0 132 112" role="img" aria-label="Instituto de Productividad"><use href="#ip-logo"/></svg>
    <span class="brand__wordmark"><span class="brand__top">Instituto de</span><span class="brand__bottom">Productividad</span></span>
  </a>
  <a href="#" class="btn btn-primary btn-sm topbar__cta" onclick="agdOpen('topbar');return false"><span class="lbl-full">Agendar entrevista</span><span class="lbl-short">Agendar</span><span class="arrow">→</span></a>
</header>
"""

# ══════════════════════════════════════════════════════════════════ BLOQUES
def cta(origen, texto="Agendar mi entrevista de admisión", fine="Sin costo · Entrevista 1 a 1 con el equipo de admisión"):
    f = '\n    <div class="fine">%s</div>' % fine if fine else ''
    return """    <div class="cta-block">
      <a href="#" class="btn btn-primary btn-lg" onclick="agdOpen('%s');return false">%s <span class="arrow">→</span></a>%s
    </div>""" % (origen, texto, f)


def casos_cards(n=None):
    items = CASOS if n is None else CASOS[:n]
    out = []
    for c in items:
        out.append("""      <article class="caso">
        <button type="button" class="caso__thumb" data-yt="%s" aria-label="Ver la entrevista de %s">
          <img src="https://img.youtube.com/vi/%s/hqdefault.jpg" alt="Entrevista a %s" loading="lazy">
          <span class="caso__play" aria-hidden="true"></span>
        </button>
        <div class="caso__body">
          <div class="caso__name">%s</div>
          <div class="caso__perfil">%s</div>
          <p class="caso__frase">%s</p>
        </div>
      </article>""" % (c['yt'], c['nombre'], c['yt'], c['nombre'], c['nombre'], c['perfil'], c['frase']))
    return "\n".join(out)


SEC_CASOS = """
<!-- CASOS · testimonios reales -->
<section class="section section--navy" id="casos">
  <div class="wrap center">
    <div class="center"><span class="eyebrow">Casos reales</span></div>
    <h2 class="h2">No es teoría: es gente que <span class="hl">ya lo hizo</span></h2>
    <p class="lead-2">Profesionales, líderes y dueños de negocio que dejaron de correr atrás del día y recuperaron el control de su tiempo, su energía y sus objetivos. Cada uno con nombre, oficio y su entrevista completa.</p>
    <div class="casos-grid">
__CARDS__
    </div>
__CTA__
  </div>
</section>
"""

SEC_INCLUYE = """
<!-- QUÉ INCLUYE -->
<section class="section__NAVY__" id="incluye">
  <div class="wrap center">
    <div class="center"><span class="eyebrow">Qué incluye</span></div>
    <h2 class="h2">Qué incluyen los programas del <span class="hl">Instituto de Productividad</span></h2>
    <p class="lead-2">Todo lo que ponemos del otro lado —dentro de nuestros procesos— para que esta vez tus objetivos sí avancen. Un profesional por cada frente, no un PDF y suerte.</p>

    <div class="bcards">
      <div class="bcard">
        <div class="bcard__ph photo-slot" data-img="coach" data-alt="Sesión de acompañamiento 1 a 1 del Instituto"></div>
        <div class="bcard__body"><span class="bcard__tag">01 · Incluido</span><h3>Tu coach dedicada, 1 a 1</h3><p>La persona del otro lado esperándote: te conoce, te sigue de cerca y no te deja aflojar. Lo que los alumnos valoran por encima de todo (8.8/10).</p></div>
      </div>
      <div class="bcard">
        <div class="bcard__ph photo-slot" data-img="modulos" data-alt="Plataforma del curso El ABC del Alto Rendimiento"></div>
        <div class="bcard__body"><span class="bcard__tag">02 · Incluido</span><h3>Biblioteca de +20 módulos</h3><p>El método completo, ordenado y secuencial. Píldoras cortas y accionables, no teoría.</p></div>
      </div>
      <div class="bcard">
        <div class="bcard__ph photo-slot" data-img="llamadas" data-alt="Clase en vivo del Instituto de Productividad"></div>
        <div class="bcard__body"><span class="bcard__tag">03 · Incluido</span><h3>Llamadas grupales en vivo</h3><p>Encuentros con Nico y el equipo para resolver tu caso real, y aprender de los compañeros.</p></div>
      </div>
      <div class="bcard">
        <div class="bcard__ph photo-slot" data-img="comunidad" data-alt="Comunidad del Instituto de Productividad"></div>
        <div class="bcard__body"><span class="bcard__tag">04 · Incluido</span><h3>Comunidad + mastermind presencial</h3><p>Gente con tu carga y tu oficio, que no juzga y acompaña — incluido el mastermind presencial en Buenos Aires.</p></div>
      </div>
    </div>

    <div class="incl-grid">
      <div class="ic"><span class="mk">05</span><div><h3>Equipo multidisciplinario</h3><p>Psicólogos, nutricionistas y coaches de alto rendimiento: un profesional por cada frente de tu vida y tu operación, no un solo referente para todo.</p></div></div>
      <div class="ic"><span class="mk">06</span><div><h3>Método y sistemas listos para usar</h3><p>Biblioteca de módulos accionables + Habit Tracker y Second Brain para sacarte la carga de la cabeza. Copiás, adaptás, aplicás.</p></div></div>
    </div>
__CTA__
  </div>
</section>
"""

SEC_AVAL = """
<!-- AVAL UNIVERSITARIO -->
<section class="section__NAVY__" id="aval">
  <div class="wrap">
    <div class="center"><span class="eyebrow">El respaldo</span></div>
    <h2 class="h2 center">Lo que casi ningún programa te puede mostrar</h2>
    <p class="lead-2 center" style="max-width:62ch;margin-left:auto;margin-right:auto">Esto es lo que separa al Instituto de "un curso más".</p>
    <div class="incl-feature">
      <div class="incl-feature__body">
        <span class="feat-badge">★ El diferencial · Respaldo académico</span>
        <h3 class="feat-title">Tu sistema, con <span class="hl">aval universitario</span></h3>
        <p class="feat-lead">No es una constancia por asistir. La versión <b>Platinum</b> se certifica de forma conjunta con la <b>Facultad de Ciencias Económicas de la Universidad Nacional de Jujuy (UNJu)</b>: un trayecto de 250 horas con evaluación y un trabajo final aplicado a tu propia vida o negocio. Se gana, no se regala — y por eso pesa distinto en tu CV, tu LinkedIn y frente a quien sea.</p>
        <ul class="feat-list">
          <li>Trayecto de 250 horas certificado por la Facultad, con evaluación y trabajo final</li>
          <li>Certificado digital emitido y firmado por la Facultad, con mecanismo de verificación</li>
          <li>Exclusivo de la versión Platinum · Certificación optativa</li>
        </ul>
        <p class="feat-legal">El certificado es emitido por la Facultad de Ciencias Económicas de la Universidad Nacional de Jujuy en el marco de un programa de certificación conjunta con NFM Productivity S.A.S. La certificación universitaria es optativa, exige requisitos académicos de aprobación y no constituye título universitario de grado ni de posgrado, ni acredita equivalencias automáticas.</p>
      </div>
      <figure class="incl-feature__photo photo-slot" data-img="certificados" data-alt="Alumnos del Instituto de Productividad con su certificado"></figure>
    </div>
__CTA__
  </div>
</section>
"""

SEC_CIERRE = """
<!-- CIERRE -->
<section class="section apply__CLASE__" id="agendar">
  <div class="wrap">
    <div class="center"><span class="eyebrow">El siguiente paso</span></div>
    <h2>¿Dónde vas a estar <span class="hl">en un año</span> si nada cambia?</h2>
    <p>Si no hacés algo distinto, en uno, dos o tres años vas a seguir en el mismo lugar. Y eso se traduce en concreto: <b>potencial que sabés que podés dar y no estás dando</b>, oportunidades que pasan de largo, calidad de vida, ingresos, tiempo con tu familia, tu salud.</p>
    <p>Todos pasamos por un punto de quiebre. <b>No tenemos por qué pasarlo solos.</b> Para eso está el Instituto de Productividad: para acompañarte en el proceso, con evidencia de cómo funciona tu cerebro y un método basado en neurociencia.</p>
    <div class="steps">
      <div class="st"><span class="b">1</span> Elegís día y hora</div>
      <div class="st"><span class="b">2</span> Charlamos tu caso</div>
      <div class="st"><span class="b">3</span> Vemos si encajás</div>
    </div>
    <a href="#" class="btn btn-primary btn-lg" onclick="agdOpen('cierre');return false">Agendar mi entrevista de admisión <span class="arrow">→</span></a>
  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════ DECK (v C)
DECK = """
<!-- DECK · el "VSL" en slides -->
<section class="section section--navy" id="presentacion">
  <div class="wrap center">
    <div class="center"><span class="eyebrow">La presentación · 4 slides</span></div>
    <h2 class="h2">Todo el Instituto, en <span class="hl">2 minutos de lectura</span></h2>
    <p class="lead-2" style="margin-bottom:34px">Pasá los slides con las flechas. Sin video, sin registro: lo que hay adentro, los pilares que se trabajan y el respaldo con el que se certifica.</p>

    <div class="deck">
      <div class="deck__stage">
        <div class="deck__track" id="deckTrack">

          <article class="slide" role="group" aria-label="Slide 1 de 4">
            <span class="slide__eyebrow">01 · Qué incluye</span>
            <h3 class="slide__title">No es un curso de videos: es un <span class="hl">acompañamiento de 6 meses</span></h3>
            <p class="slide__lead">Un profesional por cada frente de tu vida y tu operación. Todo lo que ponemos del otro lado para que esta vez tus objetivos sí avancen.</p>
            <div class="slide__grid slide__grid--3">
              <div class="sitem"><span class="mk">01</span><div><h4>Coach dedicada, 1 a 1</h4><p>Te conoce, te sigue de cerca y no te deja aflojar. Lo más valorado por los alumnos (8.8/10).</p></div></div>
              <div class="sitem"><span class="mk">02</span><div><h4>Biblioteca de +20 módulos</h4><p>El método completo, ordenado y secuencial. Píldoras cortas y accionables.</p></div></div>
              <div class="sitem"><span class="mk">03</span><div><h4>Llamadas grupales en vivo</h4><p>Encuentros con Nico y el equipo para resolver tu caso real.</p></div></div>
              <div class="sitem"><span class="mk">04</span><div><h4>Comunidad + mastermind</h4><p>Gente con tu carga y tu oficio — incluido el mastermind presencial en Buenos Aires.</p></div></div>
              <div class="sitem"><span class="mk">05</span><div><h4>Equipo multidisciplinario</h4><p>Psicólogos, nutricionistas y coaches de alto rendimiento.</p></div></div>
              <div class="sitem"><span class="mk">06</span><div><h4>Sistemas listos para usar</h4><p>Habit Tracker y Second Brain para sacarte la carga de la cabeza.</p></div></div>
            </div>
          </article>

          <article class="slide" role="group" aria-label="Slide 2 de 4">
            <span class="slide__eyebrow">02 · El método</span>
            <h3 class="slide__title">La productividad es el <span class="hl">auto completo</span>, no pisar más el acelerador</h3>
            <p class="slide__lead">Service, aceite, gomas: rendir sostenido no es apretar más fuerte, es que todo el sistema funcione. Por eso el método toca <b>las cinco áreas</b> —no una técnica suelta.</p>
            <div class="slide__grid slide__grid--3">
              <div class="sitem"><span class="mk">01</span><div><h4>Descanso y energía</h4><p>La primera palanca: sin energía no hay sistema que se sostenga.</p></div></div>
              <div class="sitem"><span class="mk">02</span><div><h4>Alimentación</h4><p>Comer para tener claridad mental, no para apagar la ansiedad.</p></div></div>
              <div class="sitem"><span class="mk">03</span><div><h4>Movimiento</h4><p>Una rutina física que te devuelva energía en lugar de quitártela.</p></div></div>
              <div class="sitem"><span class="mk">04</span><div><h4>Foco y hábitos</h4><p>Bloques de trabajo profundo y hábitos que no dependen de las ganas.</p></div></div>
              <div class="sitem"><span class="mk">05</span><div><h4>Mentalidad</h4><p>Desarmar la autoexigencia que te tiene apagando incendios.</p></div></div>
            </div>
          </article>

          <article class="slide slide--aval" role="group" aria-label="Slide 3 de 4">
            <span class="slide__eyebrow">03 · El respaldo</span>
            <h3 class="slide__title">Tu sistema, con <span class="hl">aval universitario</span></h3>
            <p class="slide__lead">No es una constancia por asistir. La versión <b>Platinum</b> se certifica de forma conjunta con la <b>Facultad de Ciencias Económicas de la Universidad Nacional de Jujuy (UNJu)</b>: se gana, no se regala — y por eso pesa distinto en tu CV, tu LinkedIn y frente a quien sea.</p>
            <ul class="feat-list">
              <li>Trayecto de 250 horas certificado por la Facultad, con evaluación y trabajo final</li>
              <li>Certificado digital emitido y firmado por la Facultad, con mecanismo de verificación</li>
              <li>Exclusivo de la versión Platinum · Certificación optativa</li>
            </ul>
            <p class="feat-legal">El certificado es emitido por la Facultad de Ciencias Económicas de la Universidad Nacional de Jujuy en el marco de un programa de certificación conjunta con NFM Productivity S.A.S. La certificación universitaria es optativa, exige requisitos académicos de aprobación y no constituye título universitario de grado ni de posgrado, ni acredita equivalencias automáticas.</p>
          </article>

          <article class="slide slide--cta" role="group" aria-label="Slide 4 de 4">
            <span class="slide__eyebrow">04 · El siguiente paso</span>
            <h3 class="slide__title">Si te hizo ruido, <span class="hl">hablemos</span></h3>
            <p class="slide__lead">Una entrevista de admisión 1 a 1 con el equipo. Vemos tu caso concreto y si el Instituto es para vos. <b>Sin costo y sin compromiso de compra.</b></p>
            <div class="steps">
              <div class="st"><span class="b">1</span> Elegís día y hora</div>
              <div class="st"><span class="b">2</span> Charlamos tu caso</div>
              <div class="st"><span class="b">3</span> Vemos si encajás</div>
            </div>
            <a href="#" class="btn btn-primary btn-lg" onclick="agdOpen('slide-cta');return false">Agendar mi entrevista de admisión <span class="arrow">→</span></a>
          </article>

        </div>
        <button class="deck__nav deck__nav--prev" id="deckPrev" type="button" aria-label="Slide anterior">‹</button>
        <button class="deck__nav deck__nav--next" id="deckNext" type="button" aria-label="Slide siguiente">›</button>
      </div>
      <div class="deck__bar"><span id="deckFill" style="width:25%"></span></div>
      <div class="deck__foot">
        <div class="deck__dots" id="deckDots"></div>
        <div class="deck__count"><b id="deckNum">01</b> / 04</div>
      </div>
      <div class="deck__hint">Pasá los slides ← →</div>
    </div>
__CTA__
  </div>
</section>
"""

DECK_JS = """
<script>
/* ---------- DECK de slides (reemplaza al VSL) ---------- */
(function(){
  var track=document.getElementById('deckTrack'); if(!track) return;
  var slides=track.querySelectorAll('.slide');
  var total=slides.length, i=0;
  var prev=document.getElementById('deckPrev'), next=document.getElementById('deckNext');
  var dots=document.getElementById('deckDots'), fill=document.getElementById('deckFill'), num=document.getElementById('deckNum');

  for(var d=0; d<total; d++){
    (function(k){
      var b=document.createElement('button');
      b.type='button'; b.className='deck__dot'+(k===0?' on':'');
      b.setAttribute('aria-label','Ir al slide '+(k+1));
      b.onclick=function(){ ir(k); };
      dots.appendChild(b);
    })(d);
  }

  function ir(n){
    i=Math.max(0, Math.min(total-1, n));
    track.style.transform='translateX(-'+(i*100)+'%)';
    var ds=dots.querySelectorAll('.deck__dot');
    for(var k=0;k<ds.length;k++) ds[k].classList.toggle('on', k===i);
    fill.style.width=((i+1)/total*100)+'%';
    num.textContent=('0'+(i+1)).slice(-2);
    prev.disabled=(i===0); next.disabled=(i===total-1);
  }
  prev.onclick=function(){ ir(i-1); };
  next.onclick=function(){ ir(i+1); };

  /* teclado: solo cuando el deck está a la vista */
  document.addEventListener('keydown', function(e){
    if(document.querySelector('.agd-overlay.open')) return;
    var r=track.getBoundingClientRect();
    if(r.bottom<0 || r.top>window.innerHeight) return;
    if(e.key==='ArrowRight'){ ir(i+1); }
    if(e.key==='ArrowLeft'){ ir(i-1); }
  });

  /* deslizar en touch */
  var x0=null, y0=null;
  track.addEventListener('touchstart', function(e){ x0=e.touches[0].clientX; y0=e.touches[0].clientY; }, {passive:true});
  track.addEventListener('touchend', function(e){
    if(x0===null) return;
    var dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0;
    if(Math.abs(dx)>44 && Math.abs(dx)>Math.abs(dy)) ir(dx<0 ? i+1 : i-1);
    x0=null; y0=null;
  }, {passive:true});

  ir(0);
})();
</script>
"""

# ══════════════════════════════════════════════════════════ FEED (versión D)
def fcta(origen, texto="Agendar mi entrevista de admisión"):
    return ('      <a href="#" class="btn btn-primary btn-lg" onclick="agdOpen(\'%s\');return false">'
            '%s <span class="arrow">&rarr;</span></a>' % (origen, texto))


def feed_html():
    S = []

    # 1 · promesa
    S.append("""  <section class="fslide">
    <div class="fslide__in">
      <span class="eyebrow">Alto rendimiento con base en neurociencia</span>
      <h1>No te falta información. Te falta un método que trabaje <span class="hl">a favor de tu cerebro</span>.</h1>
      <p class="sub">Un <b>acompañamiento de 6 meses</b> con coach dedicada, equipo multidisciplinario y aval universitario. No más apps ni más fuerza de voluntad: un sistema a tu medida, con base en neurociencia.</p>
%s
    </div>
    <div class="feed-hint"><span>Desliz&aacute; para seguir</span><span class="ar">&darr;</span></div>
  </section>""" % fcta('feed-promesa'))

    # 2 · qué incluye
    incluye = [
        ("01", "Tu coach dedicada, 1 a 1", "Te conoce, te sigue de cerca y no te deja aflojar. Lo m&aacute;s valorado por los alumnos (8.8/10)."),
        ("02", "Biblioteca de +20 m&oacute;dulos", "El m&eacute;todo completo, ordenado y secuencial. P&iacute;ldoras cortas y accionables."),
        ("03", "Llamadas grupales en vivo", "Encuentros con Nico y el equipo para resolver tu caso real."),
        ("04", "Comunidad + mastermind", "Gente con tu carga y tu oficio &mdash; incluido el mastermind presencial en Buenos Aires."),
        ("05", "Equipo multidisciplinario", "Psic&oacute;logos, nutricionistas y coaches de alto rendimiento."),
        ("06", "Sistemas listos para usar", "Habit Tracker y Second Brain para sacarte la carga de la cabeza."),
    ]
    items = "\n".join(
        '        <div class="fi"><span class="mk">%s</span><div><h4>%s</h4><p>%s</p></div></div>' % it
        for it in incluye)
    S.append("""  <section class="fslide fslide--navy">
    <div class="fslide__in">
      <span class="eyebrow">Qu&eacute; incluye</span>
      <h2 class="h2">No es un curso de videos: es un <span class="hl">acompa&ntilde;amiento de 6 meses</span></h2>
      <div class="flist">
%s
      </div>
%s
    </div>
  </section>""" % (items, fcta('feed-incluye')))

    # 3 · aval universitario
    S.append("""  <section class="fslide">
    <div class="fslide__in">
      <span class="eyebrow">El respaldo</span>
      <h2 class="h2">Tu sistema, con <span class="hl">aval universitario</span></h2>
      <p class="sub">La versi&oacute;n <b>Platinum</b> se certifica de forma conjunta con la <b>Facultad de Ciencias Econ&oacute;micas de la Universidad Nacional de Jujuy (UNJu)</b>. Se gana, no se regala.</p>
      <ul class="feat-list">
        <li>250 horas certificadas por la Facultad, con evaluaci&oacute;n y trabajo final</li>
        <li>Certificado digital firmado por la Facultad, con verificaci&oacute;n</li>
        <li>Exclusivo de la versi&oacute;n Platinum &middot; Certificaci&oacute;n optativa</li>
      </ul>
      <p class="feat-legal">El certificado es emitido por la Facultad de Ciencias Econ&oacute;micas de la Universidad Nacional de Jujuy en el marco de un programa de certificaci&oacute;n conjunta con NFM Productivity S.A.S. La certificaci&oacute;n universitaria es optativa, exige requisitos acad&eacute;micos de aprobaci&oacute;n y no constituye t&iacute;tulo universitario de grado ni de posgrado, ni acredita equivalencias autom&aacute;ticas.</p>
%s
    </div>
  </section>""" % fcta('feed-aval'))

    # 4..N · todos los casos, uno por slide
    for n, c in enumerate(CASOS, 1):
        S.append("""  <section class="fslide fslide--navy">
    <div class="fslide__in">
      <span class="eyebrow">Caso %02d de %d</span>
      <button type="button" class="fcaso__thumb caso__thumb" data-yt="%s" aria-label="Ver la entrevista de %s">
        <img src="https://img.youtube.com/vi/%s/hqdefault.jpg" alt="Entrevista a %s" loading="lazy">
        <span class="caso__play" aria-hidden="true"></span>
      </button>
      <div class="fcaso__name">%s</div>
      <div class="fcaso__perfil">%s</div>
      <p class="fcaso__frase">%s</p>
%s
    </div>
  </section>""" % (n, len(CASOS), c['yt'], c['nombre'], c['yt'], c['nombre'],
                   c['nombre'], c['perfil'], c['frase'], fcta('feed-caso-'+c['id'])))

    # cierre
    S.append("""  <section class="fslide">
    <div class="fslide__in">
      <span class="eyebrow">El siguiente paso</span>
      <h2 class="h2">Agend&aacute; tu <span class="hl">entrevista de admisi&oacute;n</span></h2>
      <p class="sub">1 a 1 con el equipo. Vemos tu caso concreto y si el Instituto es para vos. Sin costo.</p>
      <div class="steps" style="justify-content:center;display:flex;gap:18px;flex-wrap:wrap;margin-top:22px">
        <div class="st"><span class="b">1</span> Eleg&iacute;s d&iacute;a y hora</div>
        <div class="st"><span class="b">2</span> Charlamos tu caso</div>
        <div class="st"><span class="b">3</span> Vemos si encaj&aacute;s</div>
      </div>
%s
    </div>
  </section>""" % fcta('feed-cierre'))

    return ('<div class="feed-bar"><span id="feedFill"></span></div>\n'
            '<div class="feed-count" id="feedCount">01 / %d</div>\n'
            '<div class="feed" id="feed">\n' % (len(S)) + "\n".join(S) + '\n</div>\n')


FEED_JS = """
<script>
/* ---------- Feed vertical: progreso y contador ---------- */
(function(){
  var feed=document.getElementById('feed'); if(!feed) return;
  document.body.classList.add('feed-mode');
  var slides=feed.querySelectorAll('.fslide');
  var fill=document.getElementById('feedFill'), count=document.getElementById('feedCount');
  var total=slides.length, actual=0;

  function pintar(){
    fill.style.width=((actual+1)/total*100)+'%';
    count.textContent=('0'+(actual+1)).slice(-2)+' / '+('0'+total).slice(-2);
  }
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      for(var i=0;i<es.length;i++){
        if(es[i].isIntersecting){
          var k=Array.prototype.indexOf.call(slides, es[i].target);
          if(k>-1 && k!==actual){ actual=k; pintar(); }
        }
      }
    }, {root:feed, threshold:0.55});
    for(var i=0;i<total;i++) io.observe(slides[i]);
  } else {
    feed.addEventListener('scroll', function(){
      var k=Math.round(feed.scrollTop/feed.clientHeight);
      if(k!==actual){ actual=Math.min(total-1,Math.max(0,k)); pintar(); }
    }, {passive:true});
  }
  pintar();
})();
</script>
"""

# ══════════════════════════════════════════════════════════════════ FOOTER + JS
FOOTER_JS = """
<footer class="foot">
  <div class="wrap">
    <a href="#top" class="brand">
      <svg class="brand__logo" viewBox="0 0 132 112" role="img" aria-label="Instituto de Productividad"><use href="#ip-logo"/></svg>
      <span class="brand__wordmark"><span class="brand__top">Instituto de</span><span class="brand__bottom">Productividad</span></span>
    </a>
    <small>© Instituto de Productividad · Nicolás Fernández Miranda</small>
  </div>
</footer>

<!-- ═══ POPUP AGENDAR · Calendly · cierra SOLO con la X ═══ -->
<style>
  .agd-overlay{position:fixed;inset:0;z-index:200;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(6,29,48,.74);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
  .agd-overlay.open{display:flex;animation:agdfade .25s ease}
  @keyframes agdfade{from{opacity:0}to{opacity:1}}
  /* columna flex: la cabecera ocupa lo suyo y el calendario se queda con TODO el resto,
     asi Calendly nunca aparece cortado ni con doble barra de scroll */
  .agd-card{position:relative;width:100%;max-width:1020px;height:min(94vh,880px);background:#fff;border-radius:18px;box-shadow:0 40px 120px rgba(0,0,0,.42);padding:22px 22px 18px;display:flex;flex-direction:column;animation:agdpop .3s ease}
  .agd-head{flex:0 0 auto;padding-right:48px}
  @keyframes agdpop{from{opacity:0;transform:translateY(18px) scale(.98)}to{opacity:1;transform:none}}
  .agd-x{position:absolute;top:14px;right:14px;width:36px;height:36px;border-radius:50%;border:1px solid var(--hair-2);background:#fff;color:var(--mono-grey);font-size:15px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s;z-index:3}
  .agd-x:hover{color:#fff;background:var(--nfm-blue);border-color:var(--nfm-blue)}
  .agd-x:focus-visible{outline:3px solid var(--nfm-orange);outline-offset:2px}
  .agd-mono{font-family:'JetBrains Mono';font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--nfm-orange-text);font-weight:500;display:block;margin-bottom:10px}
  .agd-card h3{font-family:'Montserrat';font-weight:800;font-size:clamp(19px,2.6vw,24px);color:var(--nfm-blue);line-height:1.2;margin:0 0 18px;max-width:30ch}
  .agd-cal{flex:1 1 auto;min-height:380px;display:flex;border-radius:12px;overflow:hidden;border:1px solid var(--hair);background:#f4f6f8}
  /* el hijo se estira solo (align-items:stretch): sin height:100%, que no resuelve dentro de un flex item */
  .agd-cal>*{flex:1 1 auto;width:100%;min-width:0;border:0;display:block}
  .agd-ph{display:flex;align-items:center;justify-content:center;text-align:center;padding:28px;color:var(--muted);font-size:14px}
  .agd-ph a{color:var(--nfm-orange-text);font-weight:700}
  body.agd-lock{overflow:hidden}
  @media(max-width:640px){
    .agd-overlay{padding:0}
    .agd-card{max-width:none;height:100vh;height:100dvh;border-radius:0;padding:18px 12px 12px}
    .agd-card h3{font-size:18px;margin-bottom:12px}
    .agd-cal{min-height:0}
  }
</style>

<div class="agd-overlay" id="agdModal">
  <div class="agd-card" role="dialog" aria-modal="true" aria-label="Agendar entrevista de admisión">
    <button class="agd-x" type="button" id="agdX" onclick="agdClose()" aria-label="Cerrar">✕</button>
    <div class="agd-head">
      <span class="agd-mono">◆ Entrevista de admisión · 1 a 1 · Sin costo</span>
      <h3>Elegí el día y la hora que mejor te queden</h3>
    </div>
    <div class="agd-cal" id="agdCal"><div class="agd-ph">Cargando calendario…</div></div>
  </div>
</div>

<script>
/* =========================================================================
   ⚙️  CONFIG — EDITÁ SOLO ESTO
   ========================================================================= */
const CONFIG = {
  // Calendly de la entrevista de admisión (se abre embebido en el popup).
  CALENDLY_URL: "__CALENDLY__",
};

/* ===== FOTOS REALES DE LOS RECUADROS =====
   Podés poner VARIAS por recuadro y se arma un collage solo (hasta 4). */
const IMG = {
  comunidad:    ["https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6275ecb6db2520210e75.jpg"],
  modulos:      ["https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b62e2497cd89d2487dead.png"],
  coach:        ["https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b62e2cf81b06f057b50b2.png"],
  llamadas:     ["https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6278f7a089644cf46063.jpg"],
  certificados: [
    "https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6277cdfcf0495677abe5.jpg",
    "https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6275f7a089644cf4601d.jpg",
    "https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6275cf81b06f057b46bf.jpg",
    "https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6275ecb6db2520210e7a.jpg"
  ],
};
/* ===================== FIN DE LO QUE TENÉS QUE EDITAR ===================== */


/* ---------- Popup agendar (Calendly) · cierra solo con la X ---------- */
var agdCalLoaded=false;
function getUTM(){
  var p=new URLSearchParams(location.search);
  var s=p.get('utm_source'),m=p.get('utm_medium'),c=p.get('utm_campaign');
  if(s||m||c) return [s||'',m||'',c||''].join(' / ');
  return document.referrer||'directo';
}
function agdOpen(origen){
  var box=document.getElementById('agdCal');
  if(agdCalLoaded && box && !box.querySelector('iframe, .calendly-inline-widget')) agdCalLoaded=false;
  document.getElementById('agdModal').classList.add('open');
  document.body.classList.add('agd-lock');
  agdLoadCalendly();
  setTimeout(function(){ try{ document.getElementById('agdX').focus(); }catch(e){} }, 80);
}
function agdClose(){
  document.getElementById('agdModal').classList.remove('open');
  document.body.classList.remove('agd-lock');
}
function agdLoadCalendly(){
  if(agdCalLoaded) return;
  var box=document.getElementById('agdCal'); if(!box) return;
  var url=CONFIG.CALENDLY_URL;
  if(!url || url.indexOf('http')!==0){
    box.innerHTML='<div class="agd-ph">Pegá tu link en <b>CONFIG.CALENDLY_URL</b> para mostrar el calendario acá.</div>';
    return;
  }
  agdCalLoaded=true;
  var sep=url.indexOf('?')<0?'?':'&';
  var full=url+sep+'utm_source='+encodeURIComponent(getUTM())+'&hide_gdpr_banner=1';
  function init(){
    box.innerHTML='';
    if(window.Calendly){ Calendly.initInlineWidget({url:full, parentElement:box}); }
    else{ box.innerHTML='<div class="calendly-inline-widget" data-url="'+full+'" style="min-width:280px;height:700px;"></div>'; }
  }
  if(!document.getElementById('calendly-css')){
    var l=document.createElement('link'); l.id='calendly-css'; l.rel='stylesheet';
    l.href='https://assets.calendly.com/assets/external/widget.css'; document.head.appendChild(l);
  }
  if(window.Calendly){ init(); return; }
  var s=document.createElement('script');
  s.src='https://assets.calendly.com/assets/external/widget.js'; s.async=true;
  s.onload=init;
  s.onerror=function(){ box.innerHTML='<div class="agd-ph">No se pudo cargar el calendario. <a href="'+url+'" target="_blank" rel="noopener">Abrilo en una pestaña →</a></div>'; };
  document.head.appendChild(s);
}
/* Cierra SOLO con la X — sin clic afuera ni Escape, para evitar salidas por error */

/* ---------- Casos: click-to-play de YouTube ---------- */
document.addEventListener('click', function(e){
  var b=e.target && e.target.closest ? e.target.closest('.caso__thumb') : null;
  if(!b || b.dataset.on) return;
  var id=b.getAttribute('data-yt'); if(!id) return;
  b.dataset.on='1';
  b.innerHTML='<iframe src="https://www.youtube.com/embed/'+id+'?autoplay=1&rel=0" title="Entrevista" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen></iframe>';
});

/* ---------- Fotos reales en los recuadros (collage 1 a 4) ---------- */
function fillPhotos(){
  var slots=document.querySelectorAll('[data-img]');
  for(var s=0;s<slots.length;s++){
    var slot=slots[s], key=slot.getAttribute('data-img');
    var arr=(typeof IMG!=='undefined' && IMG[key])?IMG[key]:[];
    arr=arr.filter(function(u){ return u && u.indexOf('http')===0; });
    if(!arr.length) continue;
    var n=Math.min(arr.length,4);
    var alt=slot.getAttribute('data-alt')||'Instituto de Productividad';
    var html='<div class="collage collage--'+n+'">';
    for(var i=0;i<n;i++){ html+='<img src="'+arr[i]+'" alt="'+alt+'" loading="lazy">'; }
    html+='</div>';
    slot.innerHTML=html;
  }
}
window.addEventListener('DOMContentLoaded', fillPhotos);
</script>

__NEURAL__
</body>
</html>
"""


def hero(version):
    # larga y corta comparten el mismo hero (asi el test A/B aisla lo que va debajo)
    if version in ('larga','corta'):
        return """
<!-- HERO · la promesa -->
<section class="hero">
  <div class="wrap center">
    <span class="eyebrow fade-up d1">Alto rendimiento con base en neurociencia</span>
    <h1 class="fade-up d1" style="max-width:22ch;margin-left:auto;margin-right:auto">No te falta información. Te falta un método que trabaje <span class="hl">a favor de tu cerebro</span>.</h1>
    <p class="sub fade-up d2" style="margin-left:auto;margin-right:auto">Un <b>acompañamiento de 6 meses</b> con coach dedicada, equipo multidisciplinario y aval universitario. No más apps ni más fuerza de voluntad: un sistema a tu medida, con base en neurociencia.</p>
__CTA__
  </div>
</section>
"""
    return """
<!-- HERO · la promesa -->
<section class="hero">
  <div class="wrap center">
    <span class="eyebrow fade-up d1">Alto rendimiento con base en neurociencia</span>
    <h1 class="fade-up d1" style="max-width:22ch;margin-left:auto;margin-right:auto">No te falta información. Te falta un método que trabaje <span class="hl">a favor de tu cerebro</span>.</h1>
    <p class="sub fade-up d2" style="margin-left:auto;margin-right:auto">En el <b>Instituto de Productividad</b> no sumamos más apps ni más fuerza de voluntad. Entendemos cómo funciona tu cerebro y armamos un sistema a tu medida. <b>Neurociencia aplicada, no más disciplina.</b></p>
  </div>
</section>
"""


def build(version, title, rotulo, body):
    out = HEAD.replace('__TITLE__', title).replace('__ROTULO__', rotulo)
    out += body
    js = DECK_JS if version == 'slides' else (FEED_JS if version == 'feed' else '')
    pie = FOOTER_JS
    if version == 'feed':               # en el feed cada slide ocupa la pantalla: sin footer
        i = pie.index('<footer class="foot">'); j = pie.index('</footer>') + len('</footer>')
        pie = pie[:i] + pie[j:]
    out += pie.replace('__CALENDLY__', CALENDLY).replace('__NEURAL__', js + "\n" + NEURAL)
    return out


# ─────────────────────────────────────────────────────────── VERSIÓN A · LARGA
larga = (
    hero('larga').replace('__CTA__', cta('hero'))
    + SEC_CASOS.replace('__CARDS__', casos_cards(9)).replace('__CTA__', cta('casos', 'Quiero mi entrevista de admisión'))
    + SEC_INCLUYE.replace('__NAVY__', '').replace('__CTA__', cta('incluye'))
    + SEC_AVAL.replace('__NAVY__', ' section--navy').replace('__CTA__', cta('aval', 'Quiero aplicar al Platinum'))
)

# ─────────────────────────────────────────────────────────── VERSIÓN B · CORTA
corta = (
    hero('corta').replace('__CTA__', cta('hero'))
    + SEC_INCLUYE.replace('__NAVY__', ' section--navy').replace('__CTA__', cta('incluye'))
    + SEC_AVAL.replace('__NAVY__', '').replace('__CTA__', cta('aval', 'Quiero aplicar al Platinum'))
    + '\n<div class="quiz-wrap">\n' + QUIZ + '\n</div>\n'
)

# ────────────────────────────────────────────────────────── VERSIÓN C · SLIDES
slides = (
    hero('slides')
    + DECK.replace('__CTA__', cta('deck'))
    + SEC_CASOS.replace('section section--navy', 'section').replace('__CARDS__', casos_cards(6)).replace('__CTA__', cta('casos', 'Quiero mi entrevista de admisión'))
    + SEC_CIERRE.replace('__CLASE__', ' section--navy')
)

feed = feed_html()

files = [
    ('tsl-d-feed.html',   'feed',   'Instituto de Productividad · Pas&aacute; y agend&aacute;', 'VERSIÓN D · FEED VERTICAL (mobile-first, un slide por pantalla)', feed),
    ('tsl-a-larga.html',  'larga',  'Instituto de Productividad · Método con base en neurociencia', 'VERSIÓN A · LARGA (promesa → casos → qué incluye → aval)', larga),
    ('tsl-b-corta.html',  'corta',  'Instituto de Productividad · Método con base en neurociencia', 'VERSIÓN B · CORTA (promesa → qué incluye → aval)', corta),
    ('tsl-c-slides.html', 'slides', 'Instituto de Productividad · La presentación en 4 slides',    'VERSIÓN C · SLIDES (promesa → deck de 4 slides → casos)', slides),
]

for fname, ver, title, rotulo, body in files:
    html = build(ver, title, rotulo, body)
    p = os.path.join(BASE, fname)
    open(p, 'w', encoding='utf-8').write(html)
    print("%-20s %7d bytes" % (fname, len(html)))
