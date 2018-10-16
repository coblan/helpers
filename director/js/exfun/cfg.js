window.cfg={
    showMsg:function(msg){
        layer.alert(msg);
    },
    warning:function(msg){
        layer.alert(msg,{title:['提示','color:white;background-color:#f0ad4e'],icon: 5})
    },
    showError:function(msg){
        layer.alert(msg, {icon: 5,title:'错误'});
    },
    tr:{
        'picture_size_excceed':'图片尺寸不能超过{maxsize}'
    },
    show_load:function(){
        this._loader_index = layer.load(1)
    },
    hide_load:function(delay,msg){
        layer.close(this._loader_index)
        if(delay){
            var realMsg = msg || '操作成功'
            layer.msg(realMsg,{time:delay})
        }
    }
}