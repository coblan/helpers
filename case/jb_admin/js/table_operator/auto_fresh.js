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
            timeout_index:0,
        }
    },
    computed:{

    },
    watch:{
        myvalue(v){
            if(v){
                this.start_refresh()
            }else{
                if(this.timeout_index){
                    clearTimeout(this.timeout_index)
                }
            }
            //if(this.interval_index){
            //    clearInterval(this.interval_index)
            //}
            //
            //if(v){
            //    this.interval_index = setInterval(()=>{
            //        ex.eval(this.head.action_express,{ps:this.parStore})
            //    },v)
            //}
        },
    },
    methods:{
         start_refresh(){
            if(this.myvalue){
               this.timeout_index =  setTimeout(()=>{
                     ex.eval(this.head.action_express,{ps:this.parStore}).then(()=>{
                         this.start_refresh()
                     })

                },this.myvalue)
            }
        }
    }
}
Vue.component('com-op-table-refresh',op_a)