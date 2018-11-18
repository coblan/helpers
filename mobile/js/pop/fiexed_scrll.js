require('./scss/fiexed_scroll.scss')

export  function fixed_body(){
    //$('body').addClass('modal-open')
    ModalHelper.afterOpen()
}
function fixed_body_quit(){
    //$('body').removeClass('modal-open')
    ModalHelper.beforeClose()
}


var ModalHelper = (function(bodyCls) {
    var scrollTop;
    return {
        afterOpen: function() {
            scrollTop = document.scrollingElement.scrollTop;
            document.body.classList.add(bodyCls);
            document.body.style.top = -scrollTop + 'px';
        },
        beforeClose: function() {
            document.body.classList.remove(bodyCls);
            // scrollTop lost after set position:fixed, restore it back.
            document.scrollingElement.scrollTop = scrollTop;
        }
    };
})('modal-open');


window.fixed_body=fixed_body
window.fixed_body_quit = fixed_body_quit