//Generate code
function generateCode() {
    var characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = ' ';
    const charactersLength = characters.length;
    for ( let i = 0; i < 15; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    document.getElementById('id_code').value = result;
}
$(document).ready(function(){
    $('#checkCodeBtn').on('click', function () {
        console.log('checkCodeBtn clicked');
        // создаем AJAX-вызов
        $.ajax({
            data: {
                "code": $('#id_code').val()
            }, // получаяем данные формы
            url: "validate_code",
            // если успешно, то
            success: function (response) {
                console.log(response);
                if (response.trainer) {
                    console.log('response.trainer exists');
                    $('#id_last_name').val(response.trainer.lastName);
                    $('#id_first_name').val(response.trainer.firstName);
                    $('#id_email').val(response.trainer.email);
                }
                else {
                    if (response.error){
                        console.log('response.error exists');
                        $('#code_error').text(response.error);
                    } else {
                        console.log('do not find trainer');
                        $('#code_error').value = 'Не найден тренер с этим кодом. Проверьте код и попробуйте ещё раз.';
                    }
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