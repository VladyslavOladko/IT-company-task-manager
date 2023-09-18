function changeButtonClass(button) {
    var taskId = button.getAttribute('data-task-id');

    if (button.classList.contains('btn-secondary')) {
        button.classList.remove('btn-secondary');
        button.classList.add('btn-warning');
        button.innerText = 'Need Help!';

        localStorage.setItem('buttonState_' + taskId, 'clicked');
    } else {
        button.classList.remove('btn-warning');
        button.classList.add('btn-secondary');
        button.innerText = 'If you need help click here';

        localStorage.setItem('buttonState_' + taskId, 'not_clicked');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.color-change-button');
    buttons.forEach(function(button) {
        var taskId = button.getAttribute('data-task-id');
        var buttonState = localStorage.getItem('buttonState_' + taskId);

        if (buttonState === 'clicked') {
            button.classList.remove('btn-secondary');
            button.classList.add('btn-warning');
            button.innerText = 'Need Help!';
        }
    });

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            changeButtonClass(this);
        });
    });
});
