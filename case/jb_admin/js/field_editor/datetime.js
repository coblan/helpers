var lay_datetime={
    props:['row','head'],
    template:`<div><span v-show='head.readonly' v-text='row[head.name]'></span>

                    <input v-show="!head.readonly" type="text" :id="'id_'+head.name" v-model="row[head.name]"  :placeholder="head.placeholder" readonly>

               </div>`,
    mounted:function(){
        var self=this
        laydate.render({
            elem: $(this.$el).find('input')[0], //指定元素
            type: 'datetime',
            done: function(value, date, endDate){
                self.row[self.head.name] = value
            }
        });
    }
}

Vue.component('com-field-datetime',function(resolve,reject){
    ex.load_js('/static/lib/laydate/laydate.js',function(){
        resolve(lay_datetime)
    })
})