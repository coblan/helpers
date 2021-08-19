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
            ref="dtable"
    >
      <!--            :extend-logic="extendLogic"-->

    </director_table>
</template>
<script>
    import  director_table,{DTableLogic} from  './director_table.vue'
    const { ref, reactive,computed ,onMounted,getCurrentInstance } = VueCompositionAPI

    // class DTable2Logic extends DTableLogic{
    //     getSetup(props){
    //         // const vc = getCurrentInstance()
    //         // onMounted(()=>{
    //         //     if(vc.proxy.tableRows.length==0){
    //         //         vc.proxy.search()
    //         //     }
    //         // })
    //         return {
    //
    //         }
    //     }
    // }

//     class BackendTable{
//         getSetup(props){
//             this. dtable = ref(null)
//             this.connect_dtable_event()
//             return {
//                 dtable:this.dtable,
// //                extendLogic:DTable2Logic,
//             }
//         }
//         connect_dtable_event(){
//             const vc = getCurrentInstance()
//             onMounted(()=>{
//                 this.dtable.value.childStore.$on('finish',(data)=>{
//                     vc.emit('finish',data)
//                 })
//             })
//         }
//
//     }
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
        mounted(){
          if(!this.ctx.rows || this.ctx.rows.length==0){
              this.$refs.dtable.search()
          }
          this.$refs.dtable.childStore.$on('finish',(data)=>{
              this.emit('finish',data)
          })
        }
    }
</script>