var op_a = {
    props:['head','disabled'],
    template:` <div class="com-op-table-refresh" style="display: inline-block;margin: 0 1px 0 3px">
        <select v-model='myvalue' class="form-control input-sm com-filter-select" >
         <option class="fake-placeholder"  value="" v-text='head.label' ></option>
        <option v-for='option in head.options' :value="option.value" v-text='option.label'></option>
    </select>
    </div>`,
    data:function(){
        var parStore = ex.vueParStore(this)
        return {
            myvalue:this.head.init_value || '',
            parStore : parStore,
        }
    },
    computed:{

    },
    watch:{
        myvalue(v){
            debugger
            if(this.interval_index){
                clearInterval(this.interval_index)
            }

            if(v){
                setInterval(()=>{
                    ex.eval(this.head.action,{ps:this.parStore})
                },v)
            }
        },
    },
    methods:{

    }
}
Vue.component('com-op-table-refresh',op_a)