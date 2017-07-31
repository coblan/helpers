//function popup_close(){
//    window._popup_close()
//}
//function popup_assure(){
//    window._popup_assure()
//}

window._popup_close=function(){}
window._popup_assure=function(){}

export  var popup_page={
    methods:{
        selector:function(){
            alert('must custom selector')
        },
        assure:function(){
            alert('should assure function')
            this.close()
        },
        open:function(){
            var self=this
            f7_app.popup(self.selector())
            self.add_nav()
            ff.push(this.close_)

            this.old_popup_close=window._popup_close
            this.old_popup_assure=window._popup_assure
            window._popup_close=this.close
            window._popup_assure=function(){
                self.assure()
            }
        },
        close:function(){
            ff.pop()
            this.close_()
        },
        close_:function(){
            f7_app.closeModal(this.selector())
            this.rm_nav()
            window._popup_close = this.old_popup_close
            window._popup_assure = this.old_popup_assure
        },

//            search:function () {
//                setTimeout(function(){
//                    parent.replace_iframe(ex.appendSearch(search_args))
//                },300)
//            },
        add_nav:function(){
            ff.add_nav('<div class="navbar-inner temp-navbar" style="background-color: inherit;">\
                            <div class="left"><a href=" javascript:void(0)" onclick="call_iframe(\'_popup_close\')" style="padding-left: 1em;">取消</a></div>\
                            <div class="center"></div>\
                            <div class="right"><a href=" javascript:void(0)" onclick="call_iframe(\'_popup_assure\')" style="padding-right: 1em;">确定 </a></div>\
                            </div>')

        },
        rm_nav:function(){
            parent.remove_nav()
        }

    }
}