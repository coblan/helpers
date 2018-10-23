require('./scss/filter_select.scss')

var com_select = {
    props:['head','search_args','config'],
    template:`<select v-model='search_args[head.name]' class="form-control input-sm com-filter-select" >
        <option v-if="head.forbid_select_null" :value="null" disabled v-text='head.label'></option>
        <option v-else :value="undefined" v-text='head.label' ></option>
        <option :value="null" disabled >---</option>
        <option v-for='option in orderBy( head.options,"label")' :value="option.value" v-text='option.label'></option>
    </select>
    `,
    data:function(){
        //var inn_cfg = {
        //    order: this.head.order || false  // 默认false
        //}
        //ex.assign(inn_cfg,this.config)
        return {
            order:this.head.order || false
        }
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)
        }
    },
    methods:{
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
