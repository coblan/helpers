export var localCatch = {
    sessGet(key,def){
        if( sessionStorage.getItem(key)){
            return JSON.parse(  sessionStorage.getItem(key) )
        }else{
            return def
        }

    },
    sessSet(key,value){
        sessionStorage.setItem(key,JSON.stringify(value))
    },
    localGet(key,def){
        if( localStorage.getItem(key)){
            return JSON.parse(  localStorage.getItem(key) )
        }else{
            return def
        }

    },
    localSet(key,value){
        localStorage.setItem(key,JSON.stringify(value))
    }
}