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
})