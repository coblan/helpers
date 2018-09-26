export  var pop_fields={
    template:'<span v-text="show_text" @click="edit_me()" class="clickable"></span>',
    props:['rowData','field','index'],
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
        if(table_par){
            var value = this.rowData[this.field]
            this.head  = ex.findone(table_par.heads,{name:this.field})
        }

    },
    computed:{
        show_text:function(){
            if(this.head.show_label){
                return show_label[this.head.show_label.fun](this.rowData,this.head.show_label)
            }else {
                return this.rowData[this.field]
            }
        }
    },
    methods:{
        edit_me:function(){
            this.open_layer()
        },
        open_layer:function(){
            var self=this
            var fields_ctx={
                heads:self.table_par.head.fields_heads,
                ops:[{
                    'name':'save','editor':'com-field-op-btn','label':'确定', 'icon': 'fa-save',
                }],
                extra_mixin:[]
            }

               var win= pop_edit_local(self.rowData,fields_ctx,function(new_row) {
                   ex.assign(self.rowData,new_row)
                    //self.$emit('on-custom-comp',{fun:'edit_over'} )
                   layer.close(win)
                })

        }

    }
}
Vue.component('com-table-pop-fields-local',pop_fields)

var show_label={
    use_other_field:function(row,kws){
        var other_field=kws.other_field
        return row[other_field]
    },
    text_label:function(row,show_label){
        return show_label.text
    }
}

//var get_row={
//    use_table_row:function(callback,row,kws){
//        callback(row)
//    },
//    get_table_row:function(callback,row,kws){
//        var cache_row=ex.copy(row)
//        callback(cache_row)
//    },
//    get_with_relat_field:function(callback,row,kws){
//        var director_name=kws.director_name
//        var relat_field = kws.relat_field
//
//        var dc ={fun:'get_row',director_name:director_name}
//        dc[relat_field] = row[relat_field]
//        var post_data=[dc]
//        cfg.show_load()
//        ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
//            cfg.hide_load()
//            callback(resp.get_row)
//        })
//
//    }
//}
//
//var after_save={
//    do_nothing:function(self,new_row,old_row,table){
//    },
//    update_or_insert:function(self,new_row,old_row){
//        self.$emit('on-custom-comp',{name:'update_or_insert',new_row:new_row,old_row:old_row})
//        //if(! old_row.pk) {
//        //    table.rows.splice(0, 0, new_row)
//        //}else{
//        //    ex.assign(table.rowData,new_row)
//        //}
//
//
//    }
//}