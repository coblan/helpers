require('./scss/field_single_chosen.scss')

var field_sigle_chosen={
    props:['row','head'],
    template:`<div  :style="head.style">
    <select  class="chosen field-single-chosen form-control"
        :data-placeholder="head.placeholder" >
         <option  :value="undefined" ></option>
        <option v-for="option in order_options" :value="option.value" v-text="option.label"></option>
    </select>
    </div>`,
    mounted:function(){
        var self=this
        ex.load_css(cfg.js_lib.chosen_css)
        ex.load_js(cfg.js_lib.chosen,function(){
            $(self.$el).find('select').chosen({
                search_contains:true,
                allow_single_deselect: true,
                width:'100%',
            }).change(function(event){
                //self.$emit('input',$(this).val())
                if($(this).val() == ''){
                    delete self.row[self.head.name]
                }else{
                    self.row[self.head.name]= $(this).val()
                }
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