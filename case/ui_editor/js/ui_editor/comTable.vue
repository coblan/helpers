<template>
  <div class="flex">
    <com-backend-table  style="width: 300px"  ref="mytable" :ctx="tableCtx"></com-backend-table>
    <div>
      内容
    </div>
  </div>

<!--  <div>-->
<!--    hello-->
<!--  </div>-->
</template>
<script>
export default {
    data(){
      return {
        tableCtx:{
          autoHeight:true,
          hasPagination:false,
          autoLoad:false,
          heads:[
            {name:'com',label:'组件',editor:'com-table-span'},
            {name:'keword',label:'关键字',editor:'com-table-span'},

          ],
          rows:[],
          row_filters:[
            {name:'com',label:'送',editor:'com-filter-text'}
          ],
          search_args:{},
          row_sort:{sortable:'',sort_str:''},
          row_pages:{},
          ops:[],
          selectable:false,
          option:{},
        }
      }
    }
}
</script>