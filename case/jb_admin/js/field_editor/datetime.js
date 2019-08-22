var lay_datetime={
    props:['row','head'],
    template:`<div class="com-field-datetime">
    <span v-show='head.readonly' v-text='row[head.name]'></span>
      <el-date-picker
        v-if="!head.readonly"
      v-model="row[head.name]"
      type="datetime"
      :placeholder="head.placeholder"
      align="right"
      size="small"
      value-format="yyyy-MM-dd HH:mm:ss"
      :picker-options="pickerOptions">
    </el-date-picker>
    <input style="display: none" type="text" :name="head.name" :id="'id_'+head.name" v-model="row[head.name]">
               </div>`,
    data(){
        return {
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
        //laydate.render({
        //    elem: $(this.$el).find('input')[0], //指定元素
        //    type: 'datetime',
        //    done: function(value, date, endDate){
        //        self.row[self.head.name] = value
        //    }
        //});
    }
}

Vue.component('com-field-datetime',lay_datetime)
