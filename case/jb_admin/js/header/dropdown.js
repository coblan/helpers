require('./scss/dropdown.scss')


Vue.component('com-head-dropdown',{
    props:['head'],
    template:`<div class="com-head-userinfo">
    <div style="z-index:200" class="login" >
        <el-dropdown class="com-head-userinfo">
          <span class="el-dropdown-link">
          <span v-html="head.label"></span>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-for="action in head.options">
                <a class="com-head-dropdown-action" :href="action.url" v-text="action.label"></a>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
    </div>
    </div>`
})