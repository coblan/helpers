require('./styl/fields_table_block.styl')

Vue.component('com-fields-table-block',{
    props:['heads','row','option'],
    template:`<div class="com-fields-table-block field-panel msg-bottom">
           <table >
            <tr v-for="heads_row in table_grid_heads">
                <template v-for="head in heads_row">
                    <td class="field-label-td" :class="head.class"  :colspan="head.label_colspan" :rowspan="head.label_rowspan">
                        <div class="field-label">
                            <span class="label-content">
                                 <span v-text="head.label"></span>
                                 <span class="req_star" v-if='head.required'>*</span>
                            </span>
                        </div>
                    </td>
                    <td class="field-input-td" :class="head.class" :colspan="head.colspan" :rowspan="head.rowspan">
                        <div class="field-input">
                            <component v-if="head.editor" :is="head.editor"
                                 @field-event="$emit('field-event',$event)"
                                 :head="head" :row="row"></component>
                            <span v-if="head.help_text" class="help-text clickable" @mouseenter="show_msg(head.help_text,$event)" @mouseleave="hide_msg()">
                                 <i style="color: #3780af;"   class="fa fa-question-circle" ></i>
                            </span>
                        </div>
                    </td>
                </template>
            </tr>
        </table>
       </div>`,
    computed:{
        table_grid_heads:function(){
            var self=this
            var table_grid = this.option.table_grid
            var heads_bucket =[]
            ex.each(table_grid,function(name_row){
                let heads_row =[]
                ex.each(self.heads,function(head){
                    if(ex.isin(head.name,name_row)){
                        heads_row.push(head)
                    }
                })
                if(heads_row){
                    heads_bucket.push(heads_row)
                }
            })
            return heads_bucket
        },
    },
    methods:{
        show_msg:function(msg,event){
            this.msg_index = layer.tips(msg, event.target,{
                time:0,
            });
        },
        hide_msg:function(){
            layer.close(this.msg_index)
        }
    }
})