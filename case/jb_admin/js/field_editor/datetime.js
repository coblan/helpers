var lay_datetime={
    props:['row','head'],
    template:`<div class="com-field-datetime">
    <span class="readonly-info" v-show='head.readonly' v-text='row[head.name]'></span>
      <el-date-picker
        v-if="!head.readonly"
      v-model="row[head.name]"
      type="datetime"
      :placeholder="head.placeholder"
      align="right"
      size="small"
      :clearable="can_clear"
      value-format="yyyy-MM-dd HH:mm:ss"
      :picker-options="pickerOptions">
    </el-date-picker>
    <input style="display: none" type="text" :name="head.name" :id="'id_'+head.name" v-model="row[head.name]">
               </div>`,
    //watch:{
    //    row:{
    //        handle(nv){
    //            this.inn_data =this.row[this.head.name]
    //        },
    //        deep:true,
    //    }
    //},
    //methods:{
    //    on_blur(){
    //        this.row[this.head.name] =  this.inn_data
    //    }
    //},
    data(){
        Vue.set(this.row,this.head.name,this.row[this.head.name]||'')
        return {
            //inn_data:this.row[this.head.name],
            pickerOptions: {
                shortcuts: [{
                    text: '今天',
                    onClick(picker) {
                        var d = new Date();
                        d.setHours(0,0,0,0);
                        picker.$emit('pick', d);
                    }
                }, {
                    text: '昨天',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24);
                        date.setHours(0,0,0,0);
                        picker.$emit('pick', date);
                    }
                }, {
                    text: '一周前',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                        date.setHours(0,0,0,0);
                        picker.$emit('pick', date);
                    }
                },{
                    text: '30天前',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 30);
                        date.setHours(0,0,0,0);
                        picker.$emit('pick', date);
                    }
                }]
            },
        }
    },
    mounted:function(){
        var self=this
    },
    computed:{
        can_clear(){
            if(this.head.clearable ==undefined){
                return true
            }else{
                return this.head.clearable
            }
        }
    }
}

Vue.component('com-field-datetime',lay_datetime)
