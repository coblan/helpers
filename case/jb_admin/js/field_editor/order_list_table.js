var order_list =  {
    props:['row','head'],
    template:`<div class="com-field-table-list">
    <div>
        <button @click="add_new()" class="btn btn-default btn-xs">
            <i style="color: green" class="fa fa-plus-circle"></i>
        </button>
        <button @click="delete_rows()" :disabled="selected.length==0" class="btn btn-default btn-xs">
            <i style="color: red" class="fa fa-minus-circle"></i>
        </button>
        <div style="display: inline-block;position: relative;vertical-align: top">
            <textarea :name="head.name" v-model="row[head.name]"  style="display: none"></textarea>
        </div>
    </div>


                    <el-table ref="core_table" class="table"
                              :data="rows"
                              border
                              :stripe="true"
                              size="mini"
                              :summary-method="getSum"
                               @selection-change="handleSelectionChange"
                              style="width: 100%">
                        <el-table-column
                                type="selection"
                                width="55">
                        </el-table-column>

                        <template  v-for="col in heads">

                            <el-table-column v-if="col.editor"
                                             :show-overflow-tooltip="is_show_tooltip(col) "
                                             :label="col.label"
                                             :prop="col.name.toString()"
                                             :width="col.width">
                                <template slot-scope="scope">
                                    <component :is="col.editor"
                                               @on-custom-comp="on_td_event($event)"
                                               :row-data="scope.row" :field="col.name" :index="scope.$index">
                                    </component>

                                </template>

                            </el-table-column>
                            <el-table-column v-else
                                             :show-overflow-tooltip="is_show_tooltip(col) "
                                             :prop="col.name.toString()"
                                             :label="col.label"
                                             :width="col.width">
                            </el-table-column>
                        </template>
                    </el-table>
              </div>`,
    mixins:[mix_table_data,mix_ele_table_adapter],
    data:function(){
        if(this.row[this.head.name]){
            var rows = JSON.parse(this.row[this.head.name])
        }else{
            var rows = []
        }

        return {
            rows:rows,
            row_sort:{},
            heads:this.head.table_heads,
            selected:[],
        }

    },
    mounted:function(){
        //var self=this
        //ex.assign(this.op_funs, {
        //        edit_over: function () {
        //            self.row[self.head.name] = JSON.stringify(self.rows)
        //        },
        //    }
        //)
        //this.$on('commit',this.on_commit)
    },
    computed:{
       out_row_this_field:function(){
           return this.row[this.head.name]
       }
    },
    watch:{
        out_row_this_field:function(){
            if(this.row[this.head.name]){
                this.rows = JSON.parse(this.row[this.head.name])
            }else{
                this.rows = []
            }
        },
        rows:{
            handler: function(v){
                if(v.length>0){
                    Vue.set(this.row,this.head.name,JSON.stringify(v))
                    //this.row[this.head.name] = JSON.stringify(v)
                }else{
                    Vue.set(this.row,this.head.name,'')
                    //this.row[this.head.name] = ''
                }

            },
            deep: true
        },



    },
    methods:{
        commit:function(){
            var self=this
            self.row[self.head.name] = JSON.stringify(self.rows)
        },
        add_new:function(){
            var self = this
            self.crt_row = {}

            var fields_ctx={
                heads:self.head.fields_heads,
                ops_loc:'bottom',
                //extra_mixin:[],
                save_express:'scope.vc.$emit("finish",scope.vc.row);rt=Promise.resolve(scope.vc.row)',
                ops:[{
                    'name':'save','editor':'com-field-op-btn','label':'确定', 'icon': 'fa-save',
                }],
                genPar:self,
            }
           //var win= pop_edit_local(self.crt_row,fields_ctx,function(resp) {
           //     var new_row=resp
           //     ex.vueAssign(self.crt_row,new_row)
           //    self.rows.push(self.crt_row)
           //    layer.close(win)
           // })
            cfg.pop_vue_com('com-form-one',fields_ctx).then((row)=>{
                self.rows.push(row)
            })
        },
        delete_rows:function(){
            var self=this
            layer.confirm('确定删除?', {icon: 3, title:'提示'}, function(index){
                //do something
                ex.remove(self.rows,function(row){
                    return self.selected.indexOf(row )!=-1
                })
                layer.close(index);
            });
            //alert(this.selected.length)
        },
        norm_head:function(head,row){
            if(row._editing){
                
            }
        }
    }

}

Vue.component('com-field-table-list',order_list)