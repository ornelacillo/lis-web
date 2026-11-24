// Tienda de LIS: crea el pago en pesos en Mercado Pago (Checkout Pro) y manda a la persona a pagar.
// Al aprobarse el pago, Mercado Pago la devuelve sola a la página de gracias con la descarga.
// Mismo circuito que Peque (api/comprar.js). La credencial va en Vercel como MP_ACCESS_TOKEN.
// Uso: /api/comprar-tienda?p=sistema (o el id de cada plantilla)
const SITIO = "https://liscreativestudio.com";

const PRODUCTOS = {
  // Kit de contratos: dado de baja el 12/11/2026 (el contrato está dentro del Kit de bienvenida). La entrega para quien ya lo compró sigue en tienda-gracias.
  // Plantillas para Canva (7/11/2026): la entrega son los enlaces de plantilla, en tienda-gracias y en un PDF
  "kit-bienvenida": {
    title: "Kit de bienvenida · plantillas para Canva · LIS. Creative Studio",
    unit_price: 24900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=kit-bienvenida",
    volver: "/tienda#plantillas",
  },
  "propuesta": {
    title: "Propuesta comercial · plantillas para Canva · LIS. Creative Studio",
    unit_price: 14900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=propuesta",
    volver: "/tienda#plantillas",
  },
  "conceptboards": {
    title: "Conceptboards · plantillas para Canva · LIS. Creative Studio",
    unit_price: 14900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=conceptboards",
    volver: "/tienda#plantillas",
  },
  "entrega-identidad": {
    title: "Entrega de identidad · plantillas para Canva · LIS. Creative Studio",
    unit_price: 14900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=entrega-identidad",
    volver: "/tienda#plantillas",
  },
  "manual-de-marca": {
    title: "Manual de marca · plantillas para Canva · LIS. Creative Studio",
    unit_price: 29900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=manual-de-marca",
    volver: "/tienda#plantillas",
  },
  "entrega-web": {
    title: "Entrega de web · plantillas para Canva · LIS. Creative Studio",
    unit_price: 14900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=entrega-web",
    volver: "/tienda#plantillas",
  },
  // Producto de entrada (17/11/2026): la plantilla de presupuesto y recibo sola, para la primera compra.
  "presupuesto": {
    title: "Presupuesto y recibo · plantilla para Canva · LIS. Creative Studio",
    unit_price: 3900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=presupuesto",
    volver: "/tienda#presupuesto",
  },
  "firmas": {
    title: "Generador de firmas de mail · LIS. Creative Studio",
    unit_price: 7900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=firmas",
    volver: "/tienda#plantillas",
  },
  "sistema": {
    title: "Sistema de freelance a estudio · plantillas para Canva · LIS. Creative Studio",
    unit_price: 49900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=sistema",
    volver: "/tienda#plantillas",
  },
  // Oferta de retargeting (13/11/2026): el Sistema a mitad de precio, SOLO desde el anuncio de Meta a quien ya visitó la tienda.
  // El link va directo a Mercado Pago (no pasa por /tienda) y deja de andar el 30/11/2026: después manda a /tienda.
  "sistema-vuelve": {
    title: "Sistema de freelance a estudio · 50% off · LIS. Creative Studio",
    unit_price: 24900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=sistema&v=24900",
    volver: "/tienda#plantillas",
    hasta: "2026-12-01T03:00:00Z",
  },
  // Masterclass 01: en pausa desde el 11/11/2026 (vuelve en 2027). Sin producto, el link viejo lleva a /tienda.
};

// Black Friday 2026: 30% en toda la tienda del jueves 26/11 a las 00:00 al lunes 30/11 a las 23:59 (hora de Argentina).
// Solo desde el link que Orne manda por DM (/tienda?bf), que cambia los botones a estos ids (<id>-bf).
// Fuera de esas fechas el link lleva a la tienda con el precio de siempre.
const BF = { desde: "2026-11-26T03:00:00Z", hasta: "2026-12-01T03:00:00Z" };
const BF_PRECIOS = {
  "sistema": 34900, "kit-bienvenida": 17400, "propuesta": 10400, "conceptboards": 10400,
  "entrega-identidad": 10400, "manual-de-marca": 20900, "entrega-web": 10400, "presupuesto": 2700, "firmas": 5500,
};
for (const [id, precio] of Object.entries(BF_PRECIOS)) {
  const base = PRODUCTOS[id];
  PRODUCTOS[`${id}-bf`] = {
    title: base.title.replace(" · LIS. Creative Studio", " · Black Friday 30% off · LIS. Creative Studio"),
    unit_price: precio,
    gracias: `/tienda-gracias-8e4c5f5d4f?p=${id}&v=${precio}`,
    volver: base.volver,
    desde: BF.desde,
    hasta: BF.hasta,
  };
}

export default async function handler(req, res) {
  const redirect = (url) => { res.writeHead(302, { Location: url, "Cache-Control": "no-store" }); res.end(); };
  const id = new URL(req.url, SITIO).searchParams.get("p");
  const prod = PRODUCTOS[id];
  const respaldo = `mailto:hello@liscreativestudio.com?subject=${encodeURIComponent("Quiero comprar: " + (prod ? prod.title : "un producto de la tienda"))}`;
  if (!prod) return redirect(`${SITIO}/tienda`);
  if (prod.hasta && Date.now() > Date.parse(prod.hasta)) return redirect(`${SITIO}/tienda#plantillas`);
  if (prod.desde && Date.now() < Date.parse(prod.desde)) return redirect(`${SITIO}/tienda#plantillas`);
  const token = process.env.MP_ACCESS_TOKEN;
  if (!token) return redirect(respaldo);

  try {
    const r = await fetch("https://api.mercadopago.com/checkout/preferences", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        items: [{ id, title: prod.title, quantity: 1, unit_price: prod.unit_price, currency_id: "ARS" }],
        back_urls: {
          success: `${SITIO}${prod.gracias}`,
          pending: `${SITIO}${prod.volver || "/tienda#plantillas"}`,
          failure: `${SITIO}${prod.volver || "/tienda#plantillas"}`,
        },
        auto_return: "approved",
        // Sin efectivo (Rapipago, Pago Fácil): así la descarga o la reserva es siempre inmediata
        payment_methods: { excluded_payment_types: [{ id: "ticket" }, { id: "atm" }] },
        statement_descriptor: "LIS STUDIO",
        // Para el mail automático: Mercado Pago avisa a api/mp-webhook.js y ahí se sabe qué producto fue
        external_reference: id,
        notification_url: `${SITIO}/api/mp-webhook?source_news=webhooks`,
      }),
    });
    const data = await r.json();
    if (!r.ok || !data.init_point) throw new Error(JSON.stringify(data).slice(0, 300));
    return redirect(data.init_point);
  } catch (err) {
    console.error("Mercado Pago (tienda):", err);
    return redirect(respaldo);
  }
}
