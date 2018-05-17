export var code ={
    //hashCode:function (str){
    //    var str =btoa(str)
    //    var h = 0, off = 0;
    //    var len = str.length;
    //    for(var i = 0; i < len; i++){
    //        h = 31 * h + str.charCodeAt(off++);
    //    }
    //    var t=-2147483648*2;
    //    while(h>2147483647){
    //        h+=t
    //    }
    //    return h;
    //}

    hashDict:function(dc){
        var ls =[]
        for(var k in dc){
            if(k.startsWith('_')){
                continue
            }
            if($.isFunction(dc[k])){
                continue
            }
            ls.push(k)
        }
        ls = ls.sort()
        var lsl = []
        for(var i = 0 ;i<ls.length;i++){
            lsl.push(ls[i]+':'+dc[ls[i]])
        }
        var dc_str = lsl.join(';')
        return md5(dc_str)

    },
    //hashCode: function (input){
    //    var I64BIT_TABLE =
    //        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-'.split('');
    //    var hash = 5381;
    //    var i = input.length - 1;
    //
    //    if(typeof input == 'string'){
    //        for (; i > -1; i--)
    //            hash += (hash << 5) + input.charCodeAt(i);
    //    }
    //    else{
    //        for (; i > -1; i--)
    //            hash += (hash << 5) + input[i];
    //    }
    //    var value = hash & 0x7FFFFFFF;
    //
    //    var retValue = '';
    //    do{
    //        retValue += I64BIT_TABLE[value & 0x3F];
    //    }
    //    while(value >>= 6);
    //
    //    return retValue;
    //}
}