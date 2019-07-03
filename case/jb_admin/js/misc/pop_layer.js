import {get_proper_size} from  './pop_fields_layer'
export  function pop_layer (com_ctx,component_name,callback,layerConfig){
    // row,head ->//model_name,relat_field


    var pop_id =new Date().getTime()
    var psize = get_proper_size()
    var layer_config = {
        type: 1,
        area: psize,// ['800px', '500px'],
        title: '详细',
        resize:true,
        resizing: function(layero){
            var total_height= $('#fields-pop-'+pop_id).parents('.layui-layer').height()
            if(this.title){
                $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height-42)
            }else{
                $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height)
            }

        },
        //shadeClose: true, //点击遮罩关闭  style="height: 100%;width: 100%"
        content:`<div id="fields-pop-${pop_id}" class="pop-layer" style="height: 100%;width: 100%">
                    <component :is="component_name" :ctx="com_ctx" @finish="on_finish($event)"></component>
                </div>`,
        end: function () {
        }
    }
    if(layerConfig){
        ex.assign(layer_config,layerConfig)
    }
    var opened_layer_index = layer.open(layer_config);

        new Vue({
            el:'#fields-pop-'+pop_id,
            data:{
                com_ctx:com_ctx,
                component_name:component_name,
            },
            methods:{
                on_finish:function(e){
                    if(callback){
                        callback(e)
                    }
                }
            }
        })
    return opened_layer_index
    }




window.pop_layer = pop_layer