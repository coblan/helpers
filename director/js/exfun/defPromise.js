//export default  class DefPromise {
//    constructor(executor,def_ful) {
//        this.has_then=null
//        this.promise = new Promise(executor);
//        this.def_ful = def_ful
//        this.promise = this.promise
//            .then((resp)=>{
//                if(this.has_then){
//                    this.has_then(resp)
//                }else{
//                    this.def_ful(resp)
//                }
//            });
//    }
//    then(onFulfilled, onRejected) {
//        this.has_then =onFulfilled
//        return this.promise
//    }
//}

/*
* 1. 判断是否有then
*  var p = new DefPromise(resovle,reject=>{
*     if(p.has_then) do_something
*     else do_other
*  }).then()
*
*
* 2. 分拆promise使用
*  var p1 = new DefPromise()
*  p1.resolve()
*
*  Promise.all(p1).then()
* */
export default  class DefPromise {
    constructor(executor) {
        this.has_then=false
        if(!executor){
            this.promise = new Promise((resolve,reject)=>{
                this.cache_resolve = resolve
            })
        }else{
            this.promise = new Promise(executor);
        }

    }
    then(resolve_handler) {
        this.has_then =true
        return this.promise.then(resolve_handler)
    }
    resolve(resp){
        this.cache_resolve(resp)
    }
}