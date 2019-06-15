Vue.component('com-field-select',{
    props:['head','row'],
    template:`<div class="van-cell com-field-select">
    <div style="position: relative">
        <van-popup  v-model="show" position="bottom">
                <van-picker :columns="head.options" :default-index="crt_index"
                @confirm="onConfirm" @cancel="show=false" value-key="label" show-toolbar></van-picker>
          </van-popup>
    </div>

    <van-field v-model="show_label" style="padding: 0"
        :label="head.label"
        type="text"
        :placeholder="normed_placeholder"
        @click.native="on_click()"
        autosize
        readonly
        :error-message="head.error"
        :name="head.name"
      ></van-field>
    </div>
`,
    data:function(){
        return {
            parStore:ex.vueParStore(this),
            show:false
        }
    },
    mounted:function(){
        if(!this.head.validate_showError){
            Vue.set(this.head,'error','')
            this.head.validate_showError="scope.head.error=scope.msg"
        }
        if(!this.head.validate_clearError){
            this.head.validate_clearError="scope.head.error=''"
        }

        ex.vueEventRout(this)
    },
    watch:{
        my_value:function(v){
            this.$emit('input',v)
        }
    },
    computed:{
        crt_index:function(){
            let value = this.row[this.head.name]
            let value_list = this.head.options.map((opetion)=>{
                return opetion.value
            })
            return value_list.indexOf(value)
        },
        my_value:function(){
            return this.row[this.head.name]
        },
        show_label:function(){
            let value = this.row[this.head.name]
            let find = ex.findone(this.head.options,{value:value})
            var label = value
            if(find){
                label = find.label
            }
            return label
        },
        normed_placeholder:function(){
            if(! this.head.readonly){
               return this.head.placeholder || '请选择'+this.head.label
            }else{
                return ''
            }
        }
    },
    methods:{
        on_click:function(){
            if( ! this.head.readonly){
                this.show=true
            }

        },
        onConfirm:function(v,index){
            Vue.set( this.row,this.head.name,v.value)
            //this.row[this.head.name] = v.value
            this.show=false
        }
    }
})