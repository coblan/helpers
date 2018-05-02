export var mix_editor={
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
    methods:{
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