Vue.component('com-field-linetext',{
    props:['head','row'],
    template:`<van-field class="com-field-linetext"  v-model="row[head.name]" :required="head.required"
    :label="head.label"
    type="text"
    :placeholder="normed_placeholder"
    :name="head.name"
    autosize
    :error-message="head.error"
    :readonly="head.readonly"
  >
    <!--<template slot="left-icon">-->
        <!--<input v-model="row[head.name]" type="text" :name="head.name" style="display: none">-->
    <!--</template>-->

  </van-field>`,
    mounted:function(){
        if(!this.head.validate_showError){
            Vue.set(this.head,'error','')
            this.head.validate_showError="scope.head.error=scope.msg"
        }
        if(!this.head.validate_clearError){
            this.head.validate_clearError="scope.head.error=''"
        }
    },
    computed:{
        normed_placeholder:function(){
            if(! this.head.readonly){
                return this.head.placeholder || '请选择'+this.head.label
            }else{
                return ''
            }
        }
    },
    methods:{

    }
})

