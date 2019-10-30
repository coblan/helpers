
require('./scss/my_slide_win.scss')

/*
* 因为没有遮挡层，可能造成多次打开窗口问题，所以使用mint-ui替代了这个组件
* */
$(function(){
    $('body').append(`<div id="com-slid-win">
        <com-slide-win-1 :stack_pages="stack_pages"></com-slide-win-1>
    </div>`)

    window.slide_win = new Vue({
        el:'#com-slid-win',
        data:{
            stack_pages:[],
        },
        methods:{
            left_in_page (payload) {
                if(this.stack_pages.length ==0 ){
                    fixed_body()
                }
                history.replaceState({pop_win:true},'')
                this.stack_pages.push(payload)
                history.pushState({},'')
            },
            right_out_page(){

                this.stack_pages.pop()
                if(this.stack_pages.length==0){
                    fixed_body_quit()
                }
            },
        }
    })


})

if(window.named_hub==undefined){
    window.named_hub={}
    window.addEventListener('popstate' ,function (event) {
        if(event.state && event.state.pop_win){
            slide_win.right_out_page()
        }
        if(event.state && event.state.callback){
            var callback = named_hub[event.state.callback]
            //alert(JSON.stringify(event))
            //alert(JSON.stringify(event.state))
            callback()
            //delete named_hub[event.state.callback]
        }
        //event.preventDefault();
        //return false
    })

}

Vue.component('com-slide-win-1',{
    props:['stack_pages'],
    template:`<div  class="com-slide-win">
        <transition-group name="list" tag="p">
            <div class="mywrap" v-for="(page,index) in stack_pages"
                 style="position:fixed;top:0;left: 0;right: 0;bottom: 0;background-color: white;z-index:1000;
                 pointer-events: auto ;-moz-box-shadow:0px 0px 5px #333333; -webkit-box-shadow:0px 0px 5px #333333; box-shadow:0px 0px 5px #333333;">
                <com-slide-head :title="page.ctx? page.ctx.title:''" ></com-slide-head>
                <component class="pop-content" :is="page.editor" :ctx="page.ctx" @finish="on_finish($event,page)"></component>
            </div>
        </transition-group>
    </div>`,
    created:function(){
        //var client_h = document.documentElement.clientHeight;
        //$(window).on("resize",function(){
        //    var body_h =  document.body.scrollHeight;
        //    if(body_h < client_h){
        //        $(".mywrap").removeClass("fixed");
        //        console.log("小了");
        //    }else{
        //        console.log("正常");
        //        $(".mywrap").addClass("fixed");
        //    }
        //});

        //var winHeight = $(window).height(); //获取当前页面高度
        //$(window).resize(function() {
        //    //当窗体大小变化时
        //    var thisHeight = $(this).height();  //窗体变化后的高度
        //    if (winHeight - thisHeight > 50) {
        //        /*
        //         软键盘弹出
        //         50是设置的阈值，用来排除其他影响窗体大小变化的因素，比如有的浏览器的工具栏的显示和隐藏
        //         */
        //        //$(".mywrap").removeClass("fixed");
        //        //$('.com-slide-win').height(winHeight + 'px')
        //        $('body').css('height', winHeight + 'px');
        //    } else {
        //        /*
        //         软键盘关闭
        //         */
        //        //$(".mywrap").addClass("fixed");
        //        //$('.com-slide-win').height('100vh')
        //        $('body').css('height', '100%');
        //    }
        //});


        //this.$store.registerModule('slide_win',{
        //    state:{
        //        stack_pages:[],
        //    },
        //    mutations:{
        //        left_in_page (state,payload) {
        //            history.replaceState({pop_win:true},'')
        //            state.stack_pages.push(payload)
        //            history.pushState({},'')
        //            //state.show_lay_out=true
        //        },
        //        right_out_page(state){
        //            state.stack_pages.pop()
        //        },
        //    }
        //})
    },
    methods:{

        on_finish:function(e,page){
            if(page.callback){
                page.callback(e)
            }
        }
    }
})