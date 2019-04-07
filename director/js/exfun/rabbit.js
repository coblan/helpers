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
            ex.load_js('https://cdn.bootcss.com/stomp.js/2.3.2/stomp.min.js', function () {
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

    }
}



