document.addEventListener('DOMContentLoaded', function() {
    const messageList = document.querySelector('.message-list');
    const unreadCountElement = document.querySelector('.unread-badge');
    const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]')?.value;  // オプショナルチェイニング

    messageList.addEventListener('click', function(event) {
        if (event.target.classList.contains('mark-read-btn')) {
            const messageId = event.target.dataset.messageId;
            const messageCard = event.target.closest('.message-card');

            // CSRF トークンが存在するか確認
            if (!csrftoken) {
                console.error('CSRF token not found.');
                return;
            }

            fetch(`/api/admin-messages/${messageId}/mark_as_read/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'message marked as read') {
                    // メッセージカードを削除
                    messageCard.remove();

                    // 未読カウントを減らす
                    if (unreadCountElement) {
                        let unreadCount = parseInt(unreadCountElement.textContent);
                        if (unreadCount > 0) {
                            unreadCount--;
                            unreadCountElement.textContent = unreadCount;
                        }
                        // 未読数が0になったら非表示にする
                        if (unreadCount <= 0) {
                            unreadCountElement.style.display = 'none';
                        }
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });
});