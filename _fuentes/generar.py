#!/usr/bin/env python3
"""Genera las páginas del sitio a partir de los fragmentos de _fuentes/paginas.

Cada fragmento empieza con un bloque de datos:
    <!--
    titulo: Título de la pestaña
    descripcion: Descripción para buscadores y para compartir
    nav: mantenimiento            (enlace del menú marcado como página actual)
    cierre: Título | Texto        (llamada final antes del pie; omitir para no ponerla)
    -->
y sigue el contenido de <main>. Marcadores disponibles: {{canales}}, {{formulario}}.

Uso:  python3 _fuentes/generar.py      (escribe los .html en la raíz del sitio)
"""
import pathlib, re, html

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINAS = RAIZ / '_fuentes' / 'paginas'
URL = 'https://bilbostudios.github.io/sertes-web/'
TEL, TEL_TXT = '+34603082442', '+34 603 082 442'

MENU = [
    ('servicios', 'index.html#servicios', 'Servicios'),
    ('equipos', 'index.html#equipos', 'Equipos'),
    ('sertes', 'index.html#sertes', 'Sobre SERTES'),
    ('fabricantes', 'index.html#fabricantes', 'Fabricantes'),
]

CANALES = f'''<dl class="channels">
          <div><dt>Teléfono</dt><dd><a href="tel:{TEL}">{TEL_TXT}</a></dd></div>
          <div><dt>Correo</dt><dd><a href="mailto:sertes@sertes.es">sertes@sertes.es</a></dd></div>
          <div><dt>WhatsApp</dt><dd><a href="https://wa.me/34603082442" target="_blank" rel="noopener">Abrir conversación</a></dd></div>
          <div><dt>LinkedIn</dt><dd><a href="https://www.linkedin.com/company/sertes-servicio-t%C3%A9cnico-especializado/" target="_blank" rel="noopener">Perfil de SERTES</a></dd></div>
        </dl>'''

FORMULARIO = '''<form class="form" id="form">
        <div class="field"><label for="nombre">Nombre *</label><input id="nombre" name="nombre" required autocomplete="name"></div>
        <div class="field"><label for="email">Correo electrónico *</label><input id="email" name="email" type="email" required autocomplete="email"></div>
        <div class="field"><label for="telefono">Teléfono</label><input id="telefono" name="telefono" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="empresa">Empresa</label><input id="empresa" name="empresa" autocomplete="organization"></div>
        <div class="field wide"><label for="asunto">Asunto</label><input id="asunto" name="asunto"></div>
        <div class="field wide"><label for="mensaje">Mensaje *</label><textarea id="mensaje" name="mensaje" required placeholder="Equipo, marca y modelo, y qué ocurre o qué necesitas."></textarea></div>
        <p class="note">Los campos marcados con * son obligatorios.</p>
        <label class="consent"><input type="checkbox" required><span>He leído y acepto la <a href="privacidad.html">política de privacidad</a>.</span></label>
        <button class="btn btn-blue" type="submit">Enviar solicitud</button>
      </form>'''


def cabecera(actual):
    enlaces = []
    for clave, href, texto in MENU:
        cur = ' aria-current="page"' if clave == actual else ''
        enlaces.append(f'<a href="{href}"{cur}>{texto}</a>')
    enlaces.append('<a class="btn btn-blue" href="index.html#contacto">Contacto</a>')
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="SERTES, inicio"><span class="brand">SERTES<i></i></span></a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    <nav class="menu" id="menu" aria-label="Principal">
      {(chr(10) + '      ').join(enlaces)}
    </nav>
  </div>
</header>'''


def cierre(dato):
    if not dato:
        return ''
    titulo, texto = [x.strip() for x in dato.split('|', 1)]
    return f'''
  <section class="band band-dark cta" aria-labelledby="cierre">
    <div class="wrap">
      <div>
        <h2 id="cierre">{titulo}</h2>
        <p>{texto}</p>
      </div>
      <div class="cta-side">
        <div class="actions">
          <a class="btn btn-white" href="index.html#contacto">Solicitar asistencia</a>
          <a class="btn btn-line" href="tel:{TEL}">Llamar al {TEL_TXT[4:]}</a>
        </div>
        <p>También por <a href="https://wa.me/34603082442" target="_blank" rel="noopener">WhatsApp</a> o en <a href="mailto:sertes@sertes.es">sertes@sertes.es</a>.</p>
      </div>
    </div>
  </section>'''


PIE = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-bottom">
      <span><span class="brand">SERTES<i></i></span>&nbsp;&nbsp; © <span class="year">2026</span> · Servicio Técnico Especializado · Pamplona, Navarra</span>
      <nav aria-label="Legal">
        <a href="https://www.linkedin.com/company/sertes-servicio-t%C3%A9cnico-especializado/" target="_blank" rel="noopener">LinkedIn</a>
        <a href="aviso-legal.html">Aviso legal</a>
        <a href="privacidad.html">Política de privacidad</a>
        <a href="cookies.html">Política de cookies</a>
      </nav>
    </div>
  </div>
</footer>

<div class="callbar" aria-label="Contacto rápido">
  <a class="btn btn-blue" href="tel:{TEL}">Llamar</a>
  <a class="btn btn-line" href="https://wa.me/34603082442" target="_blank" rel="noopener">WhatsApp</a>
</div>'''


def pagina(fuente):
    texto = fuente.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--(.*?)-->\s*', texto, re.S)
    datos = dict(re.findall(r'^\s*(\w+):\s*(.+?)\s*$', m.group(1), re.M))
    cuerpo = texto[m.end():].replace('{{canales}}', CANALES).replace('{{formulario}}', FORMULARIO)
    nombre = fuente.stem + '.html'
    url = URL + ('' if nombre == 'index.html' else nombre)
    t, d = html.escape(datos['titulo']), html.escape(datos['descripcion'])
    return nombre, f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0b1548">
<link rel="icon" type="image/png" href="icono.png">
<link rel="apple-touch-icon" href="icono-180.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="SERTES">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{URL}compartir.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="fuentes/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="estilos.css">
</head>
<body>

{cabecera(datos.get('nav', ''))}

<main id="contenido">
{cuerpo.rstrip()}
{cierre(datos.get('cierre'))}
</main>

{PIE}

<script src="web.js"></script>
</body>
</html>
'''


if __name__ == '__main__':
    for f in sorted(PAGINAS.glob('*.html')):
        nombre, contenido = pagina(f)
        (RAIZ / nombre).write_text(contenido, encoding='utf-8')
        print('escrita', nombre)
