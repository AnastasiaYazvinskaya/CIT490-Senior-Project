$(document).ready(function(){
    $('#database').on('change', function () {
        console.log('database changed to ', $('#database').val());
        table = $('#database').val();
        // создаем AJAX-вызов
        $.ajax({
            data: {
                "database": table
            }, // получаяем данные формы
            url: "update_table",
            // если успешно, то
            success: function (response) {
                if (response.table) {
                    $('#table_name').text(response.table.table_name+' ('+response.table.db_table+')');
                    $('#table_fields').empty();
                    for (field in response.table.fields){
                        $('#table_fields').append('<tr><td>'+response.table.fields[field].name+'</td><td>'+response.table.fields[field].type+'</td></tr>');
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
    $('#add-ingredient').on('click', function () {
        var num = $('#formset').children().length;
        console.log('add-product #', num);
        var newForm = document.getElementById('empty-form').cloneNode(true);
        newForm.setAttribute('id', 'form-'+num);
        const regex = new RegExp('__prefix__', 'g');
        newForm.innerHTML = newForm.innerHTML.replace(regex, num);
        var totalNewForms = document.getElementById('id_form-TOTAL_FORMS');
        totalNewForms.setAttribute('value', num+1);
        document.getElementById('formset').append(newForm);
        //document.getElementById('formset').innerHTML += '<hr>';
        return false;
    });

    //delete ingredient
    $(document).on('click', '.delete', function () {
        var deleteID = '#'+$(this).val();
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
    })
})