

Vue.component('com-field-picture',{
    props:['row','head'],
    template:`<div class="com-field-picture picture">
            <input class="virtual_input" style="position:absolute;height: 0;width: 0;" type="text"  :name="head.name" v-model="row[head.name]">
            <img  class="img-uploador clickable" v-if='head.readonly && row[head.name]' @click="on_click_image(row[head.name])" :src='row[head.name]'/>
			<img-uploador @select="on_uploader_click()" v-else :up_url="head.up_url" v-model="row[head.name]" :id="'id_'+head.name" :config="head"></img-uploador></div>`,
    methods:{
        on_uploader_click:function(){
            $(this.$el).find('.virtual_input').focus()
        },
        on_click_image(url){
            var ctx = {imgsrc:url }
            pop_layer(ctx,'com-pop-image',function(){},{
                title:false,
                area: ['90%', '90%'],
                shade: 0.8,
                skin: 'img-shower',
                shadeClose: true,
            })
        }
    }
})
