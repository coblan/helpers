export var  vuetool = {
    vueSuper:function(self,kws){
        var mixin =kws.mixin
        var name=kws.fun
        var args = kws.args || []
        if (mixin){
            var index = self.$options.mixins .indexOf(mixin)
        }else{
            var index = self.$options.mixins.length
        }
        for(var i=index-1 ;i> -1;i--){
            var mix = self.$options.mixins[i]
            if(mix[name]){
                return mix.apply(self,args)
            }
        }
    },
    vueBroadCall:function(self,fun,kws){
        var rt =[]
        cusBroadCall(self,fun,kws,rt)
        return rt
    }
}

function cusBroadCall(self,fun,kws,rt){
    if(! self.$children){return}
    for(var i =0;i<self.$children.length;i++){
        var child =self.$children[i]
        if(child[fun]){
            rt.push(child[fun](kws))
        }
        cusBroadCall(child,fun,kws,rt)
    }
}