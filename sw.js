// Intonare Service Worker
// Strategy: cache-first, update in background
// Bump CACHE_NAME version any time you deploy a major update

const CACHE_NAME = 'intonare-v2';   // bumped: v1 never installed, see precache() below

// Files to precache on install
const PRECACHE = [
  './',
  './Intonare.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
];

// cache.addAll() is ALL OR NOTHING. One entry that 404s rejects the whole
// promise, install fails, and the service worker never activates — so the app
// has no offline cache at all and nothing anywhere says why. That is exactly
// what happened: icon-192.png and icon-512.png were listed here and had never
// been added to the repo, so every install since this file was written has
// failed silently.
//
// The icons exist now. This adds the belt as well as the braces: each entry is
// fetched on its own, and one missing file costs that file rather than the
// entire cache.
async function precache(cache) {
  const missing = [];
  await Promise.all(PRECACHE.map(async (url) => {
    try {
      const res = await fetch(url, { cache: 'reload' });
      if (!res.ok) { missing.push(url + ' -> HTTP ' + res.status); return; }
      await cache.put(url, res);
    } catch (e) {
      missing.push(url + ' -> ' + e);
    }
  }));
  if (missing.length) console.warn('[sw] precache incomplete:', missing);
}

// ── Install: precache core assets ──────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => precache(cache))
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
