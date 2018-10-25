var com_select = {
    props:['head','search_args','config'],
    template:`<select v-model='search_args[head.name]' class="form-control input-sm" >
        <option :value="null_value" v-text='head.label'></option>
        <option  disabled >---</option>
        <option v-for='option in orderBy( head.options,"label")' :value="option.value" v-text='option.label'></option>
    </select>
    `,
    data:function(){
        return {
        }
    },
    computed:{
        watchedValue:function(){
            return this.search_args[this.head.related]
        },
        null_value:function(){
            if(this.search_args[this.head.name] === null ){
                return null
            }else {
                return undefined
            }
        }
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)
        },
        watchedValue:function(nv){
            var self=this
            if(nv){
                var post_data=[{fun:"director_call",director_name:this.head.director_name,kws:{related:nv}}]
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    self.head.options=resp.director_call
                })
            }else{
                self.head.options=[]
            }
            self.search_args[self.head.name]=null

        }
    },
    methods:{

        orderBy:function (array,key) {
            if(! this.head.order){
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
Vue.component('com-related-select-filter',com_select)

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
