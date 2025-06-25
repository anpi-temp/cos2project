document.addEventListener('DOMContentLoaded', () => {
    console.log("Base JavaScript loaded!");
 });


document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".dropdown-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const parent = btn.closest(".dropdown");
      parent.classList.toggle("open");
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const mediaQuery = window.matchMedia("(max-width: 600px)");

  function setupDropdowns(isMobile) {
    const toggles = document.querySelectorAll(".submenu-toggle");

    toggles.forEach(toggle => {
      // 一度イベントを削除してから再追加（画面サイズ切替に対応）
      const newToggle = toggle.cloneNode(true);
      toggle.parentNode.replaceChild(newToggle, toggle);
    });

    if (isMobile) {
      document.querySelectorAll(".submenu-toggle").forEach(toggle => {
        toggle.addEventListener("click", function (e) {
          e.preventDefault(); // ← aタグだけど遷移させない

          const submenu = this.nextElementSibling;
          if (!submenu) return;

          const isOpen = submenu.classList.contains("open");

          // 他を閉じる
          document.querySelectorAll(".submenu-panel.open").forEach(panel => {
            panel.classList.remove("open");
            panel.style.maxHeight = null;
          });

          if (!isOpen) {
            submenu.classList.add("open");
            submenu.style.maxHeight = submenu.scrollHeight + "px";
          }
        });
      });
    } else {
      // PCでは max-height を解除（hoverに任せる）
      document.querySelectorAll(".submenu-panel").forEach(panel => {
        panel.classList.remove("open");
        panel.style.maxHeight = null;
      });
    }
  }

  const mq = window.matchMedia("(max-width: 600px)");
  setupDropdowns(mq.matches);
  mq.addEventListener("change", e => setupDropdowns(e.matches));
});
