<template>
  <div class="com-form-one flex-v" :class="head.inn_class">
      <div class="oprations up" v-if="ops_loc=='up'">
        <component v-for="op in normed_ops" :is="op.editor"  :key="op.name"
                   :ref="'op_'+op.name" :ctx="op" :head="op" @operation="on_operation(op)"></component>
      </div>
      <div style="overflow: auto;position: relative" :class="{ 'box box-default box-mycustom':ops_loc=='up','has-group':fields_group,}"
           class="flex-grow fields-area">
        <!--有分组的情况-->
        <div v-if="fields_group" class="fields-group" >

        <!--  以tab页面的方式显示group分组-->
          <div v-if="ctx.tab_group" style="position: absolute;left: 0;right: 0;bottom: 0;top:0;padding-top: 6px;">
              <el-tabs  tab-position="left" style=" height: 100%;width: 100%;flex-direction: row">
                <el-tab-pane :label="group.label" v-for="group in grouped_heads_bucket">

                  <fieldTableBlock v-if="table_grid " class="compact"
                                          :heads="group.heads" :row="row" :option="{table_grid:table_grid}" :alignLabel="ctx.table_grid_align_label">
                  </fieldTableBlock>


<!--                  <com-fields-table-block v-if="table_grid " class="compact"-->
<!--                                          :heads="group.heads" :row="row" :option="{table_grid:table_grid}" :alignLabel="ctx.table_grid_align_label">-->
<!--                  </com-fields-table-block>-->
                  <div v-else class='field-panel' :class="head.inn_class?'': 'suit'">
                    <field  v-for='head in group.heads' :key="head.name" :head="head" :row='row'></field>
                  </div>
                </el-tab-pane>
              </el-tabs>
          </div>

          <!--  以分块的方式显示group分组-->
          <template v-else  v-for="group in grouped_heads_bucket">
            <div v-if="group.heads && group.heads.length > 0" :class="'group_'+group.name">
              <div style="display: flex;gap: 30px;align-items: center">
                <div class="fields-group-title"  v-html="group.label"></div>
                <div v-if="group.collapse != undefined" @click="groupCollapseSwitch(group)" style="cursor: pointer">
                  <i style="font-size: 120%" v-if="group.collapse" class="el-icon-caret-right"></i>
                  <i style="font-size: 120%" v-if="!group.collapse" class="el-icon-caret-bottom"></i>
                </div>
              </div>
              <div v-show="group.collapse == undefined || !group.collapse">

                <fieldGridBlock v-if="group.grid_class "
                                :class="group.grid_class"
                                 :heads="group.heads"
                                  :css="group.grid_css"
                                  :type="group.grid_type"
                                  :row="row">
                </fieldGridBlock>

                <fieldTableBlock v-else-if="table_grid "
                                        :heads="group.heads" :row="row" :option="{table_grid:table_grid}" :alignLabel="ctx.table_grid_align_label">
                </fieldTableBlock>

<!--                <com-fields-table-block v-if="table_grid "-->
<!--                                        :heads="group.heads" :row="row" :option="{table_grid:table_grid}" :alignLabel="ctx.table_grid_align_label">-->
<!--                </com-fields-table-block>-->
                <div v-else class='field-panel' :class="head.inn_class?'': 'suit'">
                  <field  v-for='head in group.heads' :key="head.name" :head="head" :row='row'></field>
                </div>
              </div>

            </div>
            <component v-show="group.collapse == undefined || !group.collapse"
                       v-if="group.editor" :is="group.editor" :row="row" :ctx="group.editor_ctx"></component>

          </template>




        </div>
<!--        <div v-else-if="ctx.grid_class">-->
          <fieldGridBlock v-else-if="ctx.grid_class "
                          :class="ctx.grid_class"
                          :heads="normed_heads"
                          :css="ctx.grid_css"
                          :type="ctx.grid_type"
                          :row="row">
          </fieldGridBlock>
