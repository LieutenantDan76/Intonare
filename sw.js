// Intonare Service Worker
// Strategy: cache-first, update in background
// Bump CACHE_NAME version any time you deploy a major update

const CACHE_NAME = 'intonare-v1';

// Files to precache on install
const PRECACHE = [
  './',
  './Intonare.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
];

// ── Install: precache core assets ──────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting()) // activate immediately, don't wait for old SW to die
  );
});

// ── Activate: delete old caches ────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim()) // take control of all open tabs immediately
  );
});

// ── Fetch: serve from cache, update in background ──────────────
self.addEventListener('fetch', event => {
  // Only handle GET requests; skip non-http(s) (e.g. chrome-extension)
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith('http')) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(cache =>
      cache.match(event.request).then(cached => {
        // Kick off a network fetch regardless — update cache in background
        const networkFetch = fetch(event.request)
          .then(response => {
            if (response && response.ok) {
              cache.put(event.request, response.clone());
            }
            return response;
          })
          .catch(() => null);

        // Return cached version immediately if available, otherwise wait for network
        return cached || networkFetch;
      })
    )
  );
});
