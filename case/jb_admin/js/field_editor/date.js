var lay_datetime={
    props:['row','head'],
    template:`<div class="com-field-date">
        <span class="readonly-info" v-show='head.readonly' v-text='row[head.name]'></span>

     <input v-if="!head.readonly" type="text" style="display: none"
            :id="'id_'+head.name"
            :name="head.name"
            v-model="row[head.name]">
     <el-date-picker
        v-if="!head.readonly"
      v-model="row[head.name]"
      type="date"
      :placeholder="head.placeholder"
      align="right"
      size="small"
      value-format="yyyy-MM-dd"
      :picker-options="pickerOptions">
    </el-date-picker>
</div>`,
    mounted:function(){
        //var self=this
        //laydate.render({
        //    elem: $(this.$el).find('input')[0], //指定元素
        //    type: 'date',
        //    done: function(value, date, endDate){
        //        self.row[self.head.name] = value
        //    }
        //});
    },
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
    }
}

Vue.component('com-field-date',lay_datetime)

//Vue.component('com-field-date',function(resolve,reject){
//    ex.load_js('/static/lib/laydate/laydate.js',function(){
//        resolve(lay_datetime)
//    })
//})