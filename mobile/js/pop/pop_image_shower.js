Vue.component('com-pop-image',{
    props:['ctx'],
    data:function(){
        return {
            crt_view:'2d',
            read_3d:''
        }
    },
    computed:{
        wraped_3d:function(){
            return '/3d_wrap?d3_url='+encodeURIComponent(this.ctx.floor.img_3d)
        }
    },
    methods:{
        start_read:function(){
            this.read_3d= this.wraped_3d
        }
    },
    template:`<div class="com-pop-image"  style="position: absolute;top:0;left: 0;bottom: 0;right: 0;">
             <img  class="center-vh" :src="ctx.imgsrc" style="max-width: 95%;max-height:95%" alt="">
    </div>`
})