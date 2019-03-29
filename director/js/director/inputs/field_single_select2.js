require('./scss/field_single_select2.scss')

var field_sigle_chosen={
    props:['row','head'],
    template:`<div :class="['com-field-single-select2',head.class]" >
    <span v-if="head.readonly" v-text="label_text" ></span>
    <input type="text" :name="head.name" style="display: none" v-model="row[head.name]">
    <div v-show="!head.readonly">
        <select  class="select2 field-single-select2 form-control" :id="'id_'+head.name">
             <option  :value="undefined" ></option>
            <option v-for="option in inn_options" :value="option.value" v-text="option.label"></option>
        </select>
    </div>

    </div>`,
    data:function(){
        var self =this
        return {
            inn_options :this.head.options,
            parStore:ex.vueParStore(self),
        }
    },
    mounted:function(){
        var self=this

        if (this.head.style){
            ex.append_css(this.head.style)
        }
        ex.load_css('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/css/select2.min.css')
        let prom1 = ex.load_js('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js')
        if(this.head.dyn_options){
            var prom2 =  ex.eval(this.head.dyn_options,{row:this.row,vc:this})
        }else{
            var prom2 =1
        }
        Promise.all([prom1,prom2]).then(function(){
            $(self.$el).find('select').select2({
                placeholder:self.head.placeholder || '请选择',
                allowClear: true
            })
            self.setValue(self.row[self.head.name])
            $(self.$el).find('.select2').change(function(e) {
                var value = $(self.$el).find('.select2').val( )
                if(value ==''){
                    Vue.delete(self.row,self.head.name)
                }else{
                    Vue.set(self.row,self.head.name,value)
                }
            })
        })

        ex.vueEventRout(this)


    },
    watch:{
        value:function(nv){
            this.setValue(nv)
        }
    },
    computed:{
        value:function(){
            return this.row[this.head.name]
        },
        label_text:function(){
            var opt = ex.findone(this.inn_options,{value:this.row[this.head.name]})
            if(opt){
                return opt.label
            }else{
                return ''
            }
        },
        //order_options:function(){
        //    if (this.head.order){
        //        return ex.sortOrder(this.inn_options,'label')
        //    }else{
        //        return this.inn_options
        //    }
        //}
    },
    methods:{
        setValue:function(val){
            $(this.$el).find('.select2').val(val);
            $(this.$el).find('.select2').trigger('change');
            Vue.set(this.row,this.head.name,val)
            this.$emit('input',val)
        },
        update_options:function(director_name,data){
            let self=this
            return new Promise(function(resolve,reject){
                ex.director_call(director_name,data).then(resp=>{
                        self.inn_options = resp
                        resolve()
                    })
            })

        }
    }
}

Vue.component('com-field-single-select2',field_sigle_chosen)