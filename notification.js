document.addEventListener('DOMContentLoaded', () => {
  const bell = document.querySelector('.bell');
  const notificationBox = document.querySelector('.notification-box');

  if (bell && notificationBox) {
    bell.addEventListener('click', () => {
      // Toggle notification visibility
      notificationBox.classList.toggle('show');

      // Auto-hide after 5 seconds
      if (notificationBox.classList.contains('show')) {
        setTimeout(() => {
          notificationBox.classList.remove('show');
        }, 5000);
      }
    });
  }
});
