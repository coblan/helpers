/*
 与 extra_click的区别是
 1. 可以添加多个按钮
 2. 根据filter返回不同的按钮
 * */


var extra_click_plus={
    props:['rowData','field','index'],
    template:`<div><span v-for="(ope,index) in operations">
                <span class="clickable" v-text="ope.label" @click="on_click(ope)"></span><span v-if="index< operations.length-1">/</span>  </span>
                </div>`,
    created:function(){
        // find head from parent table
        var table_par = this.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        this.table_par = table_par
        this. head  = ex.findone(this.table_par.heads,{name:this.field})
    },

    computed:{
        operations:function(){
            if(this.head.filter){
                var filter_fun=window[this.head.filter]
                return filter_fun(this.head,this.rowData)
            }else{
                return this.head.operations
            }
        }
    },

    methods:{
        on_click:function(ope){
            this.$emit('on-custom-comp',{name:ope.fun,row:this.rowData,head:this.head})
        }

    }
}

Vue.component('com-table-extraclick-plus',extra_click_plus)
