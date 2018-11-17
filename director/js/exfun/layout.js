export var layout= {
    stickup: function (node,options) {
        /*
        node: 需要stickup的元素
        options:
            dom: 滚动的容器元素。注意：滚动元素应该的父元素不能 **再滚动**了。
            top：stickup 时距离上边缘的距离

        * */
        var dom=options.dom || window
        var fixed_top = options.top || 0;
        var $cur = $(node);//方便后面操作this。
        var top = $cur.offset().top;//获取元素距离顶部的距离
        var left = $cur.offset().left;//获取元素的水平位置
        var width = $cur.width();//获取元素的宽度
        var height = $cur.height();//获取元素的高度

        //克隆这个元素，这里opactiy和display:none 是双重保险.
        var now = $cur.clone().css("opacity", 0).insertBefore($cur).hide();

        $(dom).on("scroll", function () {


            var socrllTop = $(dom).scrollTop();
            if (socrllTop >= top) {
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
    },
    stickupNest: function (options) {
        // {slide:'xxx',node:'xxx'}
        var slide = options.slide
        var node =options.node
        var $slide=$(slide)
        var $cur = $(node);//方便后面操作this。

        //var top = $cur.offset().top;//获取元素距离顶部的距离
        var left = $cur.offset().left;//获取元素的水平位置
        var width = $cur.width();//获取元素的宽度
        var height = $cur.height();//获取元素的高度

        //克隆这个元素，这里opactiy和display:none 是双重保险.
        var now = $cur.clone().css("opacity", 0).insertBefore($cur).hide();

        $slide.on("scroll", function () {
            var par_top = $slide.offset().top;
            //var slide_top = $slide.offset().top;
            var cur_top = $cur.offset().top;
            var socrllTop =  $slide.scrollTop();
            if (par_top >= cur_top) {
                setStick(par_top);
            } else {
                unsetStick()
            }
        })

        function setStick(top) {
            //console.log($(dom).scrollLeft())
            //$cur.addClass(cls)
            $cur.css({
                "position": "fixed",
                "left": left - $slide.scrollLeft(),
                "top": top ,
                "width": width,
                "height": height,
                "z-index": 10
            })
            now.show();
        }

        function unsetStick() {
            $cur.removeAttr("style"),
            //$cur.removeClass(cls)
                now.hide()
        }
    },
}