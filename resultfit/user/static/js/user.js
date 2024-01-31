$(document).ready(function(){
    $('.chooseTrainer').on('click', function () {
        console.log('chooseTrainer', $(this).val());
        // создаем AJAX-вызов
        $.ajax({
            data: {
                "trainer": $(this).val()
            }, // получаяем данные формы
            url: "choose_trainer",
            // если успешно, то
            success: function (response) {
                if (response.error) {
                    $('#success_code').text(response.error);
                    $('#messages').css('display', 'flex');
                } else {
                    $('#success_code').text("Ваша заявка была отправлена тренеру: "+response.trainer+". Вы получите уведомление, когда тренер примет решение.");
                    $('#messages').css('display', 'flex');
                    $('#trainer-list').css('display', 'none');
                }
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