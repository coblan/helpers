var lay_datetime={
    props:['row','head'],
    template:`<div><span v-show='head.readonly' v-text='row[head.name]'></span>
                    <input class="form-control input-sm" v-show="!head.readonly" type="text" :id="'id_'+head.name" v-model="row[head.name]"  :placeholder="head.placeholder || '选择月份'" readonly>

               </div>`,
    mounted:function(){
        var self=this
        laydate.render({
            elem: $(this.$el).find('input')[0], //指定元素
            type: 'month',
            done: function(value, date, endDate){
                self.row[self.head.name] = value
            }
        });
    }
}

Vue.component('com-field-month',function(resolve,reject){
    ex.load_js('/static/lib/laydate/laydate.js',function(){
        resolve(lay_datetime)
    })
})