require('./styl/multi_select2.styl')

var field_multi_chosen={
    props:['row','head'],
    data(){
      return {
          inn_value:this.row[this.head.name]
      }
    },
    template:`<div class="com-field-multi-select2"  :style="head.style">
    <!--<span v-if="head.readonly" v-text="label_text" ></span>-->
    <div v-if="head.readonly">
      <el-tag v-for="label in label_list" v-text="label" size="mini"></el-tag>
    </div>
    <input type="text" :name="head.name" style="display: none" v-model="row[head.name]">
    <div v-show="!head.readonly">
        <select multiple="multiple"  class="select2 field-multi-select2 form-control" :id="'id_'+head.name">
             <option  :value="undefined" ></option>
            <option v-for="option in order_options" :value="option.value" v-text="option.label"></option>
        </select>
    </div>

    </div>`,
    mounted:function(){
        var self=this
        //ex.load_css('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/css/select2.min.css')
        //ex.load_js('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js',function(){
        ex.load_css(js_config.js_lib.select2_css)
        ex.load_js(js_config.js_lib.select2,function(){

            $(self.$el).find('select').select2({
                placeholder:self.head.placeholder || '请选择',
                //allowClear: true
            })
            self.setDomValue(self.row[self.head.name])
            $(self.$el).find('.select2').change(function(e) {
                var value = $(self.$el).find('.select2').val( )
                value = value.filter((item)=>{
                    return item != ""
                })
                self.inn_value = value

            })

        })

    },
    watch:{
        value:function(nv){
            this.setDomValue(nv)
        },
        inn_value(value,oldvalue){
            if(JSON.stringify(value) == JSON.stringify(oldvalue)){
                return
            }
            if(value ==''){
                Vue.delete(this.row,this.head.name)
            }else{
                Vue.set(this.row,this.head.name,value)
            }
        }
    },
    computed:{
        value:function(){
            return this.row[this.head.name]
        },
        label_list(){
            if(this.row[this.head.name]){
                var label_list = ex.map(this.row[this.head.name],(item)=>{
                    return ex.findone(this.head.options,{value:item}).label
                })
                return label_list
            }else{
                return []
            }
        },
        label_text:function(){
            if(this.row[this.head.name]){
                debugger
                var label_list = ex.map(this.row[this.head.name],(item)=>{
                    debugger
                    return ex.findone(this.head.options,{value:item}).label
                })
                return label_list.join(';')
            }else{
                return '---'
            }


            //var opt = ex.findone(this.head.options,{value:this.row[this.head.name]})
            //if(opt){
            //    return opt.label
            //}else{
            //    return ''
            //}
        },
        order_options:function(){
            if (this.head.order){
                return ex.sortOrder(this.head.options,'label')
            }else{
                return this.head.options
            }
        }
    },
    methods:{
        setDomValue:function(val){
            $(this.$el).find('.select2').val(val);
            $(this.$el).find('.select2').trigger('change');
            //Vue.set(this.row,this.head.name,val)
        }
    }
}

Vue.component('com-field-multi-select2',field_multi_chosen)