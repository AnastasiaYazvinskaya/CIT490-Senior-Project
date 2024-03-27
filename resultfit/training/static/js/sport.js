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
        // создаем AJAX-вызов
        $.ajax({
            data: {
                "code": $('#id_code').val()
            }, // получаяем данные формы
            url: "validate_code",
            // если успешно, то
            success: function (response) {
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
                        $('#code_error').attr('title', 'Не найден тренер с этим кодом. Проверьте код и попробуйте ещё раз.');
                        $('#code_error').css('display', 'inline');
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

    $('.sendEmailBtn').on('click', function () {
        // создаем AJAX-вызов
        $.ajax({
            data: {
                "email": $(this).val()
            }, // получаяем данные формы
            url: "send_email",
            // если успешно, то
            success: function (response) {
                $('#success_code').text("Повторное письмо для регистрации отправлено на "+response.email);
                $('#messages').css('display', 'flex');
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });

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
    });

    $('#add-exercise').on('click', function () {
        console.log('add-exercise');
        var num = $('#formset').children().length;
        var newForm = document.getElementById('empty-form').cloneNode(true);
        newForm.setAttribute('id', 'form-'+num);
        const regex = new RegExp('__prefix__', 'g');
        newForm.innerHTML = newForm.innerHTML.replace(regex, num);
        var totalNewForms = document.getElementById('id_form-TOTAL_FORMS');
        totalNewForms.setAttribute('value', num+1);
        document.getElementById('formset').append(newForm);
        return false;
    });

    //delete ingredient
    $(document).on('click', '.delete', function () {
        console.log('delete', $(this).val());
        var deleteEl = $(this).val();
        if (document.getElementById('id_form-'+deleteEl.split('-')[1]+'-DELETE')) {
            $('#'+deleteEl).css('display', 'none')
            var selector = '#id_form-'+deleteEl.split('-')[1]+'-DELETE';
            $(selector).attr('checked', 'checked');


        }
        else {
            var deleteID = '#'+deleteEl;
            var num = $('#formset').children().length;
            var totalNewForms = document.getElementById('id_form-TOTAL_FORMS');
            totalNewForms.setAttribute('value', num--);
            $(deleteID).remove();
            for (i=0; i<num; i++) {
                if (!document.getElementById('id_form-'+i+'-DELETE')) {
                    var child = $('#formset').children()[i];
                    var id = child.getAttribute('id');
                    child.removeAttribute('id');
                    child.setAttribute('id', 'form-'+i)
                    const regex = new RegExp('-'+id.split('-')[1], 'g');
                    child.innerHTML = child.innerHTML.replace(regex, '-'+i);
                }
            }
        }
    })
})