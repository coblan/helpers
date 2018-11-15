
var field_sigle_chosen={
    props:['row','head'],
    template:`<div  :style="head.style">
    <select  class="select2 field-single-select2 form-control" >
         <option  :value="undefined" ></option>
        <option v-for="option in order_options" :value="option.value" v-text="option.label"></option>
    </select>
    </div>`,
    mounted:function(){
        var self=this
        ex.load_css('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/css/select2.min.css')
        ex.load_js('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js',function(){

            $(self.$el).find('select').select2({
                placeholder:self.head.placeholder,
                allowClear: true
            })
            self.setValue(self.value)
            $(self.$el).find('.select2').change(function(e) {
                var value = $(self.$el).find('.select2').val( )
                if(value ==''){
                    Vue.delete(self.row,self.head.name)
                }else{
                    Vue.set(self.row,self.head.name,value)
                }

            })

        })

    },
    watch:{
        //value:function(nv){
        //    this.setValue(nv)
        //}
    },
    computed:{
        order_options:function(){
            if (this.head.order){
                return ex.sortOrder(this.head.options,'label')
            }else{
                return this.head.options
            }
        }
    },
    methods:{
        setValue:function(val){
            $(this.$el).find('.select2').val(val);
            $(this.$el).find('.select2').trigger('change');
            Vue.set(this.row,this.head.name,val)
        }
    }
}

Vue.component('com-field-single-select2',field_sigle_chosen)