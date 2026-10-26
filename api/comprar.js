// Peque Studio: crea el pago del kit Mi día en Mercado Pago (Checkout Pro) y manda a la persona a pagar.
// Después de pagar, Mercado Pago la devuelve sola a la página de gracias con la descarga.
// La credencial va en Vercel como variable de entorno MP_ACCESS_TOKEN (nunca en el código).
const LINK_DE_RESPALDO = "https://mpago.la/2bwgKHi"; // si algo falla, se usa el link de pago simple
const SITIO = "https://peque.liscreativestudio.com";

export default async function handler(req, res) {
  const token = process.env.MP_ACCESS_TOKEN;
  const redirect = (url) => { res.writeHead(302, { Location: url, "Cache-Control": "no-store" }); res.end(); };
  if (!token) return redirect(LINK_DE_RESPALDO);

  try {
    const r = await fetch("https://api.mercadopago.com/checkout/preferences", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        items: [{
          id: "kit-mi-dia",
          title: "Mi día · Tarjetas de rutina ilustradas (con nena y con nene + 4 bonus)",
          quantity: 1,
          unit_price: 10999,
          currency_id: "ARS",
        }],
        back_urls: {
          success: `${SITIO}/gracias-7f9aa2246d`,
          pending: `${SITIO}/#precio`,
          failure: `${SITIO}/#precio`,
        },
        auto_return: "approved",
        // Sin pagos en efectivo (Rapipago, Pago Fácil): así la descarga es siempre inmediata
        payment_methods: { excluded_payment_types: [{ id: "ticket" }, { id: "atm" }] },
        statement_descriptor: "PEQUE STUDIO",
      }),
    });
    const data = await r.json();
    if (!r.ok || !data.init_point) throw new Error(JSON.stringify(data).slice(0, 300));
    return redirect(data.init_point);
  } catch (err) {
    console.error("Mercado Pago:", err);
    return redirect(LINK_DE_RESPALDO);
  }
}
