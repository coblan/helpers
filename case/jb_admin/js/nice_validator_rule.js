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
            var exp = new RegExp(param)
            return exp.test(element.value) || '不满足规则'
        },
        express:function(element, param) {
            var real_param = ex.atou(param[0])
            if (param[1]){
                var msg = ex.atou( param[1] )
            }else{
                var msg =  '不满足规则'
            }
            return ex.eval(real_param,{value:element.value}) ||  msg
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