var ele_transfer={
    props:['row','head'],
    template:`<div class="com-field-ele-transfer" :class="head.class">
     <el-transfer v-model="row[head.name]" :data="head.options"
     :props="{
      key: 'value',
    }"
     :filterable="head.searchable"
    :filter-method="filterMethod"
     :titles="['可选项','已选项']"></el-transfer>
     </div>`,
    data:function(){
        return {
            value1:[]
        }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    },
    computed:{
        filterMethod(query, item){
            if(item){
                return item.label.index(query) > -1
            }

        }
    }
}
Vue.component('com-field-ele-transfer',ele_transfer)