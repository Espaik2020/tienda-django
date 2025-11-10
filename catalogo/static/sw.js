// --- DNM Wear Service Worker ---
const VERSION = 'v1.3';
const STATIC_CACHE = `dnmwear-static-${VERSION}`;

// Ajusta "/" si tu home real es otro (p.ej. "/inicio/")
const OFFLINE_PAGE = '/'; // o '/offline.html' si creas una página offline dedicada

// Precache de estáticos propios (mismo origen)
// OJO: rutas absolutas porque el SW no puede usar tags de Django.
const PRECACHE_URLS = [
  '/',                        // portada para fallback de navegación
  '/static/css/app.css',
  '/static/js/app.js',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  // Si quieres, agrega otros propios (img/logo.png, etc.)
  // '/static/img/logo.png',
];

// (Opcional) externos de CDN que uses mucho. No pasa nada si alguno falla.
// Nota: se almacenan como 'opaque' en algunos casos, pero sirven para cache offline.
const CDN_URLS = [
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css',
  'https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js',
  // Las hojas de Google Fonts también pueden ir aquí si quieres precachearlas:
  // 'https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Outfit:wght@300;400;600;800&display=swap'
];

// Utilidad
const isSameOrigin = (url) => self.location.origin === new URL(url, self.location).origin;

self.addEventListener('install', (event) => {
  self.skipWaiting(); // que el nuevo SW pueda activarse sin esperar
  event.waitUntil(
    caches.open(STATIC_CACHE).then(async (cache) => {
      try {
        await cache.addAll(PRECACHE_URLS);
      } catch (e) {
        // Ignora fallos individuales para que la instalación no se aborte
        console.warn('[SW] Precaching parcial:', e);
      }
      // Intenta precache de algunos CDN (best-effort)
      try {
        await cache.addAll(CDN_URLS);
      } catch (_) {}
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      // Limpia versiones antiguas
      const keys = await caches.keys();
      await Promise.all(keys.filter(k => k !== STATIC_CACHE).map(k => caches.delete(k)));
      await self.clients.claim();
    })()
  );
});

// Mensaje opcional para saltar a la nueva versión desde la app
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Solo GET
  if (request.method !== 'GET') return;

  // 1) Navegación HTML: estrategia network-first con fallback
  if (request.mode === 'navigate' || (request.headers.get('accept') || '').includes('text/html')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // 2) Estáticos mismo origen (/static/*): cache-first
  if (isSameOrigin(request.url) && new URL(request.url).pathname.startsWith('/static/')) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // 3) Resto (incluye CDNs): try cache, then network (cache-first "suave")
  event.respondWith(cacheFirst(request));
});

// --- Estrategias ---
async function networkFirst(request) {
  const cache = await caches.open(STATIC_CACHE);
  try {
    const fresh = await fetch(request);
    // Guarda copia si es mismo origen (para no llenar con todo internet)
    if (isSameOrigin(request.url)) cache.put(request, fresh.clone());
    return fresh;
  } catch (err) {
    // Fallback a caché o a OFFLINE_PAGE
    const cached = await caches.match(request);
    if (cached) return cached;
    return caches.match(OFFLINE_PAGE);
  }
}

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const resp = await fetch(request);
    // Cachea respuesta si se puede
    const cache = await caches.open(STATIC_CACHE);
    cache.put(request, resp.clone());
    return resp;
  } catch (err) {
    // último recurso: si pedían un icono, intenta el 192
    const url = new URL(request.url);
    if (url.pathname.endsWith('.png') || url.pathname.endsWith('.ico')) {
      const fallbackIcon = await caches.match('/static/icons/icon-192.png');
      if (fallbackIcon) return fallbackIcon;
    }
    throw err;
  }
}
