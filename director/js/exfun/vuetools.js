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
    }
}