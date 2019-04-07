require('./scss/linetext.scss')
var line_text = {
    props:['rowData','field','index'],
    template:`<div :class="['com-table-linetext',{'dirty':is_dirty}]">
        <span v-if="readonly" v-text="rowData[field]"></span>
        <input v-else @change="on_changed()" style="width: 100%" type="text" v-model="rowData[field]">
    </div>`,
    data:function(){
        return {
            org_value:this.rowData[this.field]
        }
    },
    created:function(){
        // find head from parent table
        var table_par = this.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        this.table_par = table_par
        this. head  = ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        is_dirty:function(){
            return this.rowData[this.field] != this.org_value
        },
        readonly:function(){
            if(this.head.readonly){
                return readonly[this.head.readonly.fun](this,this.head.readonly)
            }else{
                return false
            }
        }
    },
    watch:{
        'rowData._hash':function(){
            this.org_value=this.rowData[this.field]
        }
    },
    methods:{
        getRowValue:function(field){
            return this.rowData[field]
        },
        on_changed:function(){
            var value = this.rowData[this.field]
            if(value==this.org_value){
                this.$emit('on-custom-comp',{name:'row_changed_undo_act',row:this.rowData})
            }else{
                this.$emit('on-custom-comp',{name:'row_changed',row:this.rowData})
            }

        }
    }
}

Vue.component('com-table-linetext',line_text)

var readonly={
    checkRowValue:function(self,kws){
        var field = kws.field
        var target_value = kws.target_value
        return self.rowData[field] == target_value
    },
}
