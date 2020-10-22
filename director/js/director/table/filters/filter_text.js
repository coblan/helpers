require('./styl/filter_text.styl')
var filter_input = {
    props:['head','search_args','config'],
    template:`<div class="com-filter-input">
    <span v-if="head.show_label"><span  v-text="head.label"></span>:</span>

        <el-input class="input-with-select"
                  :placeholder="myplaceholder"
                  @keyup.native.13="parStore.search()"
                  size="small"
                  maxlength="200"
                  v-model="search_args[head.name]">
        </el-input>
        <!--<input @keyup.enter="parStore.search()" type="text" v-model='search_args[head.name]' class="form-control input-sm" :placeholder="myplaceholder">-->
    </div>
    `,
    data:function(){
        var self=this
        return {
            order:this.head.order || false,
            parStore:ex.vueParStore(this)
        }
    },

    computed:{
        myvalue:function(){
            return this.search_args[this.head.name]
        },
        myplaceholder(){
            if(this.head.show_label){
                return this.head.placeholder
            }else{
                return this.head.placeholder ||this.head.label
            }
        }
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)
        },
        options:function(v){
            delete  this.search_args[this.head.name]
        }
    },
    mounted:function(){
        //var parName = ex.vuexParName(this)
        var self=this
        if(this.head.event_slots){
            this.set_event_slot()
        }

    },
    methods:{
        set_event_slot:function(){
            var self=this
            ex.each(this.head.event_slots,function(router){
                if(router.event){
                    self.$on(router.event,function(e){
                        ex.eval(router.express,{event:e,ps:self.parStore,vc:self})
                    })
                }
                if(router.par_event){
                    self.parStore.$on(router.par_event,function(e){
                        ex.eval(router.express,{event:e,ps:self.parStore,vc:self})
                    })
                }

            })
        },

        clear_value:function(){
            delete this.search_args[this.head.name]
        },

    }
}

Vue.component('com-filter-text',filter_input)

