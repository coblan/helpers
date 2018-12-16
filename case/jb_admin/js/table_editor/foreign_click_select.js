
var foreign_click_select = {
    props:['rowData','field','index'],
    template:`<span class="clickable" v-text="rowData[field]" @click="on_click()"></span>`,
    data:function(){
        return {
            parStore:ex.vueParStore(this),
            label:'_'+this.field+'_label'
        }
    },
    computed:{
    },
    methods:{
        on_click:function(){
            //this.$emit('on-custom-comp',{fun:'send_select',row:this.rowData})
            this.parStore.$emit('finish',this.rowData)
        }
    }
}

Vue.component('com-table-foreign-click-select',foreign_click_select)
