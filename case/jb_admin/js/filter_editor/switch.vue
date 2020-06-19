<template>
    <div class='com-filter-switch'>
        <label style="font-weight: 400" :for="'filter_'+head.name" v-text="head.label"></label>
        <input :id="'filter_'+head.name" type="checkbox" v-model="search_args[head.name]">
    </div>
</template>

var filter_check = {
props:['head','search_args','config'],
template:``,
data:function(){
var self=this
return {
order:this.head.order || false,
parStore:ex.vueParStore(this)
}
},

computed:{
myvalue(){
return this.search_args[this.head.name]
},
options:function(){
}
},
watch:{
myvalue:function(v){
this.$emit('input',v)
},
options:function(v){
delete  this.search_args[this.head.name]
}
},
mounted:function(){
if(this.head.event_slots){
this.set_event_slot()
}

},
methods:{

}
}
Vue.component('com-filter-check',filter_check)

