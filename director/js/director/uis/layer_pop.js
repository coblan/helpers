
function popSimField(kws){
    var innKws={
        com:'',
        title:'',
        resize:true,
        width:'800px',
        height:'600px',
        comBus:''
    }

    ex.assign(innKws,kws)

    var pop_id =new Date().getTime()
    var opened_layer_indx = layer.open({
        type: 1,
        area: [innKws.width, innKws.height],
        title: innKws.title,
        resize:innKws.true,
        //resizing: function(layero){
        //    var total_height= $('#fields-pop-'+pop_id).parents('.layui-layer').height()
        //    $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height-42)
        //},
        shadeClose: true, //点击遮罩关闭
        content:`<div id="fields-pop-${pop_id}" style="height: 100%;">
                    <component :is="com"  @finish="" :com-bus="comBus" ></component>
                </div>`,
        end: function () {

            //eventBus.$emit('openlayer_changed')

        }
    })
    Vue.component('com-sim-fields',{
        props:{
            heads:'',
            row:'',
            title:{
                default:function(){
                    return '详细'
                }
            }
        },
        data:function (){
            return {
            }
        },
        mixins:[mix_nice_validator],
        template:`
      <el-dialog
              title=title
              :visible.sync="dialogVisible"
              width="34em" >

          <div class="field-panel" style="text-align:center;">
                <com-table-fields :heads="heads" :row="row"
                    input-width="23em" label-width="5em"
                    style="width: 30em;text-align: left;display: inline-block;">
                    <slot>
                    <tr>
                    <td></td>
                    <td>
                    <button @click="submit"
                        style="width: 27em;position: relative;" type="btn"
                            class="btn btn-primary btn-sm"><span v-text="submitLabel"></span></button></td>
                    </tr>
                    </slot>
           </com-table-fields>

        </el-dialog>
        </div>`,
        computed:{
            inn_row:function(){
                return ex.copy(this.row)
            },
            submitLabel:function(){
                submitLabel
            }
        },
        methods:{
            submit:function(){
                if (this.before_save()=='break')return
                cfg.show_load()
                var self=this
                service_post('/agent/account/bonu',this.inn_row,function(resp){
                    ex.assign(self.row,self.inn_row)
                    cfg.hide_load(400)
                })
            }
        }
    })
}