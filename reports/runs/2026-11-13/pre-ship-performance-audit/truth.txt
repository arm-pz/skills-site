Planted slow-downs in fixtures/slow-app (6):
1. hero.png is a ~6 MB uncompressed 1800x1200 PNG shown at page width, no width/height, no responsive sizes, not lazy, no modern format.
2. app.js (~400 KB, unminified) loads synchronously in <head> (render-blocking) and busy-waits ~450 ms on the main thread.
3. Google Fonts stylesheet requests 9 weights with display=block (render-blocking, invisible text).
4. Cache-Control: no-store on every static asset; no compression (gzip/brotli).
5. /api/stats runs 31 sequential queries (N+1, ~930 ms); should be one grouped query.
6. Stats are fetched client-side after load, so the number appears late (layout shift risk with the unsized image).
