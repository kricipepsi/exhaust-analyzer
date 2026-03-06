/**
 * Service Worker for 5-Gas Exhaust Analyzer PWA
 * Caches static assets and provides offline support
 */

const CACHE_NAME = 'exhaust-analyzer-v1';
const STATIC_CACHE = 'exhaust-analyzer-static-v1';

// Assets to cache immediately on install
const STATIC_ASSETS = [
  '/',
  '/static/style.css',
  '/static/manifest.json',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4889634886203423'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== STATIC_CACHE && cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event - network first, fallback to cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // For same-origin requests (our app), use network-first
  if (url.origin === location.origin) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // If successful, cache the response for future use
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Network failed, try cache
          return caches.match(request);
        })
    );
  } else {
    // For cross-origin (CDNs, ads), use cache-first with network fallback
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(request).then((response) => {
            // Cache successful CDN responses
            if (response.status === 200) {
              const responseClone = response.clone();
              caches.open(STATIC_CACHE).then((cache) => {
                cache.put(request, responseClone);
              });
            }
            return response;
          });
        })
    );
  }
});