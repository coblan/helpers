
export default  {
    props:['head','search_args'],
    data:function(){
        this.search_args['_'+this.head.name+'_compare'] =  this.search_args['_'+this.head.name+'_compare'] || '0'
        return {
            // comparetype:this.search_args['_'+this.head.name+'_compare'] || '0',
            inn_value :this.search_args[this.head.name] || ''
        }
    },
    template:`<div  class="com-filter-datetime-range flex flex-ac" :style="{width:head.width}">
                <!--<span v-text="head.label" style="white-space: nowrap"></span>:-->
                   <select name="" id="" class="form-control input-sm" style="width: 50px" v-model="search_args['_'+head.name+'_compare']">
                        <option value="0">=</option>
                         <option value="1">≥</option>
                         <option value="-1">≤</option>
                   </select>
                   <input @keyup.enter="parStore.search()" type="text" v-model='inn_value' class="form-control input-sm" :placeholder="head.label">
                </div>`,
    watch:{
        inn_value(nv){
            // var compare_name = '_'+this.head.name+'_compare'
            if(nv){
                this.$set(this.search_args,this.head.name,nv)
                // this.$set(this.search_args,compare_name,this.comparetype)
            }else{
                Vue.delete(this.search_args,this.head.name)
                // Vue.delete(this.search_args,compare_name)
            }
        },
        out_value(nv){
            if(nv){
                this.inn_value = nv
            }else{
                this.inn_value = ''
            }
        }
    },
    computed:{
        out_value(){
            return this.search_args[this.head.name]
        }
    }



}