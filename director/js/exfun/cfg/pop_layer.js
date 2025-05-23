
export  function pop_layer (com_ctx,component_name,callback,layerConfig){
    // row,head ->//model_name,relat_field

    function  update_size(layero){
        var total_height = layero.height()
        if(this.title){
            $(layero).children('.layui-layer-content').height(total_height-42)
        }else{
            $(layero).children('.layui-layer-content').height(total_height)
        }
        // var total_height= $('#fields-pop-'+pop_id).parents('.layui-layer').height()
        // if(this.title){
        //     $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height-42)
        // }else{
        //     $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height)
        // }
    }

    var pop_id =new Date().getTime()
    if(com_ctx.width && com_ctx.height){
        var psize =[com_ctx.width,com_ctx.height]
    } else {
        var psize =  get_proper_size()
        if(com_ctx.width){
             psize=[com_ctx.width,psize[1]]
        }
        if(com_ctx.height){
            psize=[psize[0],com_ctx.height]
        }
    }

    var layer_config = {
        type: 1,
        area: psize,// ['800px', '500px'],
        title: com_ctx.title || '详细',
        zIndex:1000,
        resize:true,
        resizing: function(layero){
            // console.log(layero)
            update_size.call(this,layero)
            // debugger
            // var total_height= $('#fields-pop-'+pop_id).parents('.layui-layer').height()
            // if(this.title){
            //     $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height-42)
            // }else{
            //     $('#fields-pop-'+pop_id).parents('.layui-layer-content').height(total_height)
            // }

        },
        restore(layero, index){
            update_size.call(this,layero)
        },
        full(layero, index){
            update_size.call(this,layero)
        },

        //shadeClose: true, //点击遮罩关闭  style="height: 100%;width: 100%"
        // content:`<div id="fields-pop-${pop_id}" class="pop-layer" style="height: 100%;width: 100%">
        //             <component :is="component_name" :ctx="com_ctx" @finish="on_finish($event)"></component>
        //         </div>`,
        content:`<div id="fields-pop-${pop_id}" class="pop-layer" style="height: 100%;width: 100%">
                   
                </div>`,
        end: function () {
            if(callback){
                callback('__end_by_user')
            }
            ex.remove(cfg.layer_index_stack,opened_layer_index)
        }
    }
    if(layerConfig){
        ex.assign(layer_config,layerConfig)
    }
    var opened_layer_index = layer.open(layer_config);
    cfg.layer_index_stack.push(opened_layer_index);
    new Vue({
        el:'#fields-pop-'+pop_id,
        data:{
            com_ctx:com_ctx,
            component_name:component_name,
        },
        render(createElement){
            if(this.com_ctx.title){
                delete  this.com_ctx.title
            }
            return createElement(this.component_name,{
                attrs:{
                    ctx:this.com_ctx,
                    ...this.com_ctx
                },
                    on:{
                        finish:this.on_finish
                    }
            }

                )
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

export function get_proper_size(){
    var ww= $(window).width()
    var wh=$(window).height()
    var width = 0
    var height = 0
    if(ww > 1800){width = '1200px'}
    else if(ww>1600){width = '1100px'}
    else if(ww>1500){width = '1050px'}
    else if(ww>1400){width = '1000px'}
    else if(ww>1200){width = '900px'}
    else if(ww>900){ width ='800px'}
    else {width=ww*0.9+'px'}

    if (wh > 1400){height ='1000px'}
    else if(wh>1300){height ='900px' }
    else if(wh>1200){height ='800px' }
    else if(wh>700){height = '600px'}
    else {height=wh*0.9+'px'}
    return [width,height]
}
