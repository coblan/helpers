Vue.component('com-field-richtext',{
    props:['row','head'],
    template:`<div class="com-field-richtext">
            <span v-if='head.readonly' v-text='row[head.name]'></span>
            <div v-else>
                <ckeditor ref="ck" :style="head.style" v-model="row[head.name]"
                :maxlength='head.maxlength'
                :id="'id_'+head.name" :set="head.set" :config="head.config"></ckeditor>
                <div style="height: 1em;width: 0;position: relative">
                <input type="text" :name='head.name' style="display: none"  v-model="row[head.name]">
                </div>
            </div>
         </div>`,
    methods:{
        commit:function(){
            Vue.set(this.row,this.head.name,this.$refs.ck.editor.getData())
        }
    }
})