require('./scss/select.scss')
import {mix_editor} from  './mix_editor.js'

var select = {
        props:['rowData','field','index'],
        template:`<div :class="['com-table-select',{'dirty':is_dirty}]">
            <el-dropdown trigger="click" placement="bottom" @command="handleCommand">
                <span class="el-dropdown-link clickable" v-html="show_label"></span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item v-for="op in head.options"
                    :command="op.value"
                    :class="{'crt-value':rowData[field]==op.value}" >
                    <div v-text="op.label"></div>
                    </el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>

    `,
        data:function(){
            return {
            }
        },
        created:function(){
            // find head from parent table
            var table_par = this.$parent
            while (true){
                if (table_par.heads){
                    break
                }
                table_par = table_par.$parent
                if(!table_par){
                    break
                }
            }
            this.table_par = table_par
            this. head  = ex.findone(this.table_par.heads,{name:this.field})
        },
    mixins:[mix_editor],
    computed:{
        show_label:function(){
            var value = this.rowData[this.field]
            var opt = ex.findone(this.head.options,{value:value})
            return opt.html_label ||  opt.label
        }
    },
        methods:{
            handleCommand(command) {
                //this.$message('click on item ' + command);
                if(this.rowData[this.field] != command){
                    this.rowData[this.field] = command
                    this.on_changed()
                }

            },
            setSelect:function(value){
                if(this.rowData[this.field] != value){
                    this.rowData[this.field] = value
                    this.on_changed()
                }
            },
            //on_changed:function(){
            //    this.$emit('on-custom-comp',{name:'row_changed',row:this.rowData})
            //}
        }
    }

Vue.component('com-table-select',select)


//Vue.component('com-table-select',function(resolve,reject){
//    ex.load_css('https://unpkg.com/element-ui/lib/theme-chalk/index.css')
//    ex.load_js('https://unpkg.com/element-ui/lib/index.js',function(){
//        resolve(select)
//    })
//})


//var select = {
//    props:['rowData','field','index'],
//    template:`<div >
//    <select style="width: 100%" @change="on_changed()"  v-model="rowData[field]">
//        <option v-for="op in head.options" :value="op.value" v-text="op.label"></option>
//    </select>
//    </div>`,
//    data:function(){
//        return {
//        }
//    },
//    created:function(){
//        // find head from parent table
//        var table_par = this.$parent
//        while (true){
//            if (table_par.heads){
//                break
//            }
//            table_par = table_par.$parent
//            if(!table_par){
//                break
//            }
//        }
//        this.table_par = table_par
//        this. head  = ex.findone(this.table_par.heads,{name:this.field})
//    },
//    methods:{
//        on_changed:function(){
//            this.$emit('on-custom-comp',{name:'row_changed',row:this.rowData})
//        }
//    }
//}

//Vue.component('com-table-select',select)
