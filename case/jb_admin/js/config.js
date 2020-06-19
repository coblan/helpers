ex.assign(cfg,{
    fields_editor:'com-suit-fields',
    fields_local_editor:'com-suit-fields-local',
    outdate_confirm(title,refresh,force_save){
        layer.confirm(title, {
            icon:3,
            title:'数据过期',
            btn: ['刷新数据', '强制保存', ] //可以无限个按钮

        }, function(index, layero){
            refresh()
            layer.close(index)
        }, function(index){
            force_save()
            layer.close(index)
        });
    }

})