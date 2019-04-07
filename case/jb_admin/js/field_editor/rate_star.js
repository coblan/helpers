Vue.component('com-field-rate-star',{
    props:['row','head'],
    template:`<div class="com-">
     <el-rate
        v-model="row[head.name]"
        :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
      </el-rate>
    </div>`
})