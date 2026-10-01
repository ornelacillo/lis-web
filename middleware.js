// Peque Studio: el subdominio peque.liscreativestudio.com muestra la landing de /peque
export const config = { matcher: "/:path*" };

export default function middleware(request) {
  const url = new URL(request.url);
  if (url.hostname === "peque.liscreativestudio.com" && !url.pathname.startsWith("/peque")) {
    const dest = new URL(url.pathname === "/" ? "/peque" : "/peque" + url.pathname + url.search, url);
    return new Response(null, { headers: { "x-middleware-rewrite": dest.toString() } });
  }
  return new Response(null, { headers: { "x-middleware-next": "1" } });
}