<!--        </div>-->
        <!--只有table分组-->
        <div v-else-if="table_grid " >
          <fieldTableBlock
              :heads="normed_heads" :row="row" :option="{table_grid:table_grid}" :alignLabel="ctx.table_grid_align_label"></fieldTableBlock>
<!--          <com-fields-table-block-->
<!--              :heads="normed_heads" :row="row" :option="{table_grid:table_grid}" :alignLabel="ctx.table_grid_align_label"></com-fields-table-block>-->
        </div>
        <!--没有分组-->
        <div v-else class='field-panel' :class="head.inn_class?'': 'suit'" id="form" >
          <field  v-for='head in normed_heads' :key="head.name" :head="head" :row='row'></field>
        </div>
      </div>
      <div class="oprations bottom" v-if="ops_loc=='bottom'">
        <component v-for="op in normed_ops" :key="op.name" :is="op.editor"
                   :ref="'op_'+op.name" :head="op" :ctx="op" @operation="on_operation(op)"></component>
      </div>

  </div>
</template>
<script>
/*
*
* 改造form_one.js 还未完成。
* */
import {mix_fields_data} from "../mix/mix_fields_data";
import fieldTableBlock from "./form_one/fieldTableBlock.vue";
import fieldGridBlock from "./form_one/fieldGridBlock.vue";
export default {
    components:{
      fieldTableBlock,
      fieldGridBlock
    },
    props:['ctx'],
    data(){
        if (this.ctx.director_name){
        var def_row = {_director_name:this.ctx.director_name}
        }else{
        var def_row = {}
        }
        if(this.ctx.preset){
        // 弹窗编辑窗时，可以利用preset传入par_row.pk等信息
            ex.vueAssign(def_row,this.ctx.preset)
        }else if(this.ctx.preset_express){
           var resp = ex.eval(this.ctx.preset_express,{vc:this,head:this.ctx})
            ex.vueAssign(def_row,resp)
        }
        var data_row = ex.copy(this.ctx.row  || def_row )
        var self=this
        var childStore = new Vue({
              data:{
                  vc:self,
                  name:'form-one'
                  }
              })
        var parStore = ex.vueParStore(this)
        return {
          head:this.ctx,
          par_row:this.ctx.par_row,
          heads:this.ctx.heads,
          //layout:this.ctx.layout,
          fields_group:this.ctx.fields_group,
          table_grid:this.ctx.table_grid,
          ops:this.ctx.ops,
          errors:{},
          row:data_row,
          org_row:data_row,
          childStore:childStore,
          parStore:parStore,
          ops_loc: this.ctx.ops_loc || 'up',

        }
    },
    mixins:[mix_fields_data,mix_nice_validator],
    mounted(){
        if(this.ctx.css){
          ex.append_css(this.css)
        }
    },
    computed:{
        normed_ops(){
          var last_ops =  ex.filter(this.ops,(op)=>{
            // 兼容老调用
            op.show_express = op.show_express || op.show
            if(op.show_express){
                var rt =  ex.eval(op.show_express,{row:this.row,vc:this})
              return  rt
            }else{
                return true
            }
          })
          return last_ops
        },
    grouped_heads_bucket:function(){
      var out_bucket = []
      ex.each(this.fields_group,(group)=>{
        if(group.show && ! ex.eval(group.show,{row:this.row,head:this.head})){
          return
        }
        var heads = ex.filter(this.normed_heads,function(head){
          return ex.isin(head.name,group.heads)
        })
        var gg = ex.copy(group)
        gg.heads=heads
        out_bucket.push(gg)
        // out_bucket.push({name:group.name,label:group.label,heads:heads,
        //   editor:group.editor,
        //   editor_ctx:group.editor_ctx,
        //   collapse:group.collapse,
        // })
      })
      return out_bucket
      }
    },

    methods:{
      groupCollapseSwitch(group){
        var one = ex.findone(this.fields_group,{name:group.name})
        one.collapse = !group.collapse
        // Vue.set(group,'collapse',!group.collapse)
         // group.collapse= !group.collapse
      },
      group_filter_heads:function(group){
        return ex.filter(this.normed_heads,function(head){
          return ex.isin(head.name,group.heads)
        })
      },
      save(){
        if(this.head.save_express){
          var super_save = ()=>{mix_fields_data.methods.real_save.call(this)}
          return ex.eval(this.head.save_express,{vc:this,super_save:super_save})
        }else{
          return  mix_fields_data.methods.save.call(this)
        }
      }
    }
    // data_getter  回调函数，获取数据,


}

