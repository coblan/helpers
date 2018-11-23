import {pop_fields} from './pop_fields'

var pop_fields_from_row={
    // fields 的 所有 ctx 从row中获取 。
    // 因为有时，需要根据不同的row，显示不同的 forms。 
    mixins:[pop_fields],
    methods:{
        open_layer:function(){
            var self=this
            var ctx_name=this.rowData[this.head.ctx_field]
            var allinone_ctx = named_ctx[ctx_name]
            var fun= get_row[allinone_ctx.get_row.fun]
            if(allinone_ctx.get_row.kws){
                //  这个是兼顾老的调用，新的调用，参数直接写在get_row里面，与fun平级
                var kws= allinone_ctx.get_row.kws
            }else{
                var kws= allinone_ctx.get_row
            }
            kws.director_name = allinone_ctx.fields_ctx.director_name

            fun(function(pop_row){
                //pop_fields_layer(pop_row,self.head.fields_heads,ops,self.head.extra_mixins,function(kws){
                var win_index =  pop_fields_layer(pop_row,allinone_ctx.fields_ctx,function(new_row){

                    var fun = after_save[allinone_ctx.after_save.fun]
                    fun(self,new_row,pop_row)

                    layer.close(win_index)

                })
            },this.rowData,kws)

        }
    }

}

Vue.component('com-table-pop-fields-from-row',pop_fields_from_row)

var show_label={
    use_other_field:function(row,kws){
        var other_field=kws.other_field
        return row[other_field]
    },
    text_label:function(row,show_label){
        return show_label.text
    }
}

var get_row={
    use_table_row:function(callback,row,kws){
        callback(row)
    },
    get_table_row:function(callback,row,kws){
        var cache_row=ex.copy(row)
        callback(cache_row)
    },
    get_with_relat_field:function(callback,row,kws){
        var director_name=  kws.director_name
        var relat_field = kws.relat_field

        var dc ={fun:'get_row',director_name:director_name}
        dc[relat_field] = row[relat_field]
        var post_data=[dc]
        cfg.show_load()
        ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
            cfg.hide_load()
            callback(resp.get_row)
        })

    }
}

var after_save={
    do_nothing:function(self,new_row,old_row,table){
    },
    update_or_insert:function(self,new_row,old_row){
        self.parStore.update_or_insert(new_row,old_row)
        //self.$emit('on-custom-comp',{name:'update_or_insert',new_row:new_row,old_row:old_row})
        //var par_name=ex.vuexParName(self)
        //if(par_name){
        //self.parStore.$emit('row.update_or_insert',{new_row:new_row,old_row:old_row})
        //}
    }
}