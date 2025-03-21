document.addEventListener('DOMContentLoaded', function() {
    const unreadMessagesList = document.getElementById('unread-messages');
    const unreadCountElement = document.querySelector('.unread-badge');
    const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]')?.value;

    unreadMessagesList.addEventListener('click', function(event) {
        if (event.target.classList.contains('mark-read-btn')) {
            const messageId = event.target.dataset.messageId;
            const messageCard = event.target.closest('.message-card');

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

                    // 未読カウントを更新
                    updateUnreadCount();
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    function updateUnreadCount() {
        if (unreadCountElement) {
            const currentCount = unreadMessagesList.querySelectorAll('.message-card').length;
            unreadCountElement.textContent = currentCount;
            unreadCountElement.style.display = currentCount > 0 ? 'inline' : 'none';
            
            // 未読メッセージがない場合のメッセージ表示
            if (currentCount === 0) {
                const emptyMessage = document.createElement('p');
                emptyMessage.textContent = '未読メッセージはありません。';
                unreadMessagesList.appendChild(emptyMessage);
            }
        }
    }
});