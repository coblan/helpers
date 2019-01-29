require('./scss/multi_chosen.scss')

var multi_chosen={
    props:['value','options'],
    template:`<select  multiple="multiple" class="multi-chosen form-control" data-placeholder="请选择">
    <option v-for="option in options" :value="option.value" v-text="option.label"></option>
</select>`,
    mounted:function(){
        this.install()
    },
    watch:{
        value:function(nv){
            this.setValue(nv)
        },
        options:function(nv){
            this.install()
        }
    },
    methods:{
        install:function(){
            var self=this
            ex.load_css(cfg.js_lib.chosen_css)
            ex.load_js(cfg.js_lib.chosen).then(function(){
                $(self.$el).chosen({
                    search_contains:true,
                    display_selected_options:false,
                }).change(function(event){
                    self.$emit('input',$(this).val())
                });
                self.setValue(self.value)
                $(self.$el).siblings('.chosen-container').removeAttr('style')
            })
        },
        setValue:function(val){
            $(this.$el).val(val);
            $(this.$el).trigger("chosen:updated");
        }
    }
}

Vue.component('multi-chosen',multi_chosen)