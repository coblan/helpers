require('./scss/filter_single_select2.scss')

var com_select = {
    props: ['head', 'search_args'],
    template: `<div class="com-filter-single-select2">
        <com-field-single-select2 ref="select2" :head="head" :row="search_args"></com-field-single-select2>
    </div>
    `,
    data:function(){
        var self=this
        return {
            order:this.head.order || false,
            parStore:ex.vueParStore(this),
            options:this.head.options || [],
        }
    },
    watch:{
        options(v){
            this.$refs.select2.inn_options = v
        }
    },
    mounted:function(){
        var self=this
        if(this.head.event_slots){
            ex.vueEventRout(self)
        }
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this})
        }
    },
    methods:{
        get_options:function({post_data={}}){
            var self=this
            ex.director_call(this.head.director_name,post_data,function(resp){
                self.head.options = resp
            })
        },
        clear_value:function(){
            Vue.delete(this.search_args,this.head.name)
            //this.$refs.select2.setValue(undefined)
            //delete this.search_args[this.head.name]
        },
    }
}


Vue.component('com-filter-single-select2',com_select)