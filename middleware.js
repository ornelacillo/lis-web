// Peque Studio se dio de baja el 19/11/2026: el subdominio peque.liscreativestudio.com manda a la portada de LIS
export const config = { matcher: "/:path*" };

export default function middleware(request) {
  const url = new URL(request.url);
  if (url.hostname === "peque.liscreativestudio.com") {
    return Response.redirect("https://liscreativestudio.com/", 301);
  }
  return new Response(null, { headers: { "x-middleware-next": "1" } });
}
