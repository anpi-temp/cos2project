self.addEventListener('fetch', function(event) {
  // リクエストにそのまま応答（最低限の fetch ハンドラ）
  event.respondWith(fetch(event.request));
});