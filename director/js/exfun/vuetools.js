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
            var methods = mix.methods[name]
            if(methods){
                return methods.apply(self,args)
            }
        }
    },
    vueBroadCall:function(self,fun,kws){
        var rt =[]
        cusBroadCall(self,fun,kws,rt)
        return rt
    },
    vueParCall:function(self,fun,kws){
        var rt =[]
        cusParCall(self,fun,kws,rt)
        return rt
    },
    vueExtend:function(par,mixins){
        var mixins = ex.map(mixins,function(item){
            if(typeof item =='string'){
                return window[item]
            }else{
                return item
            }
        })

        var real_par = $.extend({}, par);
        var orgin_mixins = real_par.mixins
        delete real_par.mixins
        if (orgin_mixins){
            var list = orgin_mixins
        }else{
            var list=[]
        }
        list.push(real_par)
        list=list.concat(mixins)
        var final_obj = list[list.length-1]
        final_obj.mixins=list.slice(0,list.length-1)
        return final_obj
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
function cusParCall(self,fun,kws,rt){
    if(! self.$parent){return}
    var par =self.$parent
    if(par[fun]){
        rt.push(par[fun](kws))
    }
    cusParCall(par,fun,kws,rt)

    //for(var i =0;i<self.$parent.length;i++){
    //    var par =self.$parent[i]
    //    if(par[fun]){
    //        rt.push(par[fun](kws))
    //    }
    //    cusParCall(par,fun,kws,rt)
    //}
}