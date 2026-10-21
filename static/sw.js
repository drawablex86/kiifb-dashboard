/*
 * sw.js — service-worker kill switch (T103 maintenance).
 *
 * This project ships no service worker. If a stale SW registration was
 * ever created for this origin (e.g. by a prior local server or another
 * project that served /sw.js on the same port), the browser re-checks
 * /sw.js on navigation and spams 404s against this dev server.
 *
 * This file deliberately REPLACES that stale worker: the browser installs
 * it once, it activates and immediately unregisters itself — dropping the
 * stale registration and ending the 404 cycle for good.
 */

self.addEventListener('install', function () {
	self.skipWaiting();
});

self.addEventListener('activate', function (event) {
	event.waitUntil(
		self.registration.unregister().then(function () {
			return self.clients.matchAll();
		}).then(function (clients) {
			clients.forEach(function (client) {
				client.navigate(client.url);
			});
		})
	);
});
