require('./scss/com_search_select.scss')

var com_search = {
    props:['head','search_args'],
    data:function(){
        debugger
        if(! this.search_args._q){
            Vue.set(this.search_args,'_q','')
        }
        if(!this.search_args._qf){
            Vue.set(this.search_args,'_qf',this.head.options[0].value)
        }
        return {
            myvalue:this.search_args._q
        }
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
                :placeholder="normed_placeholder"
                @keyup.native.13="$emit('submit')"
                size="small"
                maxlength="200"
                v-model="myvalue">
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
                        <!--<el-dropdown-item command="1"><span :class="{'active-search-item':isActive(1)}">黄金糕</span></el-dropdown-item>-->
                        <el-dropdown-item v-for="opt in head.options" :command="opt.value"><span :class="{'active-search-item':isActive(opt.value)}" v-text="opt.label"></span></el-dropdown-item>

                      </el-dropdown-menu>
                    </el-dropdown>
              </el-input>
    </div> `,
    watch:{
        myvalue(v){
            this.search_args._q = v
        },
        org_value(v){
            if(this.myvalue != v){
                this.myvalue = v
            }
        }
    },
    computed:{
        normed_placeholder:function(){
            var crt = ex.findone(this.head.options,{value:this.search_args._qf})
            return crt.label
        },
        org_value(){
            return this.search_args._q
        }
    },
    methods:{
        handleCommand:function(cmd){
            Vue.set(this.search_args,'_qf',cmd)
        },
        //set_value:function(v){
        //    this.search_args._qf=v
        //},
        isActive:function(v){
            return this.search_args._qf==v
        }
    }
}
Vue.component('com-search-select',com_search)