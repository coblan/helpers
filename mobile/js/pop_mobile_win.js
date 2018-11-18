require('./scss/pop_mobile_win.scss')

function pop_mobile_win(editor,ctx,callback){
    var pop_id =new Date().getTime()
    $('body').append(`<div id="pop-${pop_id}" class="pop-moible-win">
            <mt-popup  @input="on_input($event)"
                  v-model='show'
                  popup-transition="popup-fade">
                    <component :is="editor" :ctx="ctx" @finish="on_finish($event)"></component>
            </mt-popup>
            </div>`)

    var bb= new Vue({
        el:'#pop-'+pop_id,
        data:{
            ctx:ctx,
            editor:editor,
            show:true
        },

        destroyed:function(){
            $('#pop-'+pop_id).remove()
        },
        methods:{
            on_input:function(e){
                console.log(e)

                if(!e){
                    var self=this
                    setTimeout(function(){
                        self.$destroy()
                    },3000)
                }
            },
            on_finish:function(e){
                if(callback){
                    callback(e)
                }
            },
        }
    })
    return function (){
        bb.show=false
    }

}



export  function pop_layer (com_ctx,component_name,callback,layerConfig){
    // row,head ->//model_name,relat_field


    var pop_id =new Date().getTime()

    var layer_config = {
        type: 1,
        area: ['800px', '500px'],
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
        //shadeClose: true, //点击遮罩关闭
        content:`<div id="fields-pop-${pop_id}">
                    <component :is="component_name" :ctx="com_ctx" @finish="on_finish($event)"></component>
                </div>`,
        end: function () {

            //eventBus.$emit('openlayer_changed')

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




window.pop_mobile_win = pop_mobile_win