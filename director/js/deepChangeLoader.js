module.exports = function(source) {
    // source 为 compiler 传递给 Loader 的一个文件的原内容
    // 该函数需要返回处理后的内容，这里简单起见，直接把原内容返回了，相当于该 Loader 没有做任何转换
    // console.log('hello -------------------------world')
    // var out_source=source.replaceAll('::v-deep','/deep/')
    var out_source =source. replace(/::v-deep/g ,'/deep/')
    return out_source;
};