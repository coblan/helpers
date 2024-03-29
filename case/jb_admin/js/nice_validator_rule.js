$.validator.config({
    rules: {
        mobile: [/^1[3-9]\d{9}$/, "请填写有效的手机号"],
        chinese: [/^[\u0391-\uFFE5]+$/, "请填写中文字符"],
        number:function(element,params){
            if(!element.value){
                return true
            }
            var pattern = `^(\\-|\\+)?\\d+(\\.\\d+)?$`
            return RegExp(pattern).test(element.value) || '请输入数字';
        },
        digit: function(element, params) {
            var digits = params[0]
            var pattern = `\\.\\d{0,${digits}}$|^[\\d]+$`
            return RegExp(pattern).test(element.value) || '请输入有效位数为'+digits+'的数字';
        },
        dot_split_int:function(element,params){
            return /^(\d+[,])*(\d+)$/.test(element.value) || '请输入逗号分隔的整数'
        },
        ip: [/^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})$/i, '请填写有效的 IP 地址'],

        regexp:function(element, param) {
            console.log(param)
            if(param.length==2){
                var exp = new RegExp(param[0])
                var msg = param[1]
            }else{
                var exp = new RegExp(param[0])
                var msg = '不满足规则'
            }
            return exp.test(element.value) || msg
        },
        express:function(element, param) {
            // 举例
            //express = base64.b64encode("parseFloat(scope.value) > 0".encode('utf-8'))
            //msg = base64.b64encode('必须大于0'.encode('utf-8'))
            //head['fv_rule']= 'express(%s , %s)'%( express.decode('utf-8'),msg.decode('utf-8'))

            var real_param = ex.atou(param[0])
            if (param[1]){
                var msg = ex.atou( param[1] )
            }else{
                var msg =  '不满足规则'
            }
            return ex.eval(real_param,{value:element.value,element:element,vld:this}) ||  msg
        },
        myremote:function(element, param){
            // 应该没啥用了，因为和express一样的功能
            var real_param = ex.atou(param[0])
            return ex.eval(real_param,{value:element.value,element:element})
        },

        // com-field-table-list
        key_unique:function(elem, param) {
            //return /^1[3458]\d{9}$/.test($(elem).val()) || '请检查手机号格式';
            var keys = param
            var value = $(elem).val()
            if(!value) return true
            var rows = JSON.parse(value)
            var dc={}
            ex.each(keys,key=>{dc[key]=[]})
            for(var i=0;i<rows.length;i++){
                var row = rows[i]
                for(var j=0;j<keys.length;j++){
                    var key = keys[j]
                    if(ex.isin(row[key],dc[key])){
                        return  key+"重复了"
                    }else{
                        dc[key].push(row[key])
                    }
                }
            }
            return true
        },
        group_unique:function(elem, param) {
            var keys = param
            var value = $(elem).val()
            if(!value) return true
            var rows = JSON.parse(value)
            var ls=[]
            for(var i=0;i<rows.length;i++){
                var row = rows[i]
                var group_value = ''
                ex.each(keys,key=>{
                    group_value+= row[key]
                })
                if(ex.isin(group_value,ls)){
                    return  group_value+"重复了"
                }else{
                    ls.push(group_value)
                }
            }
            return true
        },
    }
});