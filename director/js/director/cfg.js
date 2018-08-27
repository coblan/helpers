window.cfg={
    showMsg:function(msg){
        layer.alert(msg);
    },
    warning:function(msg){
        layer.confirm(msg,{title:['警告','color:white;background-color:red']})
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