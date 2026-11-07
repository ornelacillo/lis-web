// Tienda de LIS: crea el pago en pesos en Mercado Pago (Checkout Pro) y manda a la persona a pagar.
// Al aprobarse el pago, Mercado Pago la devuelve sola a la página de gracias con la descarga.
// Mismo circuito que Peque (api/comprar.js). La credencial va en Vercel como MP_ACCESS_TOKEN.
// Uso: /api/comprar-tienda?p=kit-contratos · /api/comprar-tienda?p=masterclass-ia
const SITIO = "https://liscreativestudio.com";

const PRODUCTOS = {
  "kit-contratos": {
    title: "Kit de contratos para diseñadoras · LIS. Creative Studio",
    unit_price: 14900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=kit-contratos",
  },
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
  // Masterclass 01 en vivo, jueves 3/12/2026 a las 10 h (Argentina). Preventa.
  "masterclass-ia": {
    title: "Masterclass Así usamos la IA en LIS · 3 de diciembre · LIS. Creative Studio",
    unit_price: 39900,
    gracias: "/masterclass-ia-reserva-3f9a1c7e2b",
    volver: "/tienda#masterclases",
  },
};

export default async function handler(req, res) {
  const redirect = (url) => { res.writeHead(302, { Location: url, "Cache-Control": "no-store" }); res.end(); };
  const id = new URL(req.url, SITIO).searchParams.get("p");
  const prod = PRODUCTOS[id];
  const respaldo = `mailto:hello@liscreativestudio.com?subject=${encodeURIComponent("Quiero comprar: " + (prod ? prod.title : "un producto de la tienda"))}`;
  if (!prod) return redirect(`${SITIO}/tienda`);
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
