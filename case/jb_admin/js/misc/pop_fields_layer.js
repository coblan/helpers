/*
* root 层面创建Vue组件，形成弹出框

 fields_ctx:{
         'heads':[{'name':'matchid','label':'比赛','editor':'com-field-label-shower','readonly':True},
                 {'name':'home_score','label':'主队分数','editor':'linetext'},
            ],
         'ops':[{"fun":'produce_match_outcome','label':'保存','editor':'com-field-op-btn'},],
         'extra_mixins':['produce_match_outcome'],
         'fieldsPanel': 'produceMatchOutcomePanel',
         // 使用extra_mixins与fieldsPanel的区别是，设置fieldPanel可以防止引入com_pop_field对象，如果只设置extra_mixin的话，会默认引入com_pop_field
 }

* */
import {com_pop_field} from  './com_pop_fields'



export  function pop_fields_layer (row,fields_ctx,callback,layerConfig){
    // row,head ->//model_name,relat_field

    var row=ex.copy(row)
    var heads = fields_ctx.heads
    var ops = fields_ctx.ops
    var extra_mixins=fields_ctx.extra_mixins || []

    if(typeof(fields_ctx.fieldsPanel)=='string' ){
        var com_fields = window[fields_ctx.fieldsPanel] || com_pop_field
    }else{
        var com_fields = fields_ctx.fieldsPanel || com_pop_field
    }

    var id_string = JSON.stringify(com_fields) + JSON.stringify(extra_mixins)
    var com_id = md5(id_string)

    if(! window['_vue_com_'+com_id]){
        extra_mixins = ex.map(extra_mixins,function(mix){
            if(typeof(mix)=='string'){
                return window[mix]
            }else {
                return mix
            }

        })
        //var com_pop_field_real = $.extend({}, com_fields);
        //com_pop_field_real.mixins = com_fields.mixins.concat(extra_mixins)
        var com_pop_field_real =ex.vueExtend(com_fields,extra_mixins)
        Vue.component('com-pop-fields-'+com_id,com_pop_field_real)
        window['_vue_com_'+com_id] = true
    }

    var pop_id =new Date().getTime()

    var layer_config = {
        type: 1,
        area: ['800px', '500px'],
        title: '详细',
        resize:true,
        resizing: function(layero){
            var total_height= $('#fields-pop-'+pop_id).parents('.layui-layer').height()
            $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height-42)
        },
        //shadeClose: true, //点击遮罩关闭
        content:`<div id="fields-pop-${pop_id}" style="height: 100%;">
                    <component :is="'com-pop-fields-'+com_id" @del_success="on_del()" @submit-success="on_sub_success($event)"
                    :row="row" :heads="fields_heads" :ops="ops"></component>
                </div>`,
        end: function () {

            //eventBus.$emit('openlayer_changed')

        }
    }
    if(layerConfig){
        ex.assign(layer_config,layerConfig)
    }
    var openfields_layer_index = layer.open(layer_config);

    (function(pop_id,row,heads,ops,com_id,openfields_layer_index){

        //Vue.nextTick(function(){

            new Vue({
                el:'#fields-pop-'+pop_id,
                data:{
                    has_heads_adaptor:false,
                    row:row,
                    fields_heads:heads,
                    ops:ops,
                    com_id:com_id,
                },

                methods:{
                    on_sub_success:function(new_row){
                      callback(new_row,openfields_layer_index)
                        //callback({name:'after_save',new_row:event.new_row,old_row:event.old_row})


                        //if(success){
                        //    setTimeout(function(){
                        //        layer.close(openfields_layer_index)
                        //    },1000)
                        //}


                    }
                }
            })

            //eventBus.$emit('openlayer_changed')

        //})
    })(pop_id,row,heads,ops,com_id,openfields_layer_index)


    return openfields_layer_index

}

window.pop_fields_layer = pop_fields_layer