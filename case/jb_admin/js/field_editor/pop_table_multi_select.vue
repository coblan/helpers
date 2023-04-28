<template>
    <div class="com-field-pop-table-multi-select">

        <input type="text" v-model="row[head.name]" style="display: none;" :id="'id_'+head.name" :name="head.name">

        <div style="display: flex;flex-wrap: wrap;gap:5px;">
          <el-tag v-for="(label,index) in labels" :closable=" can_clear" v-if="row[head.name]" @close="clear(index)">
            <span  v-text="label"></span>
          </el-tag>

          <el-button v-if="!head.readonly" @click="open_win" size="mini" type="success" icon="el-icon-plus"></el-button>
        </div>




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
        data(){
          var labels = []
          if(this.row['_'+this.head.name+'_label']){
            labels = this.row['_'+this.head.name+'_label'] //.split(',')
          }
          var inn_data = []
          if(this.head.format=='string'){
              inn_data = this.row[this.head.name].split(',')
          }
            return {
                labels:labels,
                inn_data:inn_data,
            }
        },
        computed:{
            // labels:function(){
            //     return this.row['_'+this.head.name+'_label']
            // },
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
                cfg.pop_vue_com( 'com-backend-table', this.head.table_ctx).then(rows=>{
                    if(rows.length==0){
                      console.log('break table panel')
                      return
                    }
                if(self.head.after_select_express){
                    ex.eval(self.head.after_select_express,{selected_row:rows,row:self.row})

                }else{
                    // var list =  this.row[this.head.name] || []
                  ex.each(rows,(row)=>{
                    if(! ex.isin(row.pk, this.inn_data)){
                      this.inn_data.push(row.pk)
                      this.labels.push(row._label)

                    }
                  })
                  this.syncData()


//                    Vue.set(self.row,self.head.name,foreign_row.pk)
                }
//                Vue.set(self.row,'_'+self.head.name+'_label',foreign_row._label)
            }).catch(()=>{
                    console.log('break table panel')
            })

            },
          syncData(){
            if(this.head.format=='string'){
              this.row[this.head.name] = this.inn_data.join(',')
            }else{
              this.row[this.head.name] = this.inn_data
            }
            this.row['_'+this.head.name+'_label'] = this.labels //.join(',')
          }
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
