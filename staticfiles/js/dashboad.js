document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const tabMenu = document.getElementById('tabMenu');
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
 
    // モバイルメニューのトグル
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            const icon = this.querySelector('.menu-icon');
            tabMenu.querySelector('.tabs').classList.toggle('active');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });
    }
 
    // タブ切り替え機能
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.dataset.tab;
 
            // アクティブなタブの更新
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
 
            // コンテンツの切り替え
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });
        });
    });
 });