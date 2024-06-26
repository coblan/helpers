Vue.component('com-field-richtext',{
    props:['row','head'],
    template:`<div class="com-field-richtext">
            <div v-if='head.readonly' v-html='row[head.name]'></div>
            <div v-else>
                <ckeditor ref="ck" :style="head.style" v-model="row[head.name]"
                :maxlength='head.maxlength'
                :id="'id_'+head.name" :set="head.set" :config="head.config"></ckeditor>
                <div style="height: 1em;width: 0;position: relative">
                <input type="text" :name='head.name' style="display: none"  v-model="row[head.name]">
                </div>
            </div>
         </div>`,
    mounted(){
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,})
        }
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    },

    methods:{
        commit:function(){
            Vue.set(this.row,this.head.name,this.$refs.ck.editor.getData())
        }
    }
})