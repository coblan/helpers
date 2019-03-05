require('./scss/switch.scss')

Vue.component('com-op-switch',{
    props:['head'],
    data:function(){
        return {
            myvalue:false
        }
    },
    template:`<div class="com-op-switch">
    <span v-text="head.label"></span>
    <el-switch @click.native="trig_switch()"
      v-model="myvalue"
      :active-color="head.active_color || '#13ce66'"
      inactive-color="#888">
    </el-switch>
    </div>`,
    methods:{
        trig_switch:function(){
            var self=this
            if(this.head.op_confirm_msg){
                var mymsg = ex.eval(this.head.op_confirm_msg,{value:this.myvalue})
                layer.confirm(mymsg, {icon: 3, title:'提示',closeBtn :0}, function(index){
                    layer.close(index);
                    self.do_switch()
                },function(){
                    self.myvalue = !self.myvalue
                });
            }else{
                self.do_switch()
            }
        },
        do_switch:function(){
            this.head.value=this.myvalue
            this.$emit('operation',this.head.name)
        }
        //operation_call:function(){
        //    this.$emit('operation',this.head.name)
        //},
    }
})