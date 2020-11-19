Vue.component('com-field-select',{
    props:['head','row'],
    template:`<div class="com-field-select van-cell" :class="{'van-cell--required':head.required && !head.readonly,'readonly':head.readonly}">
       <div style="position: relative">
        <van-popup  v-model="show" position="bottom">
                <van-picker :columns="normed_options" :default-index="crt_index"
                cancel-button-text="清空"
                @confirm="onConfirm" @cancel="clear()" value-key="label" show-toolbar></van-picker>
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
      >
       <!--<van-icon v-if="row[head.name]" slot="right-icon" name="cross" @click.stop="clear()" class="custom-icon" />-->
      </van-field>



    </div>
`,
    data:function(){
        Vue.set(this.row,this.head.name,this.row[this.head.name] ||  '')
        return {
            parStore:ex.vueParStore(this),
            show:false,
            options:this.head.options || [],
        }
    },
    mounted:function(){
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,row:this.row,head:this.head})
        }

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
        normed_options(){
            /*
             head.hide_related_field设置 隐藏与 row.hide_related_field 相等的选项
             * */
            var self=this
            if(this.head.option_show_express){
                var array = ex.filter(this.options,(item)=>{
                    return ex.eval(this.head.option_show_express,{option:item,row:self.row,ps:self.parStore,vc:self})
                })
            }else {
                var array = ex.filter(this.options,(item)=>{
                    if(item.show_express){
                        return ex.eval(item.show_express,{option:item,row:self.row,ps:self.parStore,vc:self})
                    }else{
                        return true
                    }
                })
            }
            return array
        },
        crt_index:function(){
            let value = this.row[this.head.name]
            let value_list = this.options.map((opetion)=>{
                return opetion.value
            })
            return value_list.indexOf(value)
        },
        my_value:function(){
            return this.row[this.head.name]
        },
        show_label:function(){

            let value = this.row[this.head.name]
            let find = ex.findone(this.options,{value:value})
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
        clear(){
            this.show=false
            Vue.set( this.row,this.head.name,'')
        },
        on_click:function(){
            if( ! this.head.readonly){
                this.show=true
            }

        },
        onConfirm:function(v,index){
            Vue.set( this.row,this.head.name,v.value)
            //this.row[this.head.name] = v.value
            this.show=false
            Vue.nextTick(()=>{
                $(this.$el).find('input').isValid()
            })
        }
    }
})