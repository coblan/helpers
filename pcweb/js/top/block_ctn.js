require('./styl/block_ctn.styl')
/*
* 块容器
* 用户存放页面中有标题和副标题的块
* */
Vue.component('com-top-block-ctn',{
    props:['ctx'],
    template:`<div class="com-top-block-ctn" :class="ctx.class">
        <div class = 'web-wrap'>
        <!--<div v-if="ctx.title" class="title" v-text="ctx.title"> </div>-->
        <!--<div v-if="ctx.sub_title" class="sub-title" v-text="ctx.sub_title"></div>-->
        <component :is="title_editor" :ctx="ctx"></component>
        <div class="block-content">
          <component v-for="item in ctx.items" :is="item.editor" :ctx="item"></component>
        </div>
        </div>
    </div>`,
    data(){
        return {
            title_editor:this.ctx.title_editor || 'com-block-title-plain'
        }
    },
    mounted(){
        if(this.ctx.css){
            ex.append_css(this.ctx.css)
        }
    }

})