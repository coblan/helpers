<template>
    <div class="com-field-pop-table-multi-select">

        <input type="text" v-model="row[head.name]" style="display: none;" :id="'id_'+head.name" :name="head.name">

        <el-tag v-for="(label,index) in labels" :closable=" can_clear" v-if="row[head.name]" @close="clear(index)">
            <span  v-text="label"></span>
        </el-tag>

      <el-button v-if="!head.readonly" @click="open_win" size="mini" type="success" icon="el-icon-plus"></el-button>

<!--        <span v-if="!head.readonly" class="clickable" @click="open_win">-->
<!--&lt;!&ndash;          <i class="fa fa-search"></i>&ndash;&gt;-->
<!--          <i type="primary" class="el-icon-circle-plus clickable"  style="padding: 10px;"></i>-->
<!--&lt;!&ndash;          <el-button type="success"  size="mini" icon="el-icon-plus"></el-button>&ndash;&gt;-->
<!--        </span>-->
        <!--<span v-if="show_search" class="clickable" @click="open_win"><i class="fa fa-search"></i></span>-->
    </div>
</template>
<script>
    export default {
        props:['row','head'],
        computed:{
            labels:function(){
                return this.row['_'+this.head.name+'_label']
            },
            can_clear(){
                if(this.head.readonly){
                    return false
                }
                if(this.head.clearable==undefined){
                    return true
                }else{
                    return this.head.clearable
                }
            },
            show_search(){
                if(this.head.readonly){
                    return false
                }else if(this.head.clearable==false ){
                    return true
                }else{
                    return !Boolean(this.row[this.head.name])
                }
            }
        },
        mounted:function(){
//            if(! this.row[this.head.name]){
//                this.row[this.head.name] = []
//                this.row['_'+this.head.name+'_label'] = []
//            }

        },
        methods:{
            clear(index){
                if(this.head.clear_express){
                    ex.eval(this.head.clear_express,{head:this.head,row:this.row,index:index})
                }else{
                    this.row[this.head.name].splice(index,1)
                    this.row['_'+this.head.name+'_label'].splice(index,1)
//                    Vue.delete(this.row,this.head.name)
//                    Vue.delete(this.row,'_'+this.head.name+'_label')
                }
            },
            open_win:function(){
                var self=this
                if(this.head.init_express){
                    ex.eval(this.head.init_express,{head:this.head,row:this.row})
                }
                // 用到的时候，替换成 com-backend-table    //,com-table-panel
                cfg.pop_vue_com( 'com-backend-table', this.head.table_ctx).then(foreign_row=>{
                    if(!foreign_row){
                    console.log('break table panel')
                    return
                }



                if(self.head.after_select){
                    ex.eval(self.head.after_select,{selected_row:foreign_row,row:self.row})
                }else{
                    var list =  this.row[this.head.name]
                    if(! ex.isin(foreign_row.pk, list)){
                        this.row[this.head.name].push(foreign_row.pk)
                        this.row['_'+this.head.name+'_label'].push(foreign_row._label)
                    }

//                    Vue.set(self.row,self.head.name,foreign_row.pk)
                }
//                Vue.set(self.row,'_'+self.head.name+'_label',foreign_row._label)
            }).catch(()=>{
                    console.log('break table panel')
            })

            },
        }
    }
</script>

<style scoped lang="scss">
/deep/ {
  .el-button--mini{
    padding: 7px;
  }
}
</style>
