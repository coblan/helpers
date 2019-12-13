//https://bing.ioliu.cn/photo/BlueChip_ZH-CN7376022522?force=home_1

require('./styl/transparent_ctn.styl')

Vue.component('com-top-transparent-ctn',{
    props:['ctx'],
    template:`<div class="com-top-transparent-ctn" :style="mystyle">
        <div class = 'web-wrap'>
        <!--<div v-if="ctx.title" class="title" v-text="ctx.title"> </div>-->
        <!--<div v-if="ctx.sub_title" class="sub-title" v-text="ctx.sub_title"></div>-->
        <!--<div class="block-content">-->
          <!--<component v-for="item in ctx.items" :is="item.editor" :ctx="item"></component>-->
        <!--</div>-->
        </div>
    </div>`,
    computed:{
        mystyle(){

            return {'background-image':'url('+ this.ctx.image_url +')'}
        }
    }
})