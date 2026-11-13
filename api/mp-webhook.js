// Aviso de Mercado Pago (7/11/2026): cuando se aprueba un pago de la tienda, suma a quien compró
// al grupo "Compró en la tienda" de MailerLite con el campo "entrega" = el link a SU página de entrega.
// Una sola automatización (entra al grupo → mail con el botón a {$entrega}) sirve para todos los productos,
// porque el plan de MailerLite no da para una por producto.
// Mercado Pago llama acá porque api/comprar-tienda.js pone notification_url. Variables en Vercel:
// MP_ACCESS_TOKEN (ya estaba) y MAILERLITE_API_KEY.
// Seguridad: no se confía en lo que llega en el aviso; con el id se pide el pago a Mercado Pago
// y solo se actúa si está aprobado y es de un producto de la tienda.
const SITIO = "https://liscreativestudio.com";
const ENTREGAS = {
  "kit-bienvenida": "/tienda-gracias-8e4c5f5d4f?p=kit-bienvenida",
  "propuesta": "/tienda-gracias-8e4c5f5d4f?p=propuesta",
  "conceptboards": "/tienda-gracias-8e4c5f5d4f?p=conceptboards",
  "entrega-identidad": "/tienda-gracias-8e4c5f5d4f?p=entrega-identidad",
  "manual-de-marca": "/tienda-gracias-8e4c5f5d4f?p=manual-de-marca",
  "entrega-web": "/tienda-gracias-8e4c5f5d4f?p=entrega-web",
  "firmas": "/tienda-gracias-8e4c5f5d4f?p=firmas",
  "sistema": "/tienda-gracias-8e4c5f5d4f?p=sistema",
  "sistema-vuelve": "/tienda-gracias-8e4c5f5d4f?p=sistema",
  "masterclass-ia": "/masterclass-ia-reserva-3f9a1c7e2b",
};
const NOMBRES = {
  "kit-bienvenida": "Kit de bienvenida", "propuesta": "Propuesta comercial", "conceptboards": "Conceptboards",
  "entrega-identidad": "Entrega de identidad", "manual-de-marca": "Manual de marca", "entrega-web": "Entrega de web",
  "firmas": "Firmas de mail", "sistema": "Sistema de freelance a estudio", "sistema-vuelve": "Sistema de freelance a estudio", "masterclass-ia": "Masterclass Así usamos la IA en LIS",
};
const GRUPO = "Compró en la tienda";
const ML = "https://connect.mailerlite.com/api";

async function ml(path, opts = {}) {
  const r = await fetch(ML + path, {
    ...opts,
    headers: { Authorization: `Bearer ${process.env.MAILERLITE_API_KEY}`, "Content-Type": "application/json", Accept: "application/json", ...(opts.headers || {}) },
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`MailerLite ${path} ${r.status} ${JSON.stringify(data).slice(0, 200)}`);
  return data;
}

async function grupoId(nombre) {
  const d = await ml(`/groups?limit=100&filter[name]=${encodeURIComponent(nombre)}`);
  const g = (d.data || []).find((x) => x.name === nombre);
  if (!g) throw new Error(`No existe el grupo "${nombre}" en MailerLite`);
  return g.id;
}

export default async function handler(req, res) {
  const ok = () => { res.statusCode = 200; res.end("ok"); };
  try {
    const url = new URL(req.url, "https://liscreativestudio.com");
    // Chequeo de configuración (no muestra ninguna clave): /api/mp-webhook?check=1
    if (url.searchParams.get("check") === "1") {
      const estado = { mercadopago: !!process.env.MP_ACCESS_TOKEN, mailerlite: !!process.env.MAILERLITE_API_KEY, grupo: false };
      try { estado.grupo = !!(await grupoId(GRUPO)); } catch (e) { estado.error = e.message; }
      res.setHeader("Content-Type", "application/json"); res.statusCode = 200; res.end(JSON.stringify(estado)); return;
    }
    let body = req.body;
    if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
    body = body || {};
    const tipo = body.type || body.topic || url.searchParams.get("type") || url.searchParams.get("topic");
    const id = (body.data && body.data.id) || url.searchParams.get("data.id") || (tipo === "payment" ? url.searchParams.get("id") : null);
    if (tipo !== "payment" || !id) return ok();

    const r = await fetch(`https://api.mercadopago.com/v1/payments/${encodeURIComponent(id)}`, {
      headers: { Authorization: `Bearer ${process.env.MP_ACCESS_TOKEN}` },
    });
    const pago = await r.json();
    if (!r.ok) throw new Error("Mercado Pago " + r.status);
    const producto = pago.external_reference || (pago.additional_info && pago.additional_info.items && pago.additional_info.items[0] && pago.additional_info.items[0].id);
    const email = pago.payer && pago.payer.email;
    if (pago.status !== "approved" || !ENTREGAS[producto] || !email) return ok();

    const nombre = (pago.payer.first_name || (pago.additional_info && pago.additional_info.payer && pago.additional_info.payer.first_name) || "").trim();
    const gid = await grupoId(GRUPO);
    const campos = { entrega: SITIO + ENTREGAS[producto], producto: NOMBRES[producto] };
    if (nombre) campos.name = nombre;
    // Si ya había comprado antes, sale y vuelve a entrar al grupo para que la automatización la tome de nuevo
    const sub = await ml("/subscribers", { method: "POST", body: JSON.stringify({ email, fields: campos }) });
    const sid = sub.data && sub.data.id;
    if (sid) {
      await fetch(`${ML}/subscribers/${sid}/groups/${gid}`, { method: "DELETE", headers: { Authorization: `Bearer ${process.env.MAILERLITE_API_KEY}` } }).catch(() => {});
      await ml(`/subscribers/${sid}/groups/${gid}`, { method: "POST" });
    }
    console.log("Compra entregada:", producto, pago.id);
    return ok();
  } catch (err) {
    console.error("mp-webhook:", err.message);
    res.statusCode = 500; res.end("error: " + err.message); // Mercado Pago reintenta más tarde
  }
}
