//rabbit={{ rabbit | jsonify }}
export var rabbit={
    /*
     ctx={
        url:'ws://localhost:15674/ws',
        user:'guest',
        pswd:'guest',
    }
    * */
    rabbit_regist:function(ctx){
    var p =new Promise(function(resolve,reject) {
            ex.load_js(js_config.js_lib.stompjs, function () {
                // Stomp.js boilerplate
                //var client = Stomp.client('ws://' + rabbit.url + ':15674/ws');
                var client = Stomp.client(ctx.url);
//        client.debug = pipe('#second');

//        var print_first = pipe('#first', function(data) {
//            client.send('/topic/test', {"content-type":"text/plain"}, data);
//        });
                var on_connect = function (x) {
//          id = client.subscribe("/topic/test", function(d) {
//               print_first(d.body);
//          });

                    //id = client.subscribe("/exchange/zhaoxiang_weilan_warning", function(d) {
                    //    layer.alert(d.body)
                    //
                    //    console.log(d.body)
                    //});
                    resolve(client)

                };
                var on_error = function (e) {
                    console.log('error');
                    console.log(e)

                    setTimeout(function () {
                        client = Stomp.client(ctx.url);
                        client.connect(ctx.user, ctx.pswd, on_connect, on_error, '/');
                    }, 10000)

                };
                client.connect(ctx.user, ctx.pswd, on_connect, on_error, '/');
            })
        })
        return p
    },
    stompInit(ctx){
        ex.load_js(js_config.js_lib.stompjs, ()=> {
            this._stomp_client = Stomp.client(ctx.url);
            var on_connect = (x)=> {
                //gb.toast("websocket 链接成功")
                ex.each(this._lstool_list,(lstool)=>{
                    lstool.peekListen()
                })

            };

            var on_error =  (e)=> {
                console.log(e)
                ex.each(this._lstool_list,(lstool)=>{
                    lstool.cacheListened()
                })
                setTimeout( ()=> {
                    this._stomp_client = Stomp.client(ctx.url);
                    this._stomp_client.connect(ctx.user, ctx.pswd, on_connect, on_error, '/');
                }, 10000)
            };
            this._stomp_client.connect(ctx.user, ctx.pswd, on_connect, on_error, '/');
        })
    },
    _stomp_client:null,
    _lstool_list:[],
    stompListen(url,callback){
        var lstool = new ListenTool(this, ele => {
            return this._stomp_client.subscribe(url, callback);
        });
        lstool.addListen(url)
        this._lstool_list.push(lstool)
    }
}


class ListenTool {
    constructor(par, sub_fun) {
        this.needListen = [];
        this.listened = [];
        this.sub_fun = sub_fun;
        this.par = par;
        this.listenedSocket = {};
    }
    addListen(ele) {
        // ele的核心作用是标识该 订阅对象， 以便在初始，出错重连等情况下的 排队，
        if (ex.isin(ele, this.listened) || ex.isin(ele, this.needListen)) {
            this.listened.push(ele);
        } else {
            this.needListen.push(ele);
            this.peekListen();
        }
    }
    peekListen() {
        if (!this.needListen || !this.par._stomp_client || !this.par._stomp_client.connected) {
            return;
        }
        let self = this;
        this.needListen.forEach(ele => {
            this.listened.push(ele);
            if (!this.listenedSocket[ele]) {
                this.listenedSocket[ele] = this.sub_fun(ele);
            }
        });
        this.needListen = [];
    }
    unListen(ele) {
        if (gb.is_in(ele, this.listened)) {
            gb.removeOne(this.listened, ele);
        } else {
            gb.removeOne(this.needListen);
        }
        if (
            !gb.is_in(ele, this.listened) &&
            !gb.is_in(ele, this.needListen) &&
            this.listenedSocket[ele]
        ) {
            this.listenedSocket[ele].unsubscribe();
            delete this.listenedSocket[ele];
        }
    }
    cacheListened() {
        if (this.listened.length > 0) {
            this.needListen = this.needListen.concat(this.listened);
            this.listened = [];
        }
        this.listenedSocket = {};
    }

}



