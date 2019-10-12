Vue.component('com-field-blocktext',{
    props:['head','row'],
    template:`<van-field class="com-field-linetext" v-model="inn_value" type="textarea" size="large"
    autosize
    clearable
    :label="head.label"
    :readonly="head.readonly"
    :placeholder="normed_placeholder"
    :name="head.name"
  ></van-field>`,
    data(){
        return {
            inn_value:this.row[this.head.name]
        }
    },
    watch:{
        inn_value(v){
            if(v != this.row[this.head.name]){
                this.row[this.head.name] = v
            }
        },
        out_value(v){
            if(v !=this.inn_value){
                Vue.set(this,'inn_value',v)
            }
        }
    },
    computed:{
        out_value(){
            return   this.row[this.head.name]
        },
        normed_placeholder:function(){
            if(! this.head.readonly){
                return this.head.placeholder || '请输入'+this.head.label
            }else{
                return ''
            }
        }
    },
    mounted(){
        var org = this.row[this.head.name]
        this.row[this.head.name] +='.'
        setTimeout(()=>{
            this.row[this.head.name]= org
        },100)
    }
})