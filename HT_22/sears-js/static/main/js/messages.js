function closeMessage(element) {
    element.parentElement.style.display = 'none';
}

setTimeout(function () {
    var notification = document.getElementById('jq-notification');
    if (notification) {
        notification.style.display = 'none';
    }
}, 5000);
