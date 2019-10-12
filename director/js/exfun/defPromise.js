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


export default  class DefPromise {
    constructor(executor) {
        this.has_then=false
        this.promise = new Promise(executor);
    }
    then(resolve_handler) {
        this.has_then =true
        return this.promise.then(resolve_handler)
    }
}