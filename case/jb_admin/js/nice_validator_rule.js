$.validator.config({
    rules: {
        mobile: [/^1[3-9]\d{9}$/, "请填写有效的手机号"],
        chinese: [/^[\u0391-\uFFE5]+$/, "请填写中文字符"],
        digit: function(element, params) {
            var digits = params[0]
            var pattern = `\\.\\d{0,${digits}}$|^[\\d]+$`
            return RegExp(pattern).test(element.value) || '请输入有效位数为'+digits+'的数字';
        },
        dot_split_int:function(element,params){
            return /^(\d+[,])*(\d+)$/.test(element.value) || '请输入逗号分隔的整数'
        },
        ip: [/^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})$/i, '请填写有效的 IP 地址'],

    }
});