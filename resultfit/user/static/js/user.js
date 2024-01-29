$(document).ready(function(){
    $('#chooseTrainer').on('click', function () {
        console.log('chooseTrainer');
        // создаем AJAX-вызов
        $.ajax({
            data: {
                "thainer": $(this).val()
            }, // получаяем данные формы
            url: "choose_trainer",
            // если успешно, то
            success: function (response) {
                $('#success_code').text("Ваша заявка была отправлена тренеру: "+$('#trainers p').text()+".<br>Вы получите уведомление, когда тренер примет решение.");
                $('#messages').css('display', 'flex');
                $('#trainer-list').css('display', 'none');
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    })
})