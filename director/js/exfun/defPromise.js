export default  class DefPromise {
    constructor(executor,def_ful) {
        this.has_then=null
        this.promise = new Promise(executor);
        this.def_ful = def_ful
        this.promise = this.promise
            .then((resp)=>{
                if(this.has_then){
                    this.has_then(resp)
                }else{
                    this.def_ful(resp)
                }
            });
    }
    then(onFulfilled, onRejected) {
        this.has_then =onFulfilled
        return this.promise
    }
}