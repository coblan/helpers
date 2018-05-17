var ele_transfer={
    props:['row','head'],
    template:`<div>
     <el-transfer v-model="value1" :data="trans_data"></el-transfer>
     </div>`,
    data:function(){
        return {
            value1:[]
        }
    },
    computed:{
        trans_data:function(){
            return [{key:'xx',label:'bbbb'}]
        }
    }
}
Vue.component('com-field-ele-transfer',ele_transfer)