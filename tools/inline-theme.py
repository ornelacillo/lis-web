#!/usr/bin/env python3
"""Copia theme.css dentro de cada página (entre las marcas THEME-CSS) para que no bloquee la primera carga.

Editá siempre theme.css y después corré:  python3 tools/inline-theme.py
"""
import glob, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALTEAR = {'asesoria.html', 'curaduria-visual.html', 'consulting.html'}  # páginas que no se usan
LINK = '<link rel="stylesheet" href="/theme.css" />'
INICIO, FIN = '<!-- THEME-CSS: copia de theme.css, no editar acá -->', '<!-- /THEME-CSS -->'

css = open(os.path.join(RAIZ, 'theme.css'), encoding='utf-8').read().strip()
bloque = f'{INICIO}\n  <style>\n{css}\n  </style>\n  {FIN}'
cambiadas = []
for ruta in sorted(glob.glob(os.path.join(RAIZ, '*.html')) + glob.glob(os.path.join(RAIZ, 'blog', '*.html')) + glob.glob(os.path.join(RAIZ, 'en', '*.html'))):
    nombre = os.path.relpath(ruta, RAIZ)
    if os.path.basename(ruta) in SALTEAR:
        continue
    s = open(ruta, encoding='utf-8').read()
    nuevo = re.sub(re.escape(INICIO) + r'.*?' + re.escape(FIN), lambda m: bloque, s, flags=re.S) if INICIO in s else s.replace(LINK, bloque, 1)
    if nuevo != s:
        open(ruta, 'w', encoding='utf-8').write(nuevo)
        cambiadas.append(nombre)
print(f'{len(cambiadas)} páginas actualizadas:', ', '.join(cambiadas))
