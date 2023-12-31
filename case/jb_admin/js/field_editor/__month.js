var lay_datetime={
    props:['row','head'],
    template:`<div class="com-field-month">
     <input style="display: none" type="text"
     :id="'id_'+head.name" v-model="row[head.name]"
     :name="head.name">
   <el-date-picker
      v-model="row[head.name]"
      type="month"
      :readonly="head.readonly"
      size="small"
      value-format="yyyy-MM"
      :placeholder="head.placeholder || '选择月份'">
    </el-date-picker>

               </div>`,
    mounted:function(){
        //var self=this
        //laydate.render({
        //    elem: $(this.$el).find('input')[0], //指定元素
        //    type: 'month',
        //    done: function(value, date, endDate){
        //        self.row[self.head.name] = value
        //    }
        //});
    }
}

Vue.component('com-field-month',lay_datetime)

//Vue.component('com-field-month',function(resolve,reject){
//    ex.load_js('/static/lib/laydate/laydate.js',function(){
//        resolve(lay_datetime)
//    })
//})