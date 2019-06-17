var group_check = {
    props:['head','disabled'],
    template:` <div class="com-table-op-group-check" style="margin-left: 3px">
    <el-checkbox-group v-model="myvalue" size="small">
      <el-checkbox-button v-for="option in head.options" :label="option.value"  :key="option.value">
        <span v-text="option.label"></span>
      </el-checkbox-button>
    </el-checkbox-group>
    <!--<button :class="norm_class" @click="operation_call()"  :style="head.style" :disabled="disabled">-->
        <!--<i v-if="head.icon" :class='["fa",head.icon]'></i>-->
        <!--<span  v-text="head.label"></span>-->
    <!--</button>-->
    </div>`,
    data:function(){
        var parStore = ex.vueParStore(this)
        return {
            myvalue: this.head.init_value || [],
            enable:true,
            parStore : parStore,
        }
    },
    computed:{
        norm_class:function(){
            if(this.head.class){
                return 'btn btn-sm '+this.head.class
            }else{
                return 'btn btn-sm btn-default'
            }
        }
    },
    watch:{
        myvalue(newvalue,oldvalue){
            ex.eval(this.head.action,{value:newvalue,ps:this.parStore})
        }
    },
    methods:{
        operation_call:function(){
            if (this.head.action) {
                if(this.head.row_match && !this.parStore.check_selected(this.head)){
                    return
                }
                ex.eval(this.head.action, {ps: this.parStore, head: this.head,self:this})
            }else{
                this.$emit('operation',this.head.name || this.head.fun)
            }
        },
        set_enable:function(yes){
            this.enable= yes
        }
    }
}
Vue.component('com-table-op-group-check',group_check)