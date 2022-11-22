<template>
  <div class="myfront">
<!--    <com-form-one :ctx="$attrs.tab_head.fields_ctx"></com-form-one>-->
    <compnent :is="$attrs.tab_head.inn_editor_list[index]" v-bind="$attrs" @finish="onFinish"></compnent>
<!--    <com-tab-form v-bind="$attrs"></com-tab-form>-->
  </div>

</template>
<script>
/*  这个控件未开发完，可以参考$attrs的应用
*   {'name':'account',
                                'label':'账号信息',
                                 'editor':'com-tab-front-page' , #'com-tab-form',
                                 'inn_editor_list':['com-tab-confirm','com-tab-form'],
                                 'confirm_message':'当前员工还问没有账号，是要创建账号吗',
                                 'visible':can_touch(User,self.crt_user),
                                 'mounted_express':'''
                                 cfg.show_load()
                                 ex.director_call('d.get_row',{director_name:'jb_user.edit',pk:scope.vc.par_row.account}).then(resp=>{
                                   cfg.hide_load()
                                   ex.vueAssign(scope.vc.row,resp)
                                   if(!scope.vc.row.first_name){
                                       scope.vc.row.first_name=scope.par_row.name
                                   }
                                 })  ''' ,
                                 'fields_ctx':{
                                     'after_save_express':'scope.vc.par_row.account=scope.row.pk;ex.director_call("d.save_row",{row:scope.vc.par_row})',
                                     **UserFields().get_head_context()}}
*
* */
export default {
  data(){
    return {
      index:0,
    }
  },
  computed:{
      inn_editor_list(){
        return ex.eval( this.$attrs.tab_head.inn_editor_express,{vc:this,par_row:this.$attrs.par_row} )
      }
  },
  methods:{
    onFinish(){
      this.index+=1
      console.log('finish')
      // if(this.$attrs.next_express){
      //   ex.eval(this.$attrs.next_express,{vc:this})
      // }else{
      //   this.index+=1
      // }

    }
  }
}
</script>