// Render del shell: nada de terceros puede bloquear el primer pintado.
//
// Regression: ISSUE-001 — la hoja de estilos de Google Fonts era
// render-blocking, así que en cualquier red que no la alcanzara (lenta,
// offline, o redes que bloquean Google) la app quedaba en blanco ~12 s.
// Found by /qa on 2026-09-02
// Report: .gstack/qa-reports/qa-report-focus-habit-tracker-2026-09-02.md
//
// Se testea sobre el HTML/CSS como texto: es el contrato que importa y no
// necesita navegador, así que corre en la suite rápida.

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const APP = new URL('../focus-habit-tracker/', import.meta.url).pathname;
const html = readFileSync(APP + 'index.html', 'utf8');
const css = readFileSync(APP + 'css/styles.css', 'utf8');

describe('recursos externos no bloquean el render', () => {
  test('toda hoja de estilos remota se carga sin bloquear', () => {
    // <link rel=stylesheet> con href remoto: debe llevar el patrón
    // media="print" onload=... (o estar dentro de <noscript>).
    const sinNoscript = html.replace(/<noscript>[\s\S]*?<\/noscript>/g, '');
    const remotos = [...sinNoscript.matchAll(/<link\b[^>]*href="https?:\/\/[^"]*"[^>]*>/g)]
      .map((m) => m[0])
      .filter((tag) => /rel=["']?stylesheet/.test(tag));

    assert.ok(remotos.length > 0, 'el test asume que hay al menos una hoja remota');
    for (const tag of remotos) {
      assert.match(tag, /media=["']print["']/, `hoja remota bloqueante: ${tag.slice(0, 90)}`);
      assert.match(tag, /onload=/, `hoja remota sin swap a media=all: ${tag.slice(0, 90)}`);
    }
  });

  test('no hay <script> remoto y bloqueante en el head', () => {
    const head = html.slice(0, html.indexOf('</head>'));
    const bloqueantes = [...head.matchAll(/<script\b[^>]*src="https?:\/\/[^"]*"[^>]*>/g)]
      .map((m) => m[0])
      .filter((tag) => !/\b(defer|async|type=["']module["'])/.test(tag));
    assert.deepEqual(bloqueantes, [], 'un script remoto sin defer/async bloquea el render');
  });
});

describe('tipografía degrada bien sin las webfonts', () => {
  const stacks = [...css.matchAll(/--font-[\w-]+:\s*([^;]+);/g)].map((m) => m[1].trim());

  test('hay stacks de fuente definidos', () => {
    assert.ok(stacks.length >= 3, `esperaba 3 stacks, encontré ${stacks.length}`);
  });

  test('cada stack tiene fallback de sistema, no solo la genérica', () => {
    for (const stack of stacks) {
      const fuentes = stack.split(',').map((f) => f.trim().replace(/^['"]|['"]$/g, ''));
      assert.ok(fuentes.length >= 3,
        `stack sin fallback real (webfont + genérica no alcanza): ${stack}`);

      const genericas = ['sans-serif', 'serif', 'monospace', 'system-ui', 'ui-monospace'];
      const intermedias = fuentes.slice(1, -1).filter((f) => !genericas.includes(f));
      assert.ok(intermedias.length > 0 || fuentes.slice(1).some((f) => ['system-ui', 'ui-monospace'].includes(f)),
        `stack sin fuente de sistema concreta: ${stack}`);
    }
  });
});
