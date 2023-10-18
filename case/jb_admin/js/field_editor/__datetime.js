var lay_datetime={
    props:['row','head'],
    template:`<div class="com-field-datetime">
    <span class="readonly-info" v-show='head.readonly' v-text='inn_data'></span>
      <el-date-picker
        v-if="!head.readonly"
      v-model= inn_data
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
    //            debugger
    //            this.inn_data =this.row[this.head.name]
    //        },
    //        deep:true,
    //    }
    //},
    watch:{
        out_data(nv){
            this.inn_data = nv
        },
        inn_data(nv){
            this.row[this.head.name] = nv
        }
    },
    //methods:{
    //    on_blur(){
    //        this.row[this.head.name] =  this.inn_data
    //    }
    //},
    data(){
        Vue.set(this.row,this.head.name,this.row[this.head.name]||'')
        return {
            inn_data:this.row[this.head.name],
            pickerOptions: {
                shortcuts: [
                    {
                        text: '当前时间',
                        onClick(picker) {
                            var d = new Date();
                            picker.$emit('pick', d);
                        }
                    },
                    {
                        text: '5分钟前',
                        onClick(picker) {
                            //var d = new Date();
                            var outd = ex.dayjs().subtract(5,'minute')
                            picker.$emit('pick', outd.toDate());
                        }
                    },
                    {
                        text: '15分钟前',
                        onClick(picker) {
                            //var d = new Date();
                            var outd = ex.dayjs().subtract(15,'minute')
                            picker.$emit('pick', outd.toDate());
                        }
                    },
                    {
                        text: '30分钟前',
                        onClick(picker) {
                            var outd = ex.dayjs().subtract(30,'minute')
                            picker.$emit('pick', outd.toDate());
                        }
                    },
                    {
                        text: '1小时前',
                        onClick(picker) {
                            var outd = ex.dayjs().subtract(60,'minute')
                            picker.$emit('pick', outd.toDate() );
                        }
                    },
                    {
                    text: '今天零时',
                    onClick(picker) {
                        var d = new Date();
                        d.setHours(0,0,0,0);
                        picker.$emit('pick', d);
                    }
                },
                 {
                    text: '一周前',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                        date.setHours(0,0,0,0);
                        picker.$emit('pick', date);
                    }
                },{
                        text: '本月初',
                        onClick(picker) {
                            var outd = ex.dayjs().startOf('month')
                            picker.$emit('pick', outd.toDate());
                        }
                  }, {
                        text: '上月当天',
                        onClick(picker) {
                            var outd = ex.dayjs().subtract(1,'month').startOf('day')
                            picker.$emit('pick', outd.toDate());
                        }
                    },
                    {
                        text: '上月初',
                        onClick(picker) {
                            var outd = ex.dayjs().subtract(1,'month').startOf('month')
                            picker.$emit('pick', outd.toDate());
                        }
                    },]
            },
        }
    },
    mounted:function(){
        var self=this
    },
    computed:{
        out_data(){
           return this.row[this.head.name]
        },
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
