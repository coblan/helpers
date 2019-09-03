
var filter_compare={
    props:['head','search_args'],
    data:function(){
        this.search_args['_'+this.head.name+'_compare'] =  this.search_args['_'+this.head.name+'_compare'] || 0
        return {
        }
    },
    template:`<div  class="com-filter-datetime-range flex flex-ac" :style="{width:head.width}">
                <!--<span v-text="head.label" style="white-space: nowrap"></span>:-->
                   <select name="" id="" class="form-control input-sm" style="width: 50px" v-model="search_args['_'+head.name+'_compare']">
                        <option value="0">=</option>
                         <option value="1">></option>
                         <option value="-1"><</option>
                   </select>
                   <input @keyup.enter="parStore.search()" type="text" v-model='search_args[head.name]' class="form-control input-sm" :placeholder="head.label">
                </div>`,



}

Vue.component('com-filter-compare',filter_compare)