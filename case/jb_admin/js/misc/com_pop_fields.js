export var  com_pop_field= {
    props:['row','heads','ops'],
    mixins:[mix_fields_data,mix_nice_validator],
    computed:{
        real_heads:function(){
            if(this.dict_heads){
                return this.dict_heads
            }else{
                return this.heads
            }
        }
    },
    methods:{
        after_save:function(new_row){
            this.$emit('sub_success',{new_row:new_row,old_row:this.row})
            ex.assign(this.row,new_row)
        },
        del_row:function(){
            var self=this
            layer.confirm('真的删除吗?', {icon: 3, title:'确认'}, function(index){
                layer.close(index);
                var ss = layer.load(2);
                var post_data = [{fun:'del_rows',rows:[self.row]}]
                $.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    layer.close(ss)
                    self.$emit('del_success',self.row)
                })
            });
        }
    },
    template:`<div class="flex-v" style="margin: 0;height: 100%;">
    <div class = "flex-grow" style="overflow: auto;margin: 0;">
        <div class="field-panel suit" >
            <field  v-for="head in real_heads" :key="head.name" :head="head" :row="row"></field>
        </div>
      <div style="height: 15em;">
      </div>
    </div>
     <div style="text-align: right;padding: 8px 3em;">
        <component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>
    </div>
     </div>`,
        data:function(){
    return {
        fields_kw:{
            heads:this.heads,
            row:this.row,
            errors:{},
        },
     }
    }
}


//Vue.component('com-pop-fields',)