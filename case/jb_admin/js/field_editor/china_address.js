var china_address_logic={
    props:['row','head'],
    template:`<div class="com-field-china-address">
            <el-cascader
              :options="options"
              v-model="row[head.name]"></el-cascader>
               </div>`,
    mounted:function(){

    },
    data:function(){
        return {
            options:china_address
        }
    }
}

Vue.component('com-field-china-address',function(resolve,reject){
    ex.load_js('/static/lib/china_address.js',function(){
        resolve(china_address_logic)
    })
})