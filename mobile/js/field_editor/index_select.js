require('./scss/index_select.scss')

Vue.component('com-field-index-select',{
    props:['row','head'],
    template:`<div class="com-field-index-select">
    <input type="text" :name="head.name" v-model="row[head.name]" style="display: none">
    <input  type="text" @click="open_panel()"  v-model="mylabel" readonly>
    </div>`,
    data:function(){
        return {
            parStore:ex.vueParStore(this),
        }
    },
    mounted:function(){
        var self=this
        ex.vueEventRout(this)
        Vue.nextTick(function(){
            self.$emit('on-mount')
        })
        var crt_value = this.row[this.head.name]
        if(crt_value ){
            Vue.nextTick(function(){
                self.$emit('init-value',crt_value)
            })

        }
    },
    computed:{
        mylabel:function(){
            var crt_value = this.row[this.head.name]
            if(crt_value){
                for(var i=0;i<this.head.bucket_list.length;i++){
                    var bucket = this.head.bucket_list[i]
                    var one = ex.findone(bucket.items,{value:crt_value})
                    if(one){
                        return one.label
                    }
                }
            }else{
                return ''
            }
        }
    },
    methods:{
        update_options:function(data){
            var self=this
           ex.director_call(this.head.director_name,data,function(resp){
               self.head.bucket_list=resp
           })
        },
        open_panel:function(){
            var self=this
            var ctx={
                title:this.head.label,
                item_editor:this.head.item_editor,
                bucket_list:this.head.bucket_list,
            }
            // cfg.show_cloak()
            // setTimeout(()=>{
            //     cfg.hide_cloak()
            // },1000)

            cfg.show_load()
            setTimeout(()=>{
                cfg.hide_load()
            },1500)

            var  win_close = cfg.pop_big('com-index-select',ctx,function(resp){
                Vue.set(self.row,self.head.name,resp.value)
                win_close()
                self.$emit('input',resp.value)
            })

        }
    }
})

Vue.component('com-index-select',{
    props:['ctx'],
    template:`<div class="com-index-select">
     <mt-index-list>
      <mt-index-section v-for="bucket in ctx.bucket_list" :index="bucket.index">
        <component v-for="item in bucket.items" :is="ctx.item_editor" :ctx="item" @click.native="select_this(item)"></component>
      </mt-index-section>
    </mt-index-list>
    </div>`,
    methods:{
        select_this:function(event){
            this.$emit('finish',event)
        }
    }
})
