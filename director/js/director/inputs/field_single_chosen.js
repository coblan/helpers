require('./scss/field_single_chosen.scss')

var field_sigle_chosen={
    props:['row','head'],
    template:`<select  class="chosen field-single-chosen form-control" :style="head.style" :data-placeholder="head.placeholder" >
         <option  :value="null" ></option>
        <option v-for="option in order_options" :value="option.value" v-text="option.label"></option>
    </select>`,
    mounted:function(){
        var self=this
        ex.load_css('https://cdn.bootcss.com/chosen/1.8.2/chosen.min.css')
        ex.load_js('https://cdn.bootcss.com/chosen/1.8.2/chosen.jquery.min.js',function(){
            $(self.$el).chosen({
                search_contains:true,
                allow_single_deselect: true,
            }).change(function(event){
                //self.$emit('input',$(this).val())
               self.row[self.head.name]= $(this).val()
            });
            self.setValue(self.value)
        })
    },
    watch:{
        value:function(nv){
            this.setValue(nv)
        }
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
            $(this.$el).val(val);
            $(this.$el).trigger("chosen:updated");
        }
    }
}

Vue.component('com-field-single-chosen',field_sigle_chosen)