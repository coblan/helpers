export var utile = {
    /**
     * 复制内容到粘贴板
     * content : 需要复制的内容
     * message : 复制完后的提示，不传则默认提示"复制成功"
     */
     copyToClip (content) {
        var aux = document.createElement("input");
        aux.setAttribute("value", content);
        document.body.appendChild(aux);
        aux.select();
        document.execCommand("copy");
        document.body.removeChild(aux);
        return new Promise((resovle,reject)=>{
                resovle()
        })
        //if (message == null) {
        //    alert("复制成功");
        //} else{
        //    alert(message);
        //}
    }
}