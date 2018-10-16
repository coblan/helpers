$.validator.config({
    rules: {
        mobile: [/^1[3-9]\d{9}$/, "请填写有效的手机号"],
        chinese: [/^[\u0391-\uFFE5]+$/, "请填写中文字符"],
        digit: function(element, params) {
            var digits = params[0]
            var pattern = `\\.\\d{${digits}}$`
            return RegExp(pattern).test(element.value) || '请确定有效位数为'+digits;
        }
    }
});