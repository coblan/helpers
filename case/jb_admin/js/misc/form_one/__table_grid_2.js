Vue.component('com-fields-table-block',{
    props:['heads','row','layout'],
    template:`<div class="table-fields">
           <table >
            <tr v-for="heads_row in table_grid_heads">
                <template v-for="head in heads_row">
                    <td class="field-label-td"  :class="head.class" >
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
                            <span v-if="head.help_text" class="help-text clickable">
                                 <i style="color: #3780af;position: relative;top:10px;"   @click="show_msg(head.help_text,$event)" class="fa fa-question-circle" ></i>
                            </span>
                        </div>
                    </td>
                </template>
            </tr>
        </table>
       </div>`,
    computed:{
        table_grid_heads:function(){
            alert('jjy')
            var self=this
            var table_grid = this.layout.table_grid
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
})