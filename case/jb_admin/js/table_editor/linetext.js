require('./scss/linetext.scss')
var line_text = {
    props:['rowData','field','index'],
    template:`<div :class="['com-table-linetext',{'dirty':is_dirty}]"><input @change="on_changed()" style="width: 100%" type="text" v-model="rowData[field]"></div>`,
    data:function(){
        return {
            org_value:this.rowData[this.field]
        }
    },
    computed:{
        is_dirty:function(){
            return this.rowData[this.field] != this.org_value
        }
    },
    watch:{
        'rowData._hash':function(){
            this.org_value=this.rowData[this.field]
        }
    },
    methods:{
        on_changed:function(){
            this.$emit('on-custom-comp',{name:'row_changed',row:this.rowData})
        }
    }
}

Vue.component('com-table-linetext',line_text)
