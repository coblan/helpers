require('./scss/com_search_select.scss')

var com_search = {
    props:['head','search_args'],
    data:function(){
        if(! this.search_args._q){
            Vue.set(this.search_args,'_q','')
        }
        return {

        }
    },
    mounted:function(){
        Vue.set(this.search_args,'qf',1)
    },
    template:`<div class="search-select">
    <!--<input style="max-width: 20em;min-width: 10em;"-->
             <!--type="text"-->
             <!--name="_q"-->
             <!--v-model='search_args._q'-->
             <!--:placeholder='head.search_tip'-->
             <!--@keyup.13="$emit('submit')"-->
             <!--class='form-control input-sm'/>-->
             <el-input class="input-with-select"
                placeholder="请输入内容"
                prefix-icon="el-icon-search"
                size="small"
                v-model="search_args._q">
                 <!--<el-select v-model="search_args.qf" slot="append" placeholder="请选择">-->
                      <!--<el-option label="餐厅名" value="1"></el-option>-->
                      <!--<el-option label="订单号" value="2"></el-option>-->
                      <!--<el-option label="用户电话" value="3"></el-option>-->
                <!--</el-select>-->

                   <el-dropdown trigger="click" slot="append" @command="handleCommand">
                      <span class="el-dropdown-link">
                        <i class="el-icon-arrow-down el-icon--right"></i>
                      </span>
                      <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item @click="set_value(1)" :class="{'active':search_args._qf==1}">黄金糕</el-dropdown-item>
                        <el-dropdown-item>狮子头</el-dropdown-item>
                        <el-dropdown-item>螺蛳粉</el-dropdown-item>
                        <el-dropdown-item>双皮奶</el-dropdown-item>
                        <el-dropdown-item>蚵仔煎</el-dropdown-item>
                      </el-dropdown-menu>
                    </el-dropdown>
              </el-input>
    </div> `,
    methods:{
        set_value:function(v){
            this.search_args._qf=v
        }
    }
}
Vue.component('com-search-select',com_search)