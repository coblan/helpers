require('./scss/slide_head.scss')

Vue.component('com-slide-head',{
    props:['title'],
    template:`<div class="com-slide-head">
        <div class="center-v go-back"  @click="go_back()"><i class="fa fa-angle-left fa-2x"></i></div>
        <div class="center-vh head-text"  v-text="title"></div>
    </div>`,
    methods:{
        go_back:function(){
            history.back()
        }
    }
})