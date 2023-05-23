ex.assign(cfg,{
    fields_editor:'com-suit-fields',
    fields_local_editor:'com-suit-fields-local',
    outdate_confirm(title,refresh,force_save,{can_overwrite=false}={}){
        if(can_overwrite){
            layer.confirm(title, {
                icon:3,
                title:'数据过期',
                btn: ['刷新数据', '强制保存', ] //可以无限个按钮

            }, async function(index, layero){
                await  refresh()
                layer.close(index)
            }, function(index){
                force_save()
                layer.close(index)
            });
        }else{
            layer.confirm(title, {
                icon:3,
                title:'数据过期',
                btn: ['刷新数据',  ] //可以无限个按钮

            }, async function(index, layero){
                await  refresh()
                layer.close(index)
            },);

        }

    }

})