
var time_field={
    props:['row','head'],
    template:`<div :class="['com-field-time','field-'+head.name,head.class]" >
        <input v-if="!head.readonly" type="text" style="display: none"
            :id="'id_'+head.name"
            :name="head.name"
            v-model="row[head.name]">

            	  <el-time-picker
                    v-model="row[head.name]"
                    value-format="HH:mm:ss"
                    size="small"
                    :placeholder="head.placeholder || '请输入时间'">
                   </el-time-picker>
              </div>`,
    computed:{
      innvalue(){
          return this.row[this.head.name]
      }
    },
    watch:{
       innvalue(v){
           if(v.length > 10){
               this.row[this.head.name] = v.slice(11)
           }else{
               this.row[this.head.name] = v
           }
       }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
        if(this.head.width){
            var width = this.head.width
            var myclass ='.com-field-time.field-'+this.head.name
            ex.append_css(`${myclass} input{width:${width} !important;`)
        }
    },
}
Vue.component('com-field-time',time_field)