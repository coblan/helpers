require('./styl/split_text.styl')

var line_text={
    props:['row','head'],
    template:`<div :class="['com-field-split-text',head.class]" :style="head.style">
            			<span class="readonly-info" v-if='head.readonly' v-text='row[head.name]'></span>
            			<input v-else type="text" :class="['my-input-field',head.input_class]" v-model="row[head.name]"
            		 	    :id="'id_'+head.name" :name="head.name"
                        	:placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>
                       </div>`,
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
        var self=this

        setTimeout(()=>{

            //var value = self.row[self.head.name]
            //
            //if (value){
            //    var items =   value.split(',') //ex.map(value.split(','),ii=>{ return {label:ii} })
            //}else{
            //    var items = []
            //}
            //var options = self.head.options .concat(items)
            var bb = $(this.$el).find('.my-input-field').selectize({
                delimiter: this.head.splitter ||  ',',
                persist: false,
                create: true,
                //items:items,
                //create: function(input) {
                //    return {
                //        value: input,
                //        text: input
                //    }
                //},
                //create: function(input) {
                //    return {
                //        label: input,
                //    }
                //},
                hideSelected:true,
                valueField: 'value',
                labelField:'label',
                searchField:'label',
                //options:  self.head.options ||  [], //options,// items ,//
                onChange:function(value){
                    self.row[self.head.name] = value
                },
                onBlur:function(){
                    $(self.$el).find('.my-input-field').trigger('validate')
                }
            });
            Vue.nextTick(()=>{
                //ex.each(items,(ii)=>{
                //    bb[0].selectize.removeOption(ii)
                //})
                //bb[0].selectize.clearOptions()
                if(self.head.options){
                    bb[0].selectize.addOption(self.head.options)
                }

                //bb[0].selectize.setValue(items, true)
            })

        },100)



    }
}

Vue.component('com-field-split-text',function(resovle,reject){
    ex.load_css(js_config.js_lib.selectizejs_css)
    ex.load_js(js_config.js_lib.selectizejs).then(()=>{
        resovle(line_text)
    })
})