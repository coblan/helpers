var ua = navigator.userAgent.toLocaleLowerCase();
var pf = navigator.platform.toLocaleLowerCase();
var isAndroid = (/android/i).test(ua)||((/iPhone|iPod|iPad/i).test(ua) && (/linux/i).test(pf))
    || (/ucweb.*linux/i.test(ua));
var isIOS =(/iPhone|iPod|iPad/i).test(ua) && !isAndroid;
var isWinPhone = (/Windows Phone|ZuneWP7/i).test(ua);


export var layout= {
    device: {
        pc:!isAndroid && !isIOS && !isWinPhone,
        ios:isIOS,
        android:isAndroid,
        winPhone:isWinPhone
    },
    stickup: function (node) {
        var $cur = $(node);//方便后面操作this。
        var top = $cur.offset().top;//获取元素距离顶部的距离
        var left = $cur.offset().left;//获取元素的水平位置
        var width = $cur.width();//获取元素的宽度
        var height = $cur.height();//获取元素的高度

        //克隆这个元素，这里opactiy和display:none 是双重保险.
        var now = $cur.clone().css("opacity", 0).insertBefore($cur).hide();

        $(window).on("scroll", function () {


            var socrllTop = $(window).scrollTop();
            if (socrllTop >= top) {
                setStick();
            } else {
                unsetStick()
            }
        })

        function setStick() {
            console.log($(window).scrollLeft())
            $cur.css({
                "position": "fixed",
                "left": left - $(window).scrollLeft(),
                "top": 0,
                "width": width,
                "height": height,
                "z-index": 10
            })
            now.show();
        }

        function unsetStick() {
            $cur.removeAttr("style"),
                now.hide()
        }
    }
}