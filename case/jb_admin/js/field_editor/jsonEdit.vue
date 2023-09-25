<template>
  <div class="com-field-json-edit">
    <div class="editor" style="width: 600px; height: 400px;"></div>
  </div>
</template>
<script>
export default {
  props:['row','head'],
  data(){
      return {
        inn_value:this.row[this.head.name]
      }
  },
  mounted(){
    this.initData()
    var par = ex.vueParStore(this)
    par.vc.before_submit.push(this.updateData )
  },
  computed:{
      out_value(){
        return this.row[this.head.name]
      }
  },
  watch:{
    out_value(nv){
        this.inn_value = this.row[this.head.name]
        this.updateEditorData()
    }
  },
  methods:{
    initData(){
      var self = this
      ex.load_css(cfg.js_lib.jsoneditor_css)
      ex.load_js(cfg.js_lib.jsoneditor).then(()=>{
        if(self.head.readonly){
          var options = {
            mode: 'view',
            // modes: ['code', 'form', 'text', 'tree', 'view', 'preview']
            modes: [ 'view', 'preview']
          }
        }else{
          var options = {
            mode: 'code',
            // modes: ['code', 'form', 'text', 'tree', 'view', 'preview']
            modes: ['code', 'form', 'tree', 'view', 'preview']
          }
        }

        var value =  this.inn_value  //this.row[this.head.name]

        this. editor = new JSONEditor(this.$el.querySelector('.editor'), options)

        // set json
        if(!value){
          var initialJson = ex.eval(this.head.default_value_express,{vc:this})  || {}
        } else if(typeof value =='string'){
          var initialJson = JSON.parse(this.row[this.head.name])
        }else{
          var initialJson = value
        }

        this.editor.set(initialJson)

        // get json
        // const updatedJson = editor.get()
      })
    },
    updateEditorData(){
      var value =  this.inn_value  //this.row[this.head.name]

      if(!value){
        var initialJson = ex.eval(this.head.default_value_express,{vc:this})  || {}
      } else if(typeof value =='string'){
        var initialJson = JSON.parse(this.row[this.head.name])
      }else{
        var initialJson = value
      }

      this.editor.set(initialJson)
    },
    updateData(){
      this.row[this.head.name] = JSON.stringify( this.editor.get() )
    }
  }
}
</script>
<style scoped lang="scss">
::v-deep{
  .jsoneditor-menu a.jsoneditor-poweredBy{
    display: none;
  }
}
</style>
