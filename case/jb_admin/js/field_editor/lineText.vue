<template>
    <div class="com-field-linetext" :class="head.class" :style="head.style">
        <div v-if='head.readonly'>
            <span>{{head.prefix}}</span>
            <span class="readonly-info"  v-text='row[head.name]'></span>
            <span>{{head.suffix}}</span>
        </div>
        <div  v-else  class="form-inline test1">
            <slot name="inputbody">
                <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder"
                          :id="'id_'+head.name" :name="head.name"
                          :maxlength="head.maxlength">
                    <template v-slot:prepend >
                        <span  v-if="head.prefix" v-html="head.prefix"></span>
                    </template>
                    <template v-slot:append>
                        <span  v-if="head.suffix" v-html="head.suffix"></span>
                    </template>
                </el-input>
            </slot>

        </div>
    </div>
</template>
<script>
import { ref, reactive,computed ,onMounted,getCurrentInstance } from '@vue/composition-api'
    // const { ref, reactive,computed ,onMounted,getCurrentInstance } = VueCompositionAPI
    // export  class LineTextLogic{
    //     constructor(){
    //
    //     }
    //     getSetup(props){
    //         this.plain_mounted(props)
    //         return {
    //
    //         }
    //     }
    //     plain_mounted(props){
    //         onMounted(()=>{
    //             if(props.head.css){
    //                 ex.append_css(this.head.css)
    //             }
    //             var mounted_express = props.head.mounted_express || props.head.on_mounted
    //             if(mounted_express){
    //                 var vc = getCurrentInstance()
    //                 ex.eval(mounted_express,{vc:vc.proxy})
    //             }
    //         })
    //     }
    // }

export function basic_hook(props){
  var vc = getCurrentInstance()
  onMounted(()=>{
      if(props.head.css){
        ex.append_css(props.head.css)
      }
      var mounted_express = props.head.mounted_express || props.head.on_mounted
      if(mounted_express){
        ex.eval(mounted_express,{vc:vc.proxy})
      }
  })
}

    export default {
        props:['row','head'],
        setup(props){
          basic_hook(props)
          // return new LineTextLogic().getSetup(props)
        }
    }
</script>