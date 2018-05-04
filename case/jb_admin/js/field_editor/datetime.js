var lay_datetime={
    props:['row','head'],
    template:`<div><span v-if='head.readonly' v-text='row[head.name]'></span>
                    <input type="text" :id="'id_'+head.name" v-model="row[head.name]"  :placeholder="head.placeholder">
            			<!--<datetime  v-model="row[head.name]" :id="'id_'+head.name"-->
                        	<!--:placeholder="head.placeholder"></datetime>-->
               </div>`,
    mounted:function(){
        laydate.render({
            elem: $(this.$el).find('input')[0], //指定元素
            type: 'datetime'
        });
    }
}

Vue.component('com-field-datetime',function(resolve,reject){
    ex.load_js('/static/lib/laydate/laydate.js',function(){
        resolve(lay_datetime)
    })
})