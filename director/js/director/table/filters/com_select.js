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
        return {
            order:this.head.order || false
        }
    },
    computed:{
        myvalue:function(){
            return this.search_args[this.head.name]
        }
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)

            if(this.head.changed_emit ){
                ex.vuexEmit(this,this.head.changed_emit)
                //this.$store.state[parName].childbus.$emit(this.head.changed_emit)
            }
        }
    },
    mounted:function(){
        //var parName = ex.vuexParName(this)
        var self=this
        if(this.head.update_on ){
            ex.vuexOn(this,this.head.update_on,this.get_options)
            //if($.isArray(this.head.update_on)){
            //    ex.each(this.head.update_on,function(on_event){
            //        self.$store.state[parName].childbus.$on(on_event,self.get_options)
            //    })
            //}else{
            //    this.$store.state[parName].childbus.$on(this.head.update_on,this.get_options)
            //}
        }
    },
    methods:{
        get_options:function(){
            var self=this
            console.log('sss')
            ex.director_call(this.head._director_name,{search_args:self.search_args},function(resp){
                self.head.options = resp
            })
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
