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