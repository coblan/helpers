

Vue.component('com-field-picture',{
    props:['row','head'],
    template:`<div class="com-field-picture picture">
            <input class="virtual_input" style="position:absolute;height: 0;width: 0;" type="text"  :name="head.name" v-model="row[head.name]">
            <img class="img-uploador" v-if='head.readonly' :src='row[head.name]'/>
			<img-uploador @select="on_uploader_click()" v-else :up_url="head.up_url" v-model="row[head.name]" :id="'id_'+head.name" :config="head.config"></img-uploador></div>`,
    methods:{
        on_uploader_click:function(){
            $(this.$el).find('.virtual_input').focus()
        }
    }
})
