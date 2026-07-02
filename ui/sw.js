const CACHE_NAME = 'krishi-sampark-cache-v1';
const ASSETS_TO_CACHE = [
  '/agui/index.html',
  '/agui/styles.css',
  '/agui/dashboard.js',
  '/agui/panel_router.js',
  '/agui/camera.js',
  '/agui/local_models.js',
  '/agui/local_db.js',
  '/a2ui/index.html',
  '/a2ui/styles.css',
  '/a2ui/app.js',
  '/manifest.webmanifest',
  'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap'
];

// Install Event - cache core static resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Pre-caching static assets');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate Event - clean up obsolete cache keys
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - handle offline resource fetching
self.addEventListener('fetch', event => {
  const requestUrl = new URL(event.request.url);

  // Bypass cache for dynamic API endpoints and SSE stream
  if (requestUrl.pathname.startsWith('/api/') || requestUrl.pathname.startsWith('/run_sse') || requestUrl.pathname.startsWith('/feedback')) {
    event.respondWith(
      fetch(event.request)
        .catch(err => {
          console.warn('[Service Worker] Network request failed, returning offline status:', err);
          // Return custom offline JSON response for profile GET requests
          if (event.request.method === 'GET' && requestUrl.pathname.startsWith('/api/profile/')) {
            return new Response(JSON.stringify({
              offline: true,
              message: "Device offline. Data retrieved from local IndexedDB twin."
            }), {
              headers: { 'Content-Type': 'application/json' }
            });
          }
          // Return generic error for POST requests
          return new Response(JSON.stringify({
            status: "offline_queued",
            message: "Offline. Action has been queued for synchronization."
          }), {
            headers: { 'Content-Type': 'application/json' }
          });
        })
    );
    return;
  }

  // Cache-First (with Network Fallback) for static resources
  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          // Fetch updated version in the background to keep cache fresh
          fetch(event.request)
            .then(networkResponse => {
              if (networkResponse.status === 200) {
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, networkResponse));
              }
            })
            .catch(() => {}); // ignore offline background fetch failures
          return cachedResponse;
        }

        // Return from network if not in cache
        return fetch(event.request).then(response => {
          // Do not cache non-200 or non-http responses (e.g. chrome extensions)
          if (!response || response.status !== 200 || !event.request.url.startsWith('http')) {
            return response;
          }
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseToCache));
          return response;
        }).catch(err => {
          console.warn('[Service Worker] Fetch failed:', event.request.url, err);
          if (requestUrl.pathname.startsWith('/schemas/')) {
            return new Response(JSON.stringify({
              type: "card",
              title: "Offline Fallback",
              components: [{ type: "text", value: "This content is currently unavailable offline." }]
            }), {
              headers: { 'Content-Type': 'application/json' }
            });
          }
          return new Response("Network error", { status: 480, statusText: "Offline" });
        });
      })
  );
});
