require('./fields_panel.styl')

Vue.component('com-fields-panel',{
    props:['ctx'],
    data:function(){
        var childStore = new Vue({})
        childStore.vc = this
        var row = this.ctx.row?ex.copy(this.ctx.row):{}
        return {
            head:this.ctx,
            childStore:childStore,
            parStore:ex.vueParStore(this),
            heads:this.ctx.heads,
            par_row:this.ctx.par_row, // 外面的row 缓存起来
            row:row,
            ops:this.ctx.ops || [],
            fields_group:this.ctx.fields_group || [],
        }
    },
    mixins:[mix_fields_data,mix_nice_validator],
    template:`<div class="com-fileds-panel">

    <template v-if="fields_group.length > 0">
      <van-cell-group  v-for="group in grouped_heads_bucket" :title="group.label " >
            <component v-for="head in group.heads" :is="head.editor" :head="head" :row="row"></component>
        </van-cell-group>
    </template>
    <template v-else>
     <van-cell-group   >
        <component v-for="head in normed_heads" :is="head.editor" :head="head" :row="row"></component>
    </van-cell-group>
    </template>


    <div style="height: .6rem">
    </div>
    <van-cell-group v-if="ops.length>0" class="ops">
     <div v-for="op in normed_ops" class="op-wrap">
       <component :is="op.editor" :ctx="op"></component>
       </div>
    </van-cell-group>
    </div>`,
    mounted(){
        this.$on('finish',(row)=>{
            if(this.ctx.row){
                ex.vueAssign(this.ctx.row,row)
            }
        })
    },
    computed:{
        grouped_heads_bucket:function(){
            var out_bucket = []
            ex.each(this.fields_group,(group)=>{
                var heads = ex.filter(this.normed_heads,function(head){
                    return ex.isin(head.name,group.heads)
                })
                out_bucket.push({name:group.name,label:group.label,heads:heads})
            })
            return out_bucket
        }
    }
})