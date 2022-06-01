<template>
  <div class="editor-tree">
    <div>
      <button @click="add">增加</button>
      <button @click="save">保存</button>
    </div>
    <div>
      <el-tree :data="heads"
               :props="defaultProps"
               @node-click="handleNodeClick">

         <span class="custom-tree-node" slot-scope="{ node, data }">
             <div class="item-pannel">
               <div>
                  <span>{{ data.label }}</span>
                  <span style="font-size: 80%;color: lightgray">{{data.editor}}</span>
               </div>


                  <div class="my-buttons">
                       <el-button
                           type="text"
                           size="mini"
                           @click="popEdit(data)">
                        编辑
                      </el-button>

                      <el-button
                          type="text"
                          size="mini"
                          @click="() => append(data)">
                        Append
                      </el-button>
                      <el-button
                          type="text"
                          size="mini"
                          @click="() => remove(node, data)">
                        Delete
                      </el-button>
                </div>
            </div>

        </span>
      </el-tree>

      <div v-for="head in heads">
        {{head.editor}}
      </div>
    </div>
  </div>
</template>
<script>
import ex from 'weblib/ex'
export default {
  props:{
    bus:{},
    heads: {}
  },
  data(){
    return {
      defaultProps: {
        children: 'children',
        label: 'editor'
      },
      coms_options:[],
    }
  },
  mounted(){
    this.getComponents()
  },
  methods:{
    async popEdit(data){
      var fields = [
        {name:'label',label:'名称',editor:'com-field-linetext'},
      ]
      fields = fields.concat(cfg.ui_editor[data.editor].fields)
      var fields_ctx = {
        heads:fields,
        row:{label:data.label, ... data.bind},
        ops:[
          {'editor':'com-btn','label':'确定',
            'click_express':'scope.ps.vc.beforeSubmit().then(()=>{  if(scope.ps.vc.isValid()){ scope.ps.vc.$emit("finish",scope.ps.vc.row)}  })'},

        ],
        genVc:self
      }
      var resp = await cfg.pop_vue_com('com-form-one',fields_ctx)
      Vue.set(data,'label',resp.label)
      // data.label = resp.label
      delete resp.label
      data.bind=resp

    },
    handleNodeClick(){

    },
     save(){
      this.$emit('save')
    },
    async getComponents(){
      // var resp = await ex.director_get('uieditor/components/all')
      // this.coms_options=resp
      
      for(var k in cfg.ui_editor){
        this.coms_options.push({value:k,label:k})
      }

    },
    async add(){

      var fields_ctx = {
        heads:[
          {name:'editor',label:'组件',editor:'com-field-select',options:this.coms_options,required:true},
          {name:'label',label:'名称',editor:'com-field-linetext',required:true},
        ],
        row:{},
        ops:[
          {name:'save',label:'确定',editor:'com-btn',click_express:'scope.ps.vc.beforeSubmit().then(()=>{  if(scope.ps.vc.isValid()){var vc= scope.ps.vc;vc.$emit("finish",vc.row)}  })  '},
        ],
      }
      var resp = await cfg.pop_vue_com('com-form-one',fields_ctx)
      debugger
      this.heads.push(
          {editor:resp.editor,label:resp.label,bind:{} }
      )
    }
  }
}
</script>
<style scoped lang="scss">
.editor-tree{
  min-width: 150px;
  background-color: white;
  height: 100%;
}
.item-pannel{
  position: relative;
  display: flex;
  align-items: center;
  padding: 5px;
  border-top:1px solid lightgray;
  .my-buttons{
    //position: absolute;
    //top:0;
    //right: 0;
    display: none;
  }
  &:hover{
    .my-buttons{
      display: block;
    }
  }
}
</style>