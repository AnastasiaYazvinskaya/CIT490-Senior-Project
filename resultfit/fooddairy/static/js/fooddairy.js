$(document).ready(function(){
    $('.add-comment').on('click', function () {
        note_id = $(this).val();
        $('#comment-form_'+note_id).html(`
        <div class="input_field">
            <span class="label">Комментарий</span><textarea rows='4' id='comment-text_${note_id}' name='comment'></textarea>
        </div>
        <p id="save-error_${note_id}"><p>
        <div class='single-button'>
            <button type='button' class='save-comment btn btn-primary' id='save-comment_${note_id}' value='${note_id}'>Отправить</button>
        </div>`);
        $('#add-comment_'+note_id).hide();
        return false;
    });
    $(document).on('click', '.save-comment', function () {
        console.log('save-comment');
        note_id = $(this).val();
        text = $('#comment-text_'+note_id).val();
        // создаем AJAX-вызов
        $.ajax({
            data: {
                "note_id": note_id,
                "comment": text
            }, // получаяем данные формы
            url: "save_comment",
            // если успешно, то
            success: function (response) {
                if (response.comment) {
                    $('#comments_'+note_id).prepend('<p>'+response.comment.author+' ('+response.comment.created_by+')</p>'+
                    '<p>'+response.comment.text+'</p>');//text(response.table.table_name+' ('+response.table.db_table+')');
                    $('#comment-form_'+note_id).hide();
                    $('#add-comment_'+note_id).show();
                } else if (response.error) {
                    $('#save-error_'+note_id).text(response.error);
                }
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
    });
    $('#add-note').on('click', function () {
        const currentDate = new Date().toISOString().slice(0, 10);
        $('#note-form-fields').html(`
        <div class="raw-fields">
            <div class="input_field">
                <span class="label">Дата</span><input type='date' id='day' name='day' value='${currentDate}'/>
            </div>
            <div class="input_field">
                <span class="label">Прием пищи</span>
                <select id='meal' name='meal'>
                    <option value='1'>Завтрак</option>
                    <option value='2'>Обед</option>
                    <option value='3'>Ужин</option>
                    <option value='4'>Перекус</option>
                </select>
            </div>
        </div>
        <div class="input_field">
            <span class="label">Фото</span><input type='file' id='image' name='image'/>
        </div>
        <div class="raw-fields">
            <div class="input_field">
                <span class="label">Ккал</span><input type='number' id='kkal' name='kkal'/>
            </div>
            <div class="input_field">
                <span class="label">Белки</span><input type='number' id='proteins' name='proteins'/>
            </div>
            <div class="input_field">
                <span class="label">Жиры</span><input type='number' id='fats' name='fats'/>
            </div>
            <div class="input_field">
                <span class="label">Углеводы</span><input type='number' id='carbohydrates' name='carbohydrates'/>
            </div>
        </div>
        <div class="input_field">
            <span class="label">Комментарий</span><textarea rows='3' id='comment' name='comment'></textarea>
        </div>
        <p id="note-save-error"><p>
        <div class='single-button'>
            <button type='button' class='save-note btn btn-primary'>Сохранить</button>
        </div>`);
        $('#add-note').hide();
        return false;
    });
    $(document).on('click', '.save-note', function () {
        console.log('save-note');
        var formData = new FormData()
        formData.append('date', $('#day').val());
        formData.append('meal', $('#meal').val());
        formData.append('image', $('#image').val());
        formData.append('imagef', $('#image')[0].files[0]);
        formData.append('kkal', $('#kkal').val());
        formData.append('proteins', $('#proteins').val());
        formData.append('fats', $('#fats').val());
        formData.append('carbohydrates', $('#carbohydrates').val());
        formData.append('comment', $('#comment').val());
        formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

        //$('#wait-message').show();

        // создаем AJAX-вызов
        $.ajax({
            method: "POST",
            data: formData, // получаяем данные формы
            url: "save_note/",
            processData: false,
            contentType: false,
            // если успешно, то
            success: function (response) {
                console.log(response);
                location.reload();
                //$('#add-note').show();
                //$('#note-form').hide();
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
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