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
    is_small_screen:function(){
       return $(window).width()<760
    },
    stickup: function (node,options) {
        /*
        node: stickup 的元素
        options:
            dom: 滚动的容器，dom外层不能滚动，否则不能定位
            top: stick时，距离窗口上边的距离
        * */
        var dom = options.dom || window
        var fixed_top = options.top || 0
        var $cur = $(node);//方便后面操作this。
        var dom_top = $(dom).offset().top;
        var top = $cur.offset().top;//获取元素距离顶部的距离
        var left = $cur.offset().left;//获取元素的水平位置
        var width = $cur.width();//获取元素的宽度
        var height = $cur.height();//获取元素的高度

        //克隆这个元素，这里opactiy和display:none 是双重保险.
        var now = $cur.clone().css("opacity", 0).insertBefore($cur).hide();

        $(dom).on("scroll", function () {


            var socrllTop = $(dom).scrollTop();
            if (socrllTop >= (top-dom_top)) {
                setStick();
            } else {
                unsetStick()
            }
        })

        function setStick() {
            console.log($(dom).scrollLeft())
            $cur.css({
                "position": "fixed",
                "left": left - $(dom).scrollLeft(),
                "top": fixed_top,
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