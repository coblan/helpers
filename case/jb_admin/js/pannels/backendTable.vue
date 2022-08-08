<template>
    <director_table
            :filter-heads='ctx.row_filters'
            :table-rows="ctx.rows"
            :table-heads="ctx.heads"
            :row-sort="ctx.row_sort"
            :row-pages="ctx.row_pages"
            :advise-heads="ctx.advise_heads"
            :advise-heads-cookie-path="ctx.advise_heads_cookie_path"
            :director-name="ctx.director_name"
            :operation-heads="ctx.ops"
            :footer="ctx.footer"
            :parents="ctx.parents"
            :search-args="ctx.search_args"
            :selectable="ctx.selectable"
            :hasPagination="ctx.hasPagination"
            :tableClass="ctx.tableClass"
            :autoHeight="ctx.autoHeight"
            :fitWidth="ctx.fitWidth"
            :opMergeCount="ctx.opMergeCount"
            ref="dtable"
    >

      <template v-slot:default="slotprops">
        <slot v-bind:rows="slotprops.rows"></slot>
      </template>


    </director_table>
</template>
<script>
    import  director_table from  './director_table.vue'
    export default {
        components:{
            director_table,
        },
        props:['ctx'],
        data(){
            return {

                // extendLogic:DTable2Logic
            }
        },
        // setup(props){
        //     debugger
        //     return new BackendTable().getSetup(props)
        // },
      computed:{
        proxy(){
          var self = this
          return new Proxy(this.$refs.dtable,{
            get: function(obj, prop) {
              if(prop in self){
                return  self[prop]
              }else if(prop in obj){
                return  obj[prop]
              }else if(obj.proxy){
                return  obj.proxy[prop]
              }
            }
          })
        }
      },
        mounted(){
          if(this.ctx.autoLoad!=false){
            if(!this.ctx.rows || this.ctx.rows.length==0){
              this.$refs.dtable.search()
            }
          }

          this.$refs.dtable.childStore.$on('finish',(data)=>{
              this.$emit('finish',data)
          })
        },
      methods:{
          search(){
            this.$refs.dtable.search()
          }
      }
    }
</script>