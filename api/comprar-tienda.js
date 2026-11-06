// Tienda de LIS: crea el pago en pesos en Mercado Pago (Checkout Pro) y manda a la persona a pagar.
// Al aprobarse el pago, Mercado Pago la devuelve sola a la página de gracias con la descarga.
// Mismo circuito que Peque (api/comprar.js). La credencial va en Vercel como MP_ACCESS_TOKEN.
// Uso: /api/comprar-tienda?p=kit-contratos
const SITIO = "https://liscreativestudio.com";

const PRODUCTOS = {
  "kit-contratos": {
    title: "Kit de contratos para diseñadoras · LIS. Creative Studio",
    unit_price: 14900,
    gracias: "/tienda-gracias-8e4c5f5d4f?p=kit-contratos",
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
          pending: `${SITIO}/tienda#plantillas`,
          failure: `${SITIO}/tienda#plantillas`,
        },
        auto_return: "approved",
        // Sin efectivo (Rapipago, Pago Fácil): así la descarga es siempre inmediata
        payment_methods: { excluded_payment_types: [{ id: "ticket" }, { id: "atm" }] },
        statement_descriptor: "LIS STUDIO",
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
