function toggleNav() {
    var updateElement = document.getElementById("menu-icon");
    var openSidebar = document.getElementById("menu");
    var darken = document.getElementById("darken");
    //toggle adds a class if it's not there or removes it if it is.
    updateElement.classList.toggle("open");
    openSidebar.classList.toggle("open-menu");
    //darken.classList.toggle("darken");
} 

function openHint() {
    var hint = document.getElementById("hint");
    //toggle adds a class if it's not there or removes it if it is.
    hint.classList.toggle("open-hint");
}

$(document).ready(function(){
    $('.close').on('click', function () {
        $('#messages').css('display', 'none');
    })
})
