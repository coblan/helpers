require('./scss/search.scss')

Vue.component('com-op-search',{
    props:['head'],
    data:function(){
        return {
            myvalue:'',
            parStore:ex.vueParStore(this)
        }
    },
    template:`<div class="com-op-search">
         <template v-if="head.btn_text">
          <input type="text" :placeholder="head.label" v-model="myvalue"> <button  @click="operation_call()" v-text="head.btn_text"></button>
         </template>
         <input v-else type="text" :placeholder="head.label" v-model="myvalue" :key="operation_call()">
    </div>`,

    methods:{
        operation_call:function(){
            let head = ex.copy( this.head )
            head.value = this.myvalue
            this.$emit('operation',head)
        },

    }
})

