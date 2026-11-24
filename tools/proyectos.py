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
        'siguiente': 'green-golden',  # slug del próximo proyecto
    },
    {
        'slug': 'green-golden',
        'nombre': 'Green Golden',
        'bajada': 'Identidad visual y web para un espacio de congresos y eventos en Barcelona',
        'titulo_seo': 'Green Golden, identidad visual y web para un espacio de eventos en Barcelona · LIS',
        'descripcion': 'Identidad visual, íconos y web para Green Golden Congress BCN Events, un espacio de congresos y eventos en Barcelona: un monograma de dos G, un verde muy oscuro y una web con los formatos de sala a un clic.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual, los íconos y la web de Green Golden Congress BCN Events, un espacio para eventos corporativos, formaciones y presentaciones a pasos de Fira Gran Via, en Barcelona. El sistema parte de un monograma de dos G enfrentadas sobre un verde muy oscuro, y la web muestra fotos reales de los eventos, la propuesta gastronómica y siete formatos de sala con su capacidad.',
        'servicio': 'Identidad visual y diseño web',
        'intro': [
            'Green Golden Congress BCN Events es un espacio para eventos corporativos, formaciones y presentaciones a pasos de Fira Gran Via, en Barcelona, con propuesta gastronómica propia. Trabajamos la marca y la web para que una empresa que busca dónde hacer su evento entienda en minutos qué puede hacer ahí, para cuántas personas y cómo reservar.',
            'La marca parte de un monograma de dos G enfrentadas sobre un verde muy oscuro, que funciona como sello en la entrada del espacio y en todas las piezas, y la web pone las fotos de los eventos, los formatos de sala y la ubicación a un clic.',
        ],
        'ficha': [
            ('Cliente', 'Green Golden Congress BCN Events'),
            ('Rubro', 'Espacio de eventos y congresos'),
            ('Lugar', "L'Hospitalet de Llobregat, Barcelona"),
            ('Alcance', 'Identidad visual, íconos y diseño web'),
        ],
        'web': None,
        'cliente_org': {'name': 'Green Golden Congress BCN Events'},
        'columnas': [
            ('El desafío', 'Que el espacio se venda solo antes de la visita, mostrando la sala, la luz y los materiales con fotos de eventos reales y no con renders.'),
            ('La idea', 'Un sello más que un logo: el monograma de dos G enfrentadas, con la Della Robbia para los títulos y la Futura para los textos y los datos.'),
            ('El sistema', 'Un set de íconos para cada disposición de sala, de banquete a cabaret, con su capacidad, para que quien organiza un evento sepa en un vistazo si el espacio le sirve.'),
        ],
        'filas_arriba': [
            [('img', 'portada.webp', 'Monograma y logo de Green Golden en blanco sobre la foto de un evento en el espacio')],
            [('img', 'home.webp', 'Portada de la web de Green Golden en una ventana de navegador, con la foto de un evento y el botón Contáctanos')],
        ],
        'filas_abajo': [
            [('img', 'sistema.webp', 'Sistema visual de Green Golden: tipografías Della Robbia y Futura, paleta de verde, negro, crema y blanco, y el monograma'),
             ('img', 'eventos.webp', 'Las secciones de eventos y de propuesta gastronómica en la web de Green Golden')],
            [('video', 'recorrido.mp4', 'recorrido.jpg', 'Recorrido en movimiento por la web de Green Golden')],
            [('img', 'reales.webp', 'Fotos reales de eventos, gastronomía y salas en Green Golden'),
             ('img', 'formatos.webp', 'Íconos de los siete formatos de sala de Green Golden con su capacidad, de banquete a cabaret')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'estudio-disegna',
    },
    {
        'slug': 'estudio-disegna',
        'nombre': 'Estudio Disegna',
        'bajada': 'Web para un estudio de arquitectura e interiorismo en Fisherton y Funes',
        'titulo_seo': 'Estudio Disegna, web para un estudio de arquitectura e interiorismo · LIS',
        'descripcion': 'Cómo diseñamos la web de Estudio Disegna, el estudio de arquitectura e interiorismo de Genoveva Yerkovich en Fisherton y Funes: simple, silenciosa y con la fotografía de obra como protagonista.',
        'resumen': 'LIS. Creative Studio diseñó y desarrolló la web de Estudio Disegna, el estudio de arquitectura e interiorismo de Genoveva Yerkovich en Fisherton y Funes, Argentina. El estudio no tenía portfolio ni un lugar donde explicar sus servicios, así que el sitio muestra obras seleccionadas, sus tres líneas de trabajo, testimonios reales y dos caminos de contacto: agendar una llamada o dejar un mensaje.',
        'servicio': 'Diseño web',
        'intro': [
            'Disegna tenía obras terminadas, clientes felices y una forma muy propia de mirar los espacios, pero no tenía dónde mostrarlo. Sus trabajos vivían solo en Instagram y no había un lugar que explicara sus tres servicios: arquitectura y dirección de obra, interiorismo residencial y Disegna Selection, un asesoramiento online.',
            'La web se pensó como una extensión del nuevo universo visual del estudio, con la fotografía de obra como protagonista, tipografía grande y liviana, mucho aire y una paleta de grises cálidos con un único acento chocolate.',
        ],
        'ficha': [
            ('Cliente', 'Estudio Disegna, de Genoveva Yerkovich'),
            ('Rubro', 'Arquitectura e interiorismo residencial'),
            ('Lugar', 'Fisherton y Funes, Argentina'),
            ('Alcance', 'Estrategia de contenido, diseño UI, desarrollo responsive en WordPress'),
        ],
        'web': 'https://estudiodisegna.com',
        'cliente_org': {'name': 'Estudio Disegna', 'url': 'https://estudiodisegna.com'},
        'columnas': [
            ('El desafío', 'Mostrar el criterio del estudio sin decir de más, con una selección editorial de obras en lugar de un catálogo y tres servicios que se entendieran de un vistazo.'),
            ('La idea', 'Pasar del "me gusta" en Instagram al "quiero hablar con ellos", con una home que recorre quién está detrás, las obras, los servicios y los testimonios antes de llegar al contacto.'),
            ('El sistema', 'Neue Montreal liviana para títulos y textos, grises cálidos con un acento chocolate y botones que se repiten igual en todo el sitio, también en el celular, que es por donde llega la mayoría.'),
        ],
        'filas_arriba': [
            [('img', 'portada.webp', 'Logo de Disegna en blanco sobre la foto en blanco y negro de una casa diseñada por el estudio')],
            [('img', 'home.webp', 'Portada de la web de Disegna con la frase Una mirada integral para cada proyecto')],
        ],
        'filas_abajo': [
            [('img', 'sistema.webp', 'Sistema visual de Disegna: tipografías Neue Montreal y Quicksand, paleta de grises y chocolate, y botones'),
             ('img', 'servicios.webp', 'Sección de servicios de la web de Disegna con tres paneles fotográficos')],
            [('video', 'recorrido.mp4', 'recorrido.jpg', 'Recorrido en movimiento por la portada de la web de Disegna')],
            [('img', 'mobile.webp', 'La web de Disegna en cuatro celulares sobre fondo oscuro')],
            [('img', 'celulares.webp', 'Testimonios, novedades, contacto y pie de la web de Disegna en celulares'),
             ('img', 'fotografia.webp', 'Portadas de obras de Disegna: oficinas San Lorenzo, Morrison Fisherton, Don Mateo Funes y Yerko Campos')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'buenas-marcas',
    },
    {
        'slug': 'buenas-marcas',
        'nombre': 'Buenas Marcas',
        'bajada': 'Identidad visual, merch y web para un medio que verifica tiendas online',
        'titulo_seo': 'Buenas Marcas, identidad visual, merch y web · LIS',
        'descripcion': 'Identidad visual completa para Buenas Marcas, un medio que ayuda a comprar online con seguridad: un azul fuerte, un patrón propio y un isotipo corto, aplicados en la web, remeras, gorras y latas.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual completa de Buenas Marcas, un medio que ayuda a la gente a comprar online con seguridad verificando tiendas y contando historias de marcas. El sistema combina un azul fuerte, un patrón propio que funciona como textura y un isotipo corto, y se aplica en la web, remeras, gorras, latas y packaging.',
        'servicio': 'Identidad visual y diseño web',
        'intro': [
            'Buenas Marcas es un medio que ayuda a la gente a comprar online con seguridad, verificando tiendas y contando historias de marcas. Necesitaba verse confiable sin perder la cercanía, porque le habla a gente común que quiere saber si una tienda es real antes de pagar.',
            'Armamos un sistema con un azul fuerte, un patrón propio que funciona como textura y un isotipo corto, pensado para aplicarse igual de bien en la web que en remeras, gorras, latas y packaging.',
        ],
        'ficha': [
            ('Cliente', 'Buenas Marcas'),
            ('Rubro', 'Medio digital y verificación de tiendas online'),
            ('Lugar', 'Argentina'),
            ('Alcance', 'Identidad visual, patrón, merch y diseño web'),
        ],
        'web': 'https://buenasmarcas.ar',
        'cliente_org': {'name': 'Buenas Marcas', 'url': 'https://buenasmarcas.ar'},
        'columnas': [
            ('El desafío', 'Transmitir confianza en un rubro donde la gente desconfía, con una marca que se vea seria en una nota y simpática en una remera.'),
            ('La idea', 'Un azul que se reconoce de lejos y un patrón hecho con las letras de la marca, que funciona como textura y se puede usar solo, sin el logo.'),
            ('El sistema', 'El isotipo bm con su flecha para los espacios chicos, como una etiqueta o el costado de una gorra, y el patrón para las superficies grandes.'),
        ],
        'filas_arriba': [
            [('img', 'web.webp', 'La web de Buenas Marcas en una laptop sostenida en el aire, con el cielo de fondo')],
            [('img', 'remera.webp', 'Remera blanca con el patrón azul de Buenas Marcas en la espalda')],
        ],
        'filas_abajo': [
            [('img', 'gorra.webp', 'Gorra azul con el isotipo bm bordado atrás'),
             ('img', 'gorro.webp', 'Gorro de lana azul con la etiqueta de Buenas Marcas')],
            [('video', 'merch.mp4', 'merch.jpg', 'Las piezas de merch de Buenas Marcas en movimiento')],
            [('img', 'lata.webp', 'Lata con el nombre Buenas Marcas repetido en azul, en la mano'),
             ('img', 'platos.webp', 'Remera con el patrón de Buenas Marcas detrás de una pila de platos'),
             ('img', 'gorra-bol.webp', 'Gorra blanca de Buenas Marcas en un bol con limones')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'orfeon',
    },
    {
        'slug': 'orfeon',
        'nombre': 'Orfeon',
        'bajada': 'Identidad visual para una empresa de tecnología e inteligencia artificial',
        'titulo_seo': 'Orfeon, identidad visual para una empresa de tecnología e IA · LIS',
        'descripcion': 'Identidad visual para Orfeon, una empresa que automatiza procesos e incorpora inteligencia artificial, con dos líneas, Orfeon Tech y Orfeon Financial: una O que gira como un anillo, un azul profundo y un patrón de píxeles.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de Orfeon, una empresa que optimiza procesos, automatiza tareas e incorpora inteligencia artificial de forma práctica, con dos líneas de negocio: Orfeon Tech y Orfeon Financial. El símbolo es una O que gira como un anillo en movimiento, acompañada por un azul profundo y un patrón de píxeles, y el sistema se aplica en la app, la web, etiquetas y merch.',
        'servicio': 'Identidad visual',
        'intro': [
            'Orfeon es una empresa que optimiza procesos, automatiza tareas e incorpora inteligencia artificial de forma práctica, con dos líneas de negocio, Orfeon Tech y Orfeon Financial, que tenían que convivir bajo una misma marca.',
            'El símbolo es una O que gira como un anillo en movimiento, y lo acompañamos con un azul profundo y un patrón de píxeles que habla de tecnología sin caer en lo frío. El sistema se aplica igual de bien en la app y la web que en piezas físicas como etiquetas y merch.',
        ],
        'ficha': [
            ('Cliente', 'Orfeon'),
            ('Rubro', 'Tecnología, automatización e inteligencia artificial'),
            ('Alcance', 'Identidad visual, manual de marca, ícono de app y aplicaciones'),
        ],
        'web': None,
        'cliente_org': {'name': 'Orfeon'},
        'columnas': [
            ('El desafío', 'Una marca de tecnología que no se viera fría ni genérica, y que le diera lugar a dos líneas de negocio distintas sin perder la unidad.'),
            ('La idea', 'Una O que gira como un anillo, la idea de un proceso que se mueve solo, y que funciona igual como ícono de app que bordada en una etiqueta.'),
            ('El sistema', 'Cinco azules, de un azul casi negro a un celeste hielo, y un patrón de píxeles que sirve de fondo para la web, las presentaciones y las piezas.'),
        ],
        'filas_arriba': [
            [('img', 'relieve.webp', 'El símbolo de Orfeon en relieve sobre papel azul')],
            [('img', 'lineas.webp', 'Las dos líneas de la marca, Orfeon Financial y Orfeon Tech, en azul')],
        ],
        'filas_abajo': [
            [('img', 'patron.webp', 'Patrón de píxeles de Orfeon en distintos azules'),
             ('img', 'paleta.webp', 'Paleta de cinco azules de Orfeon con sus códigos')],
            [('video', 'logo.mp4', 'logo.jpg', 'Animación del símbolo de Orfeon')],
            [('img', 'etiqueta.webp', 'Etiqueta tejida con el símbolo de Orfeon'),
             ('img', 'laptop.webp', 'Presentación de Orfeon con el patrón de píxeles en una laptop'),
             ('img', 'tejido.webp', 'Etiqueta de Orfeon cosida en un tejido azul, entre los dedos')],
            [('img', 'etiqueta-celular.webp', 'Etiqueta de Orfeon en un tejido y la app en un celular')],
            [('img', 'app.webp', 'El ícono de la app de Orfeon en la pantalla de un celular')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'santo-pastel',
    },
    {
        'slug': 'santo-pastel',
        'nombre': 'Santo Pastel',
        'bajada': 'Identidad visual e ilustración para un café y pastelería artesanal',
        'titulo_seo': 'Santo Pastel, identidad visual e ilustración para un café y pastelería · LIS',
        'descripcion': 'Identidad visual para Santo Pastel, un café y pastelería artesanal: un logo de trazo manual que se apoya sobre las fotos, una paleta del grano a la medialuna e ilustraciones tipo sticker para redes.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de Santo Pastel, un café y pastelería artesanal con recetas clásicas, café de especialidad y helado. El sistema combina un logo de trazo manual, una cursiva suelta con una tipografía alta y delgada, pensado para apoyarse sobre las fotos del café, una paleta tomada del grano a la medialuna, un set de ilustraciones tipo sticker y plantillas para redes.',
        'servicio': 'Identidad visual e ilustración',
        'intro': [
            'Santo Pastel es un café y pastelería artesanal con recetas clásicas, café de especialidad y helado. Necesitaba una identidad cálida y cercana, que se sintiera hecha a mano sin perder prolijidad, y un sistema de piezas para que sus redes tuvieran una voz propia.',
            'Diseñamos un logo de trazo manual que combina una cursiva suelta con una tipografía alta y delgada, pensado para apoyarse sobre las fotos del café y los productos, una paleta tomada del grano a la medialuna y un set de ilustraciones tipo sticker.',
        ],
        'ficha': [
            ('Cliente', 'Santo Pastel'),
            ('Rubro', 'Café y pastelería artesanal'),
            ('Alcance', 'Identidad visual, ilustraciones y plantillas para redes'),
        ],
        'web': None,
        'cliente_org': {'name': 'Santo Pastel'},
        'columnas': [
            ('El desafío', 'Que la marca se sintiera como entrar a un café de barrio, con olor a medialunas recién hechas, y que al mismo tiempo se viera prolija en cada pieza.'),
            ('La idea', 'Una firma más que un logo, de trazo manual y en blanco, que vive sobre las fotos del café, el grano y los productos en lugar de competir con ellas.'),
            ('El sistema', 'Seis colores del espresso al celeste, ilustraciones con borde blanco para redes, packaging y vidriera, y plantillas para el feed con fotos de producto recortadas.'),
        ],
        'filas_arriba': [
            [('img', 'portada.webp', 'Logo de Santo Pastel en blanco sobre la foto de un helado en una calle')],
            [('img', 'fotos.webp', 'El logo de Santo Pastel sobre cuatro fotos de café, grano y productos')],
        ],
        'filas_abajo': [
            [('img', 'paleta.webp', 'Paleta de Santo Pastel: espresso, café con leche, caramelo, durazno, celeste y crema'),
             ('img', 'ilustraciones.webp', 'Ilustraciones tipo sticker de Santo Pastel: medialuna, taza, moka, vaso, granos y cafetera')],
            [('video', 'ilustraciones-mov.mp4', 'ilustraciones-mov.jpg', 'Las ilustraciones de Santo Pastel en movimiento')],
            [('img', 'redes.webp', 'Plantillas para redes de Santo Pastel con una medialuna y un helado recortados')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'menatech',
    },
    {
        'slug': 'menatech',
        'nombre': 'MenaTech',
        'bajada': 'Identidad visual y redes para una empresa de tecnología e inteligencia artificial',
        'titulo_seo': 'MenaTech, identidad visual y redes para una empresa de tecnología · LIS',
        'descripcion': 'Identidad visual para MenaTech, una empresa de tecnología e inteligencia artificial: un logo con una flecha que sube, cinco colores para separar temas, plantillas de Instagram y aplicaciones en papelería, cuadernos, remeras y tazas.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de MenaTech, una empresa de tecnología e inteligencia artificial con la idea de tecnología que ordena tu negocio. El sistema tiene un logo con una flecha que sube, una paleta de verde, violeta, celeste, gris y naranja para separar temas, Montserrat como tipografía, el perfil y las plantillas de Instagram, y aplicaciones en papelería, cuadernos, remeras y tazas.',
        'servicio': 'Identidad visual y redes',
        'intro': [
            'MenaTech es una empresa de tecnología e inteligencia artificial con una idea muy clara: tecnología que ordena tu negocio. Necesitaba una marca que se entendiera rápido y que pudiera hablar de temas muy distintos en redes sin perder la unidad.',
            'Diseñamos un logo con una flecha que sube, una paleta de cinco colores para separar temas y Montserrat como tipografía de todo el sistema, y armamos el perfil y las plantillas de Instagram junto con las aplicaciones en papelería, cuadernos, remeras y tazas.',
        ],
        'ficha': [
            ('Cliente', 'MenaTech'),
            ('Rubro', 'Tecnología e inteligencia artificial'),
            ('Alcance', 'Identidad visual, plantillas de Instagram y aplicaciones'),
        ],
        'web': None,
        'cliente_org': {'name': 'MenaTech'},
        'columnas': [
            ('El desafío', 'Que una empresa de inteligencia artificial se viera cercana y ordenada, y no como una más de las que prometen todo con fondos oscuros y brillos.'),
            ('La idea', 'Una flecha que sube dentro de la M, la idea de un negocio que crece cuando se ordena, que funciona sola en espacios chicos y completa en el logo.'),
            ('El sistema', 'Verde, violeta, celeste, gris y naranja, cada uno para un tema, y plantillas de Instagram que cambian de color sin dejar de verse de la misma marca.'),
        ],
        'filas_arriba': [
            [('img', 'tarjetas.webp', 'Tarjetas de MenaTech, una naranja con el patrón y una blanca con el logo, sobre escalones grises')],
            [('img', 'logos.webp', 'Versiones del logo de MenaTech en blanco, naranja y gris')],
        ],
        'filas_abajo': [
            [('img', 'paleta.webp', 'Paleta de MenaTech: verde, violeta, celeste, gris y naranja')],
            [('img', 'piezas.webp', 'Piezas de MenaTech en verde y violeta sobre una oficina'),
             ('img', 'piezas-2.webp', 'Historias de MenaTech en violeta y celeste sobre una oficina')],
            [('img', 'instagram.webp', 'Posteos de MenaTech en dos celulares')],
            [('img', 'cuadernos.webp', 'Cuadernos negro y verde de MenaTech en la mano'),
             ('img', 'remera.webp', 'Remera blanca con el patrón de MenaTech en la espalda')],
            [('img', 'taza.webp', 'Taza blanca con el logo de MenaTech'),
             ('img', 'laptop.webp', 'Una presentación de MenaTech en una laptop'),
             ('img', 'celular.webp', 'Un posteo de MenaTech en un celular')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'pastas-prin',
    },
    {
        'slug': 'pastas-prin',
        'nombre': 'Pastas Prin',
        'bajada': 'Identidad visual e ilustración para una marca de pastas frescas',
        'titulo_seo': 'Pastas Prin, identidad visual e ilustración para una marca de pastas frescas · LIS',
        'descripcion': 'Identidad visual para Pastas Prin, una marca de pastas frescas: personajes ilustrados que amasan y cocinan, un patrón de pastas en rosa y crema y un azul fuerte, en el menú, los afiches, la bolsa y las redes.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de Pastas Prin, una marca de pastas frescas que quería verse cálida, familiar y con mucho carácter. El sistema tiene personajes ilustrados que amasan y cocinan, un patrón de pastas en rosa y crema y un azul fuerte para el logo, y se aplica en el menú, los afiches, la bolsa y las piezas para redes.',
        'servicio': 'Identidad visual e ilustración',
        'intro': [
            'Pastas Prin es una marca de pastas frescas que quería verse cálida, familiar y con mucho carácter, lejos de la típica estética de fábrica de pastas.',
            'Armamos un sistema ilustrado con personajes que amasan y cocinan, un patrón de pastas en rosa y crema y un azul fuerte para el logo, y lo llevamos al menú, a los afiches, a la bolsa y a las piezas para redes.',
        ],
        'ficha': [
            ('Cliente', 'Pastas Prin'),
            ('Rubro', 'Pastas frescas'),
            ('Alcance', 'Identidad visual, ilustración, patrón, menú, packaging y redes'),
        ],
        'web': None,
        'cliente_org': {'name': 'Pastas Prin'},
        'columnas': [
            ('El desafío', 'Que una marca de pastas frescas se sintiera familiar sin caer en lo antiguo, y que tuviera piezas suficientes para el local, el delivery y las redes.'),
            ('La idea', 'Personajes que amasan, cortan y cocinan, dibujados con trazo azul, para que la marca cuente cómo se hacen las pastas en lugar de solo mostrarlas.'),
            ('El sistema', 'Un azul fuerte para el logo y los afiches, un patrón de ravioles, moños y tallarines en rosa y crema, y stickers que se combinan con fotos de producto.'),
        ],
        'filas_arriba': [
            [('img', 'afiche.webp', 'Afiche azul de Pastas Prin con un tenedor y tallarines, colgado en un restaurante'),
             ('img', 'personajes.webp', 'Cuatro personajes ilustrados de Pastas Prin amasando y cocinando')],
            [('img', 'patron.webp', 'Patrón de pastas de Pastas Prin en rosa y crema'),
             ('img', 'patron-detalle.webp', 'Detalle del patrón de Pastas Prin con un raviol grande')],
        ],
        'filas_abajo': [
            [('video', 'piezas.mp4', 'piezas.jpg', 'Piezas de Pastas Prin en movimiento'),
             ('img', 'mesa.webp', 'Ilustraciones de pastas en blanco sobre una mesa servida')],
            [('img', 'stickers.webp', 'Stickers de Pastas Prin con el chef y platos de pasta'),
             ('img', 'posteo.webp', 'Posteo naranja de Pastas Prin con stickers de comida'),
             ('img', 'posteo-2.webp', 'Posteo naranja de Pastas Prin con pastas secas y el chef')],
            [('img', 'menu.webp', 'Menú de Pastas Prin colgado en la pared de un local'),
             ('img', 'bolsa.webp', 'Bolsa celeste de Pastas Prin con un personaje, en la mano'),
             ('img', 'vidriera.webp', 'Ilustraciones de pastas de Pastas Prin sobre la foto de un local')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'carpetania',
    },
    {
        'slug': 'carpetania',
        'nombre': 'Carpetania',
        'bajada': 'Identidad visual para una cafetería de especialidad',
        'titulo_seo': 'Carpetania, identidad visual para una cafetería de especialidad · LIS',
        'descripcion': 'Identidad visual para Carpetania, una cafetería de especialidad donde la tradición se encuentra con la pasión por el café: una paleta de tostados y chocolate, un símbolo de trazo continuo y aplicaciones en vasos, bolsas y remeras.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de Carpetania, una cafetería de especialidad inspirada en la historia de la región que lleva su nombre, con el lema "Donde la tradición se encuentra con la pasión por el café". El sistema combina un logotipo de letras gruesas, un símbolo de trazo continuo, una paleta de tostados, terracota y chocolate, y aplicaciones en vasos, bolsas, papelería y remeras.',
        'servicio': 'Identidad visual',
        'intro': [
            'Carpetania es una cafetería de especialidad inspirada en la historia de la región que lleva su nombre, pensada como un lugar donde el tiempo se detiene y cada taza cuenta una historia. Su lema lo resume: donde la tradición se encuentra con la pasión por el café.',
            'Diseñamos un logotipo de letras gruesas y redondeadas, un símbolo de trazo continuo que aparece solo en los vasos, las remeras y hasta en el arte del latte, y una paleta tomada del café, de los tostados claros al chocolate.',
        ],
        'ficha': [
            ('Rubro', 'Cafetería de especialidad'),
            ('Alcance', 'Identidad visual, paleta, papelería y aplicaciones'),
        ],
        'web': None,
        'cliente_org': {'name': 'Carpetania'},
        'columnas': [
            ('El desafío', 'Que una cafetería nueva transmitiera tradición y oficio desde el primer vaso, sin verse antigua ni parecerse a todas las cafeterías de especialidad.'),
            ('La idea', 'Un símbolo de trazo continuo, simple como un dibujo a mano, que funciona solo sobre cualquier soporte y le da a la marca algo para reconocerla sin el nombre.'),
            ('El sistema', 'Cinco colores, del arena al chocolate pasando por un terracota fuerte, el logotipo para la fachada y el packaging, y el símbolo para los vasos y el merch.'),
        ],
        'filas_arriba': [
            [('img', 'bolsa.webp', 'Bolsa de papel de Carpetania con el patrón de la marca sobre una mesa de madera')],
            [('img', 'vasos.webp', 'Vasos de café de Carpetania con el símbolo'),
             ('img', 'tarjetas.webp', 'Tarjetas de Carpetania en marrón y blanco sobre madera')],
        ],
        'filas_abajo': [
            [('img', 'paleta.webp', 'Paleta de Carpetania: arena, gris tostado, terracota, chocolate y caramelo')],
            [('video', 'logo.mp4', 'logo.jpg', 'Animación del logotipo de Carpetania')],
            [('img', 'cafetera.webp', 'Café y cafetera en una barra con el packaging de Carpetania'),
             ('img', 'remera.webp', 'Remera blanca con el símbolo de Carpetania')],
            [('img', 'vaso-calle.webp', 'Un vaso de Carpetania en la mano frente a una cafetería de noche'),
             ('img', 'remera-negra.webp', 'Remera negra con el símbolo de Carpetania')],
            [('video', 'cafe.mp4', 'cafe.jpg', 'Packaging de café de Carpetania junto al símbolo'),
             ('video', 'latte.mp4', 'latte.jpg', 'El símbolo de Carpetania dibujado en un latte')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'jeudi',
    },
    {
        'slug': 'jeudi',
        'nombre': 'Jeudi',
        'bajada': 'Identidad visual para una marca de ropa',
        'titulo_seo': 'Jeudi, identidad visual para una marca de ropa · LIS',
        'descripcion': 'Identidad visual para Jeudi, una marca de ropa con una idea simple, tu jueves todos los días: un logotipo con la tipografía LK Ternima, una paleta de marrones y azul pizarra y aplicaciones en bolsas, remeras y pilusos.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de Jeudi, una marca de ropa cuyo lema es "Tu jueves, todos los días", la idea de vivir la espontaneidad y la comodidad del jueves cualquier día de la semana. El sistema combina un logotipo con la tipografía LK Ternima DCU, un isotipo de tres líneas, una paleta de marrones y azul pizarra y aplicaciones en bolsas, remeras, libros y pilusos.',
        'servicio': 'Identidad visual',
        'intro': [
            'Jeudi es una marca de ropa con una frase que la resume: tu jueves, todos los días. La idea es vivir la espontaneidad y la comodidad del jueves cualquier día de la semana, con prendas en las que sus clientas se sientan identificadas y que reflejen su estilo.',
            'El logotipo está armado con la LK Ternima DCU, una tipografía moderna y desenfadada que le da un aire joven, y lo acompañamos con un isotipo de tres líneas, una paleta de marrones y azul pizarra y fotos de calle en tonos fríos.',
        ],
        'ficha': [
            ('Rubro', 'Marca de ropa'),
            ('Alcance', 'Identidad visual, tipografía, paleta y aplicaciones'),
        ],
        'web': None,
        'cliente_org': {'name': 'Jeudi'},
        'columnas': [
            ('El desafío', 'Una marca de ropa para un público joven que se sintiera actual y con carácter, sin depender de una tendencia que pase de moda en una temporada.'),
            ('La idea', 'El jueves como estado de ánimo, con la semana casi terminada, más libertad y más ganas de salir, llevado a una marca que se usa todos los días.'),
            ('El sistema', 'La LK Ternima para el logotipo y la Futura para los textos, cinco colores de marrones y azul pizarra, y un isotipo de tres líneas para etiquetas y bordados.'),
        ],
        'filas_arriba': [
            [('img', 'portada.webp', 'Logotipo de Jeudi en blanco sobre la foto en blanco y negro de una chica con un café')],
            [('img', 'fotos.webp', 'Fotos de calle de la marca Jeudi, con abrigos y café'),
             ('img', 'fotos-2.webp', 'Fotos de Jeudi con zapatillas y jeans en la calle')],
        ],
        'filas_abajo': [
            [('img', 'paleta.webp', 'Paleta de Jeudi en marrones y azul pizarra'),
             ('img', 'tipografia.webp', 'Tipografías de Jeudi: LK Ternima DCU y Futura')],
            [('video', 'logo.mp4', 'logo.jpg', 'Animación del logotipo de Jeudi')],
            [('img', 'escalera.webp', 'El isotipo de Jeudi sobre la foto de una escalera'),
             ('img', 'zapatillas.webp', 'Zapatillas blancas con la paleta de Jeudi')],
            [('img', 'remera.webp', 'Remera blanca con cámara y fotos, en el universo de Jeudi'),
             ('img', 'libro.webp', 'Libro y remera con el logotipo de Jeudi')],
            [('img', 'bolsa.webp', 'Bolsa blanca de Jeudi colgada de un bolso'),
             ('img', 'piluso.webp', 'Piluso verde con el isotipo de Jeudi')],
            [('video', 'ventana.mp4', 'ventana.jpg', 'Foto de Jeudi en blanco y negro con la marca en una ventana')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'golden-hour',
    },
    {
        'slug': 'golden-hour',
        'nombre': 'Golden Hour',
        'bajada': 'Identidad visual para una joyería de autor',
        'titulo_seo': 'Golden Hour, identidad visual para una joyería de autor · LIS',
        'descripcion': 'Identidad visual para Golden Hour, una joyería de autor con piezas únicas y personalizadas: un logotipo de serif fina, una paleta de chocolate, canela y miel y patrones para la papelería.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de Golden Hour, una joyería de autor que ofrece piezas únicas y personalizadas para mujeres que buscan expresar su individualidad, inspiradas en la belleza natural y la luz dorada. El sistema combina un logotipo de serif fina, una paleta de chocolate, canela, miel y choco blanco, patrones de puntos y líneas y aplicaciones en sobres, tarjetas y vasos.',
        'servicio': 'Identidad visual',
        'intro': [
            'Golden Hour es una joyería de autor que ofrece piezas únicas y personalizadas, diseñadas para mujeres que buscan expresar su individualidad. Sus piezas se inspiran en la belleza natural y en la luz dorada, y son una celebración de la feminidad y el estilo personal.',
            'Quisimos que el logotipo transmitiera la exclusividad y la artesanía de cada pieza, con una serif fina y delicada, y lo acompañamos con una paleta de chocolates y mieles y patrones suaves para que la experiencia de compra se sienta especial.',
        ],
        'ficha': [
            ('Rubro', 'Joyería de autor'),
            ('Alcance', 'Identidad visual, paleta, patrones y papelería'),
        ],
        'web': None,
        'cliente_org': {'name': 'Golden Hour'},
        'columnas': [
            ('El desafío', 'Que una joyería chica se viera exclusiva y artesanal a la vez, a la altura de piezas únicas, sin caer en el dorado brillante de siempre.'),
            ('La idea', 'La hora dorada, la luz cálida del atardecer, llevada a una paleta de chocolate, canela y miel y a fotos con piel, tela y luz natural.'),
            ('El sistema', 'Un logotipo de serif fina, cinco colores con nombre propio y dos patrones, uno de puntos y otro de líneas, para sobres, tarjetas y packaging.'),
        ],
        'filas_arriba': [
            [('img', 'portada.webp', 'Logotipo de Golden Hour sobre la foto de unos anillos')],
            [('img', 'collar.webp', 'Una mujer con un collar de cadena dorada y un top blanco'),
             ('img', 'anillos.webp', 'Manos con anillos dorados sobre una camisa de seda')],
        ],
        'filas_abajo': [
            [('img', 'paleta.webp', 'Paleta de Golden Hour: chocolate, canela, miel, choco blanco y choco leche'),
             ('img', 'logo.webp', 'Logotipo de Golden Hour, joyería de autor')],
            [('img', 'cadena.webp', 'Una cadena dorada con gotas de agua'),
             ('img', 'espalda.webp', 'Una mujer de espaldas con un collar fino')],
            [('img', 'sobre.webp', 'Sobre y tarjeta de Golden Hour con el patrón de puntos'),
             ('img', 'tarjetas.webp', 'Tarjetas de Golden Hour sobre platos rosas con flores')],
            [('img', 'vaso.webp', 'Vaso de café con el patrón de líneas de Golden Hour junto a una laptop'),
             ('img', 'aros.webp', 'Un aro dorado largo junto a una cadena')],
            [('img', 'patron.webp', 'Patrón de puntos de Golden Hour')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': 'brunch-club',
    },
    {
        'slug': 'brunch-club',
        'nombre': 'Brunch Club Café',
        'bajada': 'Identidad visual para un café de brunch',
        'titulo_seo': 'Brunch Club Café, identidad visual para un café de brunch · LIS',
        'descripcion': 'Identidad visual para Brunch Club Café, un café de brunch, comida sana, buen café y perros bienvenidos: un imagotipo con un limón, un perro que toma café y patrones en lima, gris y crema.',
        'resumen': 'LIS. Creative Studio diseñó la identidad visual de Brunch Club Café, un café de brunch, comida sana, buen café, jugos verdes y buena música, donde los perros son bienvenidos. El sistema combina un logotipo de serif con cursiva, un imagotipo con un limón, un personaje de perro que toma café, una paleta de lima, negro, grises y verde oliva y patrones para el packaging y el merch.',
        'servicio': 'Identidad visual',
        'intro': [
            'Brunch Club Café es un café de brunch, comida sana y buen café, con jugos verdes, buena música y un detalle que lo define: los perros son bienvenidos. Necesitaba una marca fresca y con humor, que se viera tan bien en el vaso como en las redes.',
            'Diseñamos un logotipo que combina una serif clásica con una cursiva, un imagotipo con un limón y un perro que toma café que se convirtió en el personaje de la marca, y lo llevamos a patrones, vasos, bolsas y gorras.',
        ],
        'ficha': [
            ('Rubro', 'Café de brunch'),
            ('Alcance', 'Identidad visual, manual de marca, patrones y aplicaciones'),
        ],
        'web': None,
        'cliente_org': {'name': 'Brunch Club Café'},
        'columnas': [
            ('El desafío', 'Un café de brunch con mucha competencia alrededor, que necesitaba diferenciarse con una personalidad propia y no solo con fotos lindas de platos.'),
            ('La idea', 'El perro que toma café como personaje, porque el lugar es dog friendly, y un limón que habla de lo fresco y lo sano en cada pieza.'),
            ('El sistema', 'Scotch Display para los títulos y Helvetica para los textos, un lima que resalta sobre negro y verde oliva, y tres patrones con el perro, la cafetera y las medialunas.'),
        ],
        'filas_arriba': [
            [('img', 'portada.webp', 'Logo de Brunch Club Café en blanco sobre la foto de una barra con teteras')],
            [('img', 'logo.webp', 'Logotipo e isotipo de Brunch Club Café con el limón'),
             ('img', 'frases.webp', 'Frases de Brunch Club Café en verde oliva y gris: brunch, healthy food, great coffee')],
        ],
        'filas_abajo': [
            [('img', 'colores.webp', 'Paleta de Brunch Club Café: lima, negro, grises y verde oliva'),
             ('img', 'tipografia.webp', 'Tipografía Scotch Display de Brunch Club Café')],
            [('img', 'patron-perro.webp', 'Patrón del perro que toma café de Brunch Club Café'),
             ('img', 'patron-lima.webp', 'Patrón lima con cafeteras y medialunas de Brunch Club Café'),
             ('img', 'patron-oscuro.webp', 'Patrón gris con cafeteras y medialunas de Brunch Club Café')],
            [('img', 'aplicaciones.webp', 'Vaso negro y bolsa lima de Brunch Club Café'),
             ('video', 'gorra.mp4', 'gorra.jpg', 'Gorra negra con el logo de Brunch Club Café')],
        ],
        'portada_og': 'og.jpg',
        'tarjeta': 'card.webp',
        'siguiente': None,
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
