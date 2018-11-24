require('./scss/filter_select.scss')

var com_select = {
    props:['head','search_args','config'],
    template:`<select v-model='search_args[head.name]' class="form-control input-sm com-filter-select" >
        <option v-if="head.forbid_select_null" :value="undefined" disabled v-text='head.label'></option>
        <option v-else :value="undefined" v-text='head.label' ></option>
        <option :value="null" disabled >---</option>
        <option v-for='option in orderBy(options,"label")' :value="option.value" v-text='option.label'></option>
    </select>
    `,
    data:function(){
        var self=this
        return {
            order:this.head.order || false,
            parStore:ex.vueParStore(this)
        }
    },
    computed:{
        myvalue:function(){
            return this.search_args[this.head.name]
        },
        options:function(){
            if(this.head.ctx_name){
                return named_ctx[this.head.ctx_name]
            }else{
                return this.head.options
            }
        }
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)
            if(this.head.changed_emit ){
                this.parStore.$emit(this.head.changed_emit,v)
            }
        },
        options:function(v){
            delete  this.search_args[this.head.name]
        }
    },
    mounted:function(){
        //var parName = ex.vuexParName(this)
        var self=this

        // 更新值
        if(this.head.update_options_on ){
            //ex.vuexOn(this,this.head.update_options_on,this.get_options)
            this.parStore.$on(this.head.update_options_on,this.get_options)
        }
        // 清空值
        //if(this.head.clear_value_on){
        //    //ex.vuexOn(this,this.head.update_options_on,this.clear_value)
        //    this.parStore.$on(this.head.update_options_on,this.clear_value)
        //}
    },
    methods:{
        get_options:function(){
            this.clear_value()
            var self=this
            console.log('sss')
            ex.director_call(this.head.director_name,{search_args:self.search_args},function(resp){
                self.head.options = resp
            })
        },
        clear_value:function(){
            delete this.search_args[this.head.name]
        },
        orderBy:function (array,key) {
            if(! this.order){
                return array
            }else{
                return  array.slice().sort(function (a,b) {
                    if(isChinese(a[key])&&isChinese(b[key])){
                        return a[key].localeCompare(b[key],'zh')
                    }else{
                        return compare(a[key],b[key])
                    }
                })
            }
        },
    }
}
Vue.component('com-select-filter',com_select)
// 以后替换为下面的标准名
Vue.component('com-filter-select',com_select)

function isChinese(temp){
    var re=/[^\u4E00-\u9FA5]/;
    if (re.test(temp[0])){return false  ;}
    return true ;
}
function compare(temp1, temp2) {
    if (temp1 < temp2) {
        return -1;
    } else if (temp1 == temp2) {
        return 0;
    } else {
        return 1;
    }
}
