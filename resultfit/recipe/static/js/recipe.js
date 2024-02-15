$(document).ready(function(){
    $('#add-ingredient').on('click', function () {
        console.log('add-ingredient');
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
    //choose ingredient from datalist
    $(document).on('input', '.product_name', function () { //(".product_name").on('input'
        prodId = $(this).attr('id').split('-')[1];
        console.log('product input', prodId);
        //send ajax for update datalist
        $.ajax({
            data: {
                "inputVal": this.value
            }, // получаяем данные формы
            url: "update_datalist",
            // если успешно, то
            success: function (response) {
                console.log('response', response);
                datalist = ''
                for (i in response.products) {
                    console.log('product', response.products[i].name);
                    datalist += `<option value='${response.products[i].name}'></option>`;
                }
                $('#products-'+prodId).html(datalist);
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
    $(".product_name").on('blur', function () {
        console.log('product choosen (blur)', this.value);
        //send ajax for update unitType
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