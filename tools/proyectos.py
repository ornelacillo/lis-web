#!/usr/bin/env python3
"""Arma las páginas de proyecto (/proyectos/<slug>) a partir de la lista PROYECTOS.

Toma el encabezado, el menú y el pie de una nota del blog para que todo quede igual al resto
del sitio, y escribe proyectos/<slug>.html. Las imágenes van en img/proyectos/<slug>/.

    python3 tools/proyectos.py
"""
import html, json, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RAIZ, 'blog', 'portfolio-estudio-de-arquitectura.html')
SITIO = 'https://liscreativestudio.com'

PROYECTOS = [
    {
        'slug': 'bwild',
        'nombre': 'BWILD',
        'bajada': 'Web para un estudio de arquitectura e interiorismo en Buenos Aires',
        'titulo_seo': 'BWILD, web para un estudio de arquitectura e interiorismo · LIS',
        'descripcion': 'Cómo diseñamos la web de BWILD, el estudio de arquitectura e interiorismo de Josefina en Buenos Aires: fotos de obra protagonistas, tres líneas de trabajo claras y cada obra contada como un caso.',
        'resumen': 'LIS. Creative Studio diseñó y desarrolló la web de BWILD, un estudio de arquitectura e interiorismo de Buenos Aires: un sitio luminoso con las fotos de obra como protagonistas, sus tres líneas de trabajo (interiorismo, reformas y espacios de trabajo) explicadas en la portada, cada obra contada como un caso y un botón para agendar una llamada siempre a mano.',
        'servicio': 'Diseño web',
        'intro': [
            'BWILD es el estudio de arquitectura e interiorismo de Josefina en Buenos Aires, que trabaja con una idea muy clara: creatividad al servicio del diseño y diseño al servicio del bienestar. Tenía obras con historias muy lindas para contar y necesitaba una web a la altura, que explicara sus tres líneas de trabajo, mostrara cada obra como un caso y llevara a agendar una llamada.',
            'Diseñamos un sitio contundente y luminoso, con las fotos de obra como protagonistas y los textos del estudio como parte del diseño, en tipografía grande y con las palabras clave en negrita.',
        ],
        'ficha': [
            ('Cliente', 'BWILD, estudio de Josefina'),
            ('Rubro', 'Arquitectura e interiorismo'),
            ('Lugar', 'Buenos Aires, Argentina'),
            ('Alcance', 'Diseño UI, desarrollo responsive y carga de proyectos'),
        ],
        'web': 'https://bwild.com.ar',
        'cliente_org': {'name': 'BWILD', 'url': 'https://bwild.com.ar'},
        'columnas': [
            ('El desafío', 'Mostrar la forma de pensar del estudio y no solo las fotos, con tres líneas de trabajo muy distintas (interiorismo, reformas y espacios de trabajo) que se tenían que entender de un vistazo.'),
            ('La idea', 'Una casa vivida, más que una de revista. Por eso las fotos muestran gente usando los espacios y los textos hablan del bienestar, la familia y la vida social de quien vive ahí.'),
            ('El sistema', 'Inter en tres pesos, una base de negro, grafito y hueso y un verde lima que le da energía a la marca, con el botón para agendar una llamada siempre a mano, desde la portada hasta el último proyecto.'),
        ],
        # Galería: cada fila es una lista de piezas; ('img', archivo, alt) o ('video', archivo, poster, alt)
        'filas_arriba': [
            [('img', 'portada.webp', 'Logo de BWILD en blanco sobre la foto de una cocina con patio diseñada por el estudio')],
            [('img', 'home.webp', 'Portada de la web de BWILD en una ventana de navegador, con la frase Smart design for creative living')],
        ],
        'filas_abajo': [
            [('img', 'sistema.webp', 'Sistema visual de BWILD: tipografía Inter, paleta de negro, grafito, gris, hueso y lima, y botones'),
             ('img', 'secciones.webp', 'Dos secciones de la web de BWILD sobre fondo lima: servicios y cómo trabajan')],
            [('video', 'recorrido.mp4', 'recorrido.jpg', 'Recorrido en movimiento por la portada de la web de BWILD')],
            [('img', 'proyectos.webp', 'Listado de proyectos y página de una obra en la web de BWILD'),
             ('img', 'mobile.webp', 'La web de BWILD en cuatro celulares, con cada sección acomodada en una columna')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': None,  # slug del próximo proyecto, cuando exista
    },
]


def e(s):
    return html.escape(s, quote=True)


def pieza(slug, p, i):
    carpeta = f'/img/proyectos/{slug}/'
    if p[0] == 'video':
        _, archivo, poster, alt = p
        return (f'<div class="pj-media"><video src="{carpeta}{archivo}" poster="{carpeta}{poster}" autoplay muted loop playsinline '
                f'preload="none" aria-label="{e(alt)}"></video></div>')
    _, archivo, alt = p
    carga = 'eager" fetchpriority="high' if i == 0 else 'lazy'
    return f'<div class="pj-media"><img src="{carpeta}{archivo}" alt="{e(alt)}" loading="{carga}" decoding="async" /></div>'


def filas(slug, lista, inicio=0):
    out, i = [], inicio
    for fila in lista:
        piezas = []
        for p in fila:
            piezas.append(pieza(slug, p, i)); i += 1
        out.append(f'    <div class="pj-row pj-{len(fila)} fi">\n      ' + '\n      '.join(piezas) + '\n    </div>')
    return '\n'.join(out), i


CSS = '''<style>/* Páginas de proyecto (tools/proyectos.py) */
.pj { max-width: 1440px; margin: 0 auto; padding: 150px 40px 40px; }
.pj-back { display: inline-block; font-family: Inter, Helvetica, Arial, sans-serif; font-size: 14px; color: var(--ink); text-decoration: none; opacity: .65; margin-bottom: 36px; transition: opacity .2s; }
.pj-back:hover { opacity: 1; }
.pj-head { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: start; margin-bottom: 56px; }
.pj-title { font-family: var(--font-display); font-weight: 500; text-transform: uppercase; letter-spacing: -.05em; line-height: .88; font-size: clamp(64px, 10vw, 156px); color: var(--ink); }
.pj-bajada { font-family: var(--font-script); font-style: italic; font-size: clamp(22px, 2.2vw, 30px); line-height: 1.2; margin-top: 18px; max-width: 520px; }
.pj-web { display: inline-flex; align-items: center; gap: 8px; margin-top: 28px; background: var(--ink); color: var(--cream); padding: 13px 24px; border-radius: 4px; font-family: Inter, Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 500; letter-spacing: .06em; text-transform: uppercase; text-decoration: none; transition: background .2s; }
.pj-web:hover { background: var(--gray); }
.pj-intro p { font-size: 17px; line-height: 1.6; margin-bottom: 16px; }
.pj-ficha { margin-top: 28px; border-top: 1px solid var(--ink); }
.pj-ficha div { display: grid; grid-template-columns: 120px 1fr; gap: 16px; padding: 11px 0; border-bottom: 1px solid var(--soft); font-size: 14px; }
.pj-ficha dt { color: var(--gray); }
.pj-row { display: grid; gap: 16px; margin-bottom: 16px; }
.pj-1 { grid-template-columns: 1fr; }
.pj-2 { grid-template-columns: 1fr 1fr; }
.pj-3 { grid-template-columns: 1fr 1fr 1fr; }
.pj-media { overflow: hidden; border-radius: 4px; background: var(--soft); }
.pj-media img, .pj-media video { display: block; width: 100%; height: auto; }
.pj-cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; margin: 72px 0 88px; }
.pj-cols > div { border-top: 1px solid var(--ink); padding-top: 18px; }
.pj-cols h2 { font-family: var(--font-display); font-weight: 500; letter-spacing: -.03em; font-size: 26px; line-height: 1.1; margin-bottom: 12px; }
.pj-cols p { font-size: 15px; line-height: 1.6; }
.pj-tienda { display: flex; justify-content: space-between; align-items: center; gap: 32px; margin: 88px 0 0; padding: 36px 0; border-top: 1px solid var(--ink); border-bottom: 1px solid var(--ink); }
.pj-tienda p { font-size: 18px; line-height: 1.5; max-width: 640px; }
.pj-tienda a { flex-shrink: 0; display: inline-flex; background: #6f6b64; color: var(--cream); padding: 13px 24px; border-radius: 4px; font-size: 12px; font-weight: 500; letter-spacing: .06em; text-transform: uppercase; text-decoration: none; transition: background .2s; }
.pj-tienda a:hover { background: var(--ink); }
.pj-next { display: block; padding: 72px 0 96px; text-decoration: none; color: var(--ink); }
.pj-next span { display: block; font-family: var(--font-script); font-style: italic; font-size: 26px; margin-bottom: 8px; }
.pj-next strong { display: block; font-family: var(--font-display); font-weight: 500; text-transform: uppercase; letter-spacing: -.05em; line-height: .9; font-size: clamp(48px, 8vw, 120px); transition: opacity .2s; }
.pj-next:hover strong { opacity: .6; }
@media (max-width: 860px) {
  .pj { padding: 120px 16px 24px; }
  .pj-head { grid-template-columns: 1fr; gap: 32px; }
  .pj-2, .pj-3, .pj-cols { grid-template-columns: 1fr; }
  .pj-row { gap: 10px; margin-bottom: 10px; }
  .pj-cols { gap: 28px; margin: 48px 0 56px; }
  .pj-ficha div { grid-template-columns: 96px 1fr; }
  .pj-tienda { flex-direction: column; align-items: flex-start; }
}
</style>'''


def jsonld(obj):
    return '  <script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n  </script>'


def construir(p, base, todos):
    slug, url = p['slug'], f"{SITIO}/proyectos/{p['slug']}"
    img_og = f"{SITIO}/img/proyectos/{slug}/{p['portada_og']}"

    i_desc = base.index('  <meta name="description"')
    i_vis = base.index('  <!-- Sistema visual 2026 -->')
    i_head = base.index('</head>')
    i_body = base.index('<body')
    i_hero = base.index('  <!-- ══ HERO ══ -->')
    i_foot = base.index('  <!-- ══ FOOTER ══ -->')

    cabeza = re.sub(r'<title>.*?</title>', f"<title>{e(p['titulo_seo'])}</title>", base[:i_desc], count=1)

    obra = {
        '@context': 'https://schema.org', '@type': 'CreativeWork',
        'name': f"{p['nombre']} · {p['bajada']}", 'headline': p['bajada'],
        'description': p['descripcion'], 'abstract': p['resumen'],
        'url': url, 'mainEntityOfPage': url, 'image': img_og, 'inLanguage': 'es-AR',
        'genre': p['servicio'],
        'about': {'@type': 'Organization', **p['cliente_org']},
        'creator': {'@id': f'{SITIO}/#business'},
        'author': {'@type': 'Person', '@id': f'{SITIO}/#ornela', 'name': 'Ornela Cillo'},
        'publisher': {'@type': 'Organization', '@id': f'{SITIO}/#business', 'name': 'LIS. Creative Studio'},
    }
    migas = {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': f'{SITIO}/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Proyectos', 'item': f'{SITIO}/#portfolio'},
            {'@type': 'ListItem', 'position': 3, 'name': p['nombre'], 'item': url},
        ],
    }
    meta = f'''  <meta name="description" content="{e(p['descripcion'])}" />
  <link rel="canonical" href="{url}" />
{jsonld(obra)}
{jsonld(migas)}
  <meta name="theme-color" content="#f4ede3" />
  <meta property="og:title" content="{e(p['nombre'])} · {e(p['bajada'])}" />
  <meta property="og:description" content="{e(p['descripcion'])}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="es_AR" />
  <meta property="og:site_name" content="LIS. Creative Studio" />
  <meta property="og:image" content="{img_og}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(p['nombre'])} · {e(p['bajada'])}" />
  <meta name="twitter:description" content="{e(p['descripcion'])}" />
  <meta name="twitter:image" content="{img_og}" />
'''
    head_fin = base[i_vis:i_head].replace(base[i_vis:i_head], base[i_vis:i_head])
    cuerpo_ini = base[i_body:i_hero].replace(' style="opacity:.45"', '')

    arriba, n = filas(slug, p['filas_arriba'])
    abajo, _ = filas(slug, p['filas_abajo'], n)
    intro = '\n'.join(f'        <p>{e(t)}</p>' for t in p['intro'])
    ficha = '\n'.join(f'          <div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p['ficha'])
    cols = '\n'.join(f'      <div><h2>{e(t)}</h2><p>{e(x)}</p></div>' for t, x in p['columnas'])
    web = f'\n        <a class="pj-web" href="{p["web"]}" target="_blank" rel="noopener">Ver la web online →</a>' if p.get('web') else ''

    sig = next((q for q in todos if q['slug'] == p.get('siguiente')), None)
    if sig:
        siguiente = f'''    <a class="pj-next fi" href="/proyectos/{sig['slug']}"><span>Siguiente proyecto</span><strong>{e(sig['nombre'])} →</strong></a>'''
    else:
        siguiente = '''    <a class="pj-next fi" href="/#portfolio"><span>Seguí mirando</span><strong>Todos los proyectos →</strong></a>'''

    contenido = f'''  <!-- ══ PROYECTO ══ -->
  <main class="pj">
    <a href="/#portfolio" class="pj-back fi">← Todos los proyectos</a>
    <header class="pj-head">
      <div class="fi">
        <h1 class="pj-title">{e(p['nombre'])}</h1>
        <p class="pj-bajada">{e(p['bajada'])}</p>{web}
      </div>
      <div class="pj-intro fi fi-d1">
{intro}
        <dl class="pj-ficha">
{ficha}
        </dl>
      </div>
    </header>

{arriba}

    <section class="pj-cols" aria-label="Sobre el proyecto">
{cols}
    </section>

{abajo}

    <div class="pj-tienda fi">
      <p>Si sos diseñadora, las plantillas con las que presento y entrego cada proyecto están en la tienda, listas para editar con tu marca.</p>
      <a href="/tienda">Ver la tienda</a>
    </div>

{siguiente}
  </main>

'''
    return cabeza + meta + head_fin + CSS + '\n' + base[i_head:i_body] + cuerpo_ini + contenido + base[i_foot:]


def main():
    base = open(BASE, encoding='utf-8').read()
    os.makedirs(os.path.join(RAIZ, 'proyectos'), exist_ok=True)
    for p in PROYECTOS:
        ruta = os.path.join(RAIZ, 'proyectos', p['slug'] + '.html')
        open(ruta, 'w', encoding='utf-8').write(construir(p, base, PROYECTOS))
        print('ok', os.path.relpath(ruta, RAIZ))


if __name__ == '__main__':
    main()