// var get_data={
// get_row:function(self,callback,kws){
// //kws={model_name ,relat_field}
// var director_name = kws.director_name
// var relat_field = kws.relat_field
// var dt = {fun:'get_row',director_name:director_name}
// dt[relat_field] = self.par_row[relat_field]
// //var post_data=[dt]
// cfg.show_load()
// ex.director_call('d.get_row?dname='+director_name,dt).then((resp)=>{
// cfg.hide_load()
// callback(resp)
// })
//
// },
// table_row:function(self,callback,kws){
// callback(self.par_row)
// }
// }

// var after_save={
// update_or_insert:function(self,new_row,kws){
// var old_row= self.old_row
// var parStore = ex.vueParStore(self)
// parStore.update_or_insert(new_row,old_row)
// // 要update_or_insert ，证明一定是 更新了 par_row
// //ex.vueAssign(self.par_row,new_row)
// //self.$emit('tab-event',{name:'update_or_insert',new_row:self.par_row,old_row:old_row})
// },
// // do_nothing:function(self,new_row,kws){
// // },
//
// update_par_row_from_db:function(self,new_row,kws){
// //
// var post_data=[{fun:'get_row',director_name:self.par_row._director_name,pk:self.par_row.pk}]
// ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
// ex.vueAssign(self.par_row,resp.get_row)
// })
// }
// }
</script>

<style scoped lang="scss">
// 为了分组显示好看

//.fields-group{
//  padding: 0 20px;
//}
.fields-group-title{
  padding-left: 10px;
  font-size: 110%;
  font-weight: bold;
}
.oprations.up{
  background-color: white;
  //border-bottom: 1px solid #dadada;
}
//.fields-area{
//  background-color: white;
//}
//
.com-form-one{
  height: 100%;

  .oprations{
    padding: 5px 10px;
  }
  .oprations.bottom{
    text-align: right;
    border-top:1px solid #d7d7d7;
  }

  .table-fields{
    border:1px solid #efefef;
    background-color: #f8f8f8;
    //border-radius: 4px;
    margin:5px 15px;
    padding: 5px 30px;
  }
  .fields-group-title{
    margin: 10px;
  }

  //.field-input-td{
  //  .msg-box.n-right{
  //    position: absolute;
  //    bottom: 0;
  //    left: 0;
  //  }
  //}

 ::v-deep{
   .msg-bottom{
     .msg-box.n-right{
       position: absolute;
       bottom: 0;
       left: 0;
     }
   }
 }

}

.fields-area{
  &.has-group{
    padding: 10px;
  }

}

.box-mycustom{
  border-top-color: #f4f4f4;
}


.plain{
  .field-panel{
    //background-color: #FAFAFA;
    margin: auto;
    padding: 20px 30px;
    position: relative;
    //border: 1px solid #E0E0E0;
    min-width: 600px;

    .form-group.field{
      display: flex;
      align-items: stretch;
      margin-bottom: 0;


    }
  }
  /deep/{
    .control-label{
      width: 180px;
      text-align: right;
      padding: 5px 30px 5px 0;
      z-index: 100;
      flex-shrink: 0;
      //border-top: 1px solid #EEE;
      padding-top: 10px;
    }
    .help-text {
      padding: 13px 3px;
      color: #999;
      font-style: italic;
      font-size: 0.9em;
    }
  }

}

</style>