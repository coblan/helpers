<template>
  <div class="com-field-banner">
    <div v-html="row[head.name]"></div>
  </div>
</template>
<script>
    export default {
        props:['head','row'],
//        methods:{
//            on_blur(){
//                if(this.inn_data || this.inn_data==0){
//                    this.row[this.head.name] = parseInt(this.inn_data)
//                }else{
//                    this.row[this.head.name] = ''
//                }
//            }
//        }
    }
</script>