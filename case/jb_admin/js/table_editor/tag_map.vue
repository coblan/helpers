<template>
    <div class="com-table-tag-map">
        <el-tag
                :type="mytype"
                effect="dark"
                size = 'mini'
                v-text="mylabel">
        </el-tag>
    </div>
</template>
<script>
    export default {
        props:['rowData','field','index'],
        computed:{
            mytype(){
                if(this.head.class_express){
                    return ex.eval( this.head.class_express,{row:this.rowData}) || 'info'
                }else{
                    return this.head.class_map[ this.rowData[this.field]  ] || 'info'
                }

            },
            mylabel(){
                var option = ex.findone(this.head.options,{value:this.rowData[this.field]})
                if(option){
                  return option.label
                }else{
                  return  this.rowData[this.field]
                }

            }

        },
        created(){
            // find head from parent table
            var table_par = this.$parent
            while (true){
                if (table_par.heads){
                    break
                }
                table_par = table_par.$parent
                if(!table_par){
                    break
                }
            }
            this.table_par = table_par
            this. head  = ex.findone(this.table_par.heads,{name:this.field})
            this.parStore = ex.vueParStore(this)
        },
    }
</script>