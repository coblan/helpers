require('./styl/tree_select.styl')

Vue.component('com-field-tree-select',{
    props:['head','row'],
    template:`<van-field class="com-field-pop-table-select"  v-model="label_text" :required="head.required"
    :label="head.label"
    type="text"
    :placeholder="normed_placeholder"
    :name="head.name"
    autosize
    :error-message="head.error"
    @click="open_win"
    readonly
  >
  </van-field>`,
    mounted:function(){
        this.setup_validate_msg_router()
    },
    computed:{
        label_text(){
            return this.row['_'+this.head.name+'_label']
        },
        normed_placeholder:function(){
            if(! this.head.readonly){
                return this.head.placeholder || '请输入'+this.head.label
            }else{
                return ''
            }
        }
    },
    methods:{
        open_win(){
            //cfg.pop_big('com-field-tree-shower',{title:this.head.title,
            //    table_ctx:this.head.table_ctx,
            //    placeholder:this.head.search_placeholder,
            //    par_row:this.row,
            //    parent_click:this.head.parent_click
            //})
            live_root.open_live('live_field_tree_shower',{title:this.head.title,
                        table_ctx:this.head.table_ctx,
                        placeholder:this.head.search_placeholder,
                        par_row:this.row,
                        parent_click:this.head.parent_click
                    })
        },
        setup_validate_msg_router(){
            if(!this.head.validate_showError){
                Vue.set(this.head,'error','')
                this.head.validate_showError="scope.head.error=scope.msg"
            }
            if(!this.head.validate_clearError){
                this.head.validate_clearError="scope.head.error=''"
            }
        }
    }
})

window.live_field_tree_shower = {
    props:['ctx'],
    basename:'live-field-tree-shower',
    template:`<div class="com-field-tree-shower">
    <com-uis-nav-bar :title="ctx.title" :back="true" ></com-uis-nav-bar>
 <div class="path">
    <span class="parent-node clickable" v-for="par in childStore.parents" v-text="par.label" @click="on_par_click(par)"></span>
 </div>
  <com-ctn-scroll-table :ctx="ctx.table_ctx"> </com-ctn-scroll-table>
    </div>`,
    data(){
        var childStore = new Vue(table_store)
        childStore.rows=[]
        childStore.vc = this
        childStore.director_name = this.ctx.table_ctx.director_name
        childStore.par_row = this.ctx.par_row,
            childStore.search_args = {}
        return {
            childStore:childStore,
        }
    },
    mounted(){
        this.search()
    },
    methods:{
        search(){
            this.childStore.search().then(res=>{
                cfg.hide_load()
            })
        },
        on_par_click(par){
            ex.eval(this.ctx.table_ctx.option.parent_click,{parent:par,head:this.ctx,ps:this.childStore})
        },
        onSearch(){
            cfg.show_load()
            this.childStore.search().then(res=>{
                cfg.hide_load()
            })

        },
        onCancel(){
            history.back()
        }
    }
}
