
Vue.component('com-head-bell-msg',{
    props:['head'],
    template:` <li  class="com-head-bell-msg dropdown notifications-menu" @click="on_click()">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            <i class="fa fa-bell-o"></i>
            <span v-if="head.count !=0 " class="label label-warning" v-text="head.count"></span>
        </a>
    </li>`,
    mounted(){
      if(this.head.init_express){
          ex.eval(this.head.init_express,{head:this.head,vc:this})
      }
    },
    methods:{
        on_click:function(){
            if(this.head.link){
                location = this.head.link
            }
        }
    }
})



