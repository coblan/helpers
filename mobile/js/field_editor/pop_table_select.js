require('./styl/pop_table_select.styl')

Vue.component('com-field-pop-table-select',{
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
            this.head.table_ctx.title = '选择'+this.head.label
            this.head.table_ctx.par_row= this.row
            live_root.open_live('live_list',this.head.table_ctx)
            //cfg.pop_big('com-field-pop-search',{table_ctx:this.head.table_ctx,placeholder:this.head.search_placeholder,par_row:this.row})
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

Vue.component('com-field-pop-search',{
    props:['ctx'],
    template:`<div class="com-field-pop-search">
    <form action="/">
          <van-search
            v-model="childStore.search_args._q"
            :placeholder="this.ctx.placeholder || '请输入搜索关键词'"
            show-action
            @search="onSearch"
            @cancel="onCancel"
          >
          <div slot="left-icon" @click="onSearch">
            <van-icon name="search" />
          </div>
          </van-search>
    </form>
    <!--<van-search-->
    <!--v-model="childStore.search_args._q"-->
    <!--:placeholder="this.ctx.placeholder || '请输入搜索关键词'"-->
    <!--show-action-->
    <!--@search="onSearch"-->
    <!--@cancel="onCancel"-->
  <!--&gt;-->
   <!--<div slot="action" @click="onSearch">搜索</div>-->
  <!--</van-search>-->
  <com-ctn-scroll-table :ctx="ctx.table_ctx"> </com-ctn-scroll-table>

    </div>`,
    data(){
        var childStore = new Vue(table_store)
        childStore.rows=[]
        childStore.vc = this
        childStore.director_name = this.ctx.table_ctx.director_name
        childStore.par_row = this.ctx.par_row,
        childStore.search_args = {_q:''}
        return {
            childStore:childStore,
        }
    },
    methods:{
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
})
