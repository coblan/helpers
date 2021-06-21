<template>
    <int-input class="com-field-number" :head="head" :row="row" :extend-logic="extend_logic"></int-input>
</template>
<script>
    import intInput ,{IntInputLogic} from './int.vue'

  export  class NumberLogic extends IntInputLogic{
          constructor(){
              super()
              this.fv_rule=null
          }
            setup(props){
                return {
                    extend_logic:super.setup(props)
                }
            }
            isNumber(evt){
                evt = (evt) ? evt : window.event;
                var charCode = (evt.which) ? evt.which : evt.keyCode;
                if ((charCode >= 48 && charCode <= 57) || charCode== 46 || charCode== 45) {
                    if(charCode==46 && this.row[this.head.name].indexOf('.')!=-1){
                        return evt.preventDefault();
                    }else{
                        return true
                    }
                }else{
                    return evt.preventDefault();
                }
            }
    }
    export default {
        props:['row','head'],
        components:{
            intInput
        },
        setup(props){
            return new NumberLogic().setup(props)
        }
    }
</script>

