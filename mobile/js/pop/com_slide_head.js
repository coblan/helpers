Vue.component('com-slide-head',{
    props:['title'],
    template:`<div style="height: 6rem;flex-shrink:0;background-color: #393738;color: white;position: relative">
        <div class="center-v" style="left: 1rem;padding: 1rem" @click="go_back()"><i class="fa fa-angle-left fa-2x"></i></div>
        <div class="center-vh"  v-text="title"></div>
    </div>`,
    methods:{
        go_back:function(){
            history.back()
        }
    }
})