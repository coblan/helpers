export var notify={
    notify(title,options){
        if (!('Notification' in window)) {
            console.log('This browser does not support notification');
            this._layerNofity(title,options)
        }else if(this._notify_permission==null){
            Notification.requestPermission().then((permission)=> {
                if(permission === 'granted'){
                    console.log('用户允许通知');
                    this._notify_permission='granted'
                    this._notify(title,options)
                }else if(permission === 'denied'){
                    console.log('用户拒绝通知');
                    this._notify_permission='denied'
                    this._layerNofity(title,options)
                }
            });
        }else if(this._notify_permission=="denied"){
            this._layerNofity(title,options)
        }else if(this._notify_permission=='granted'){
            this._notify(title,options)
        }else{
            this._layerNofity(title,options)
        }
    },
    _notify_permission:null,
    _notify(title,options){
        var notification = new Notification(title, options)
        if(options.data && options.data.url){
            notification.onclick = function(){
                notification.close();                              // 并且关闭通知
                location = options.data.url
                //window.open(options.data.url, '_blank');      // 打开网址
                
            }
        }
    },
    _layerNofity(title,options){
        layer.open({
            title: '通知',
            content: title,
            icon:0,
            shade:false,
            offset:'rb',
            yes:function(index,layero){
                layer.close(index)
                if(options.data && options.data.url){
                    location = options.data.url
                }
            },
            end: function () {
                if(options.onclose){
                    options.onclose()
                }
            }
        });
    }

}