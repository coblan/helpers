var multi_chosen= {
    props: ['row', 'head'],
    data: function () {
        var inn_config = {
            //orgin_order:true,
            order: false
        }
        if (this.head.config) {
            ex.assign(inn_config, this.head.config)
        }

        this.head.placeholder = this.head.placeholder || '请选择'

        return {
            model: this.row[this.head.name],
            cfg: inn_config,
            parStore:ex.vueParStore(this)
        }
    },
    template: `<div>
	        	<ul v-if='head.readonly'><li v-for='value in row[head.name]' v-text='get_label(value)'></li></ul>
	        	<div v-else>
	        	<input type="text" style="display: none" v-model='row[head.name]' :name="head.name">
	        	<multi-chosen  v-model='row[head.name]' :id="'id_'+head.name" :options='normed_options'></multi-chosen>
	        	</div>
	        	</div>`,
    mounted: function () {
        // 如果有默认值，
        if (this.head.default && !this.row[this.head.name]) {
            Vue.set(this.row, this.head.name, this.head.default)
        }
        var self=this
        // remote_options 只用在初始化的时候，请求远端服务器获取options。如果需要动态切换options，请设置 director_name 。
        //if(this.head.remote_options){
        //    ex.director_call(this.head.remote_options,{crt_value:this.row[this.head.name]},function(resp){
        //        self.head.options=resp
        //    })
        //}

        // 这种方式，一般是与filter共用options的时候
        if(this.head.ctx_name){
            self.head.options = named_ctx[this.head.ctx_name]
        }
        ex.vueEventRout(this)
    },

    watch:{
        my_value:function(v){
            this.$emit('input',v)
        }
    },

    computed:{
        my_value:function(){
            return this.row[this.head.name]
        },
        is_select:function(){
            var v = this.row[this.head.name]
            return v != undefined
        },
        place_value:function(){
            var v = this.row[this.head.name]
            if(v === undefined){
                return undefined
            }else  if(v === null){
                return null
            }else{
                return ''
            }
        },
        normed_options:function(){
            /*
             head.hide_related_field设置 隐藏与 row.hide_related_field 相等的选项

             * */
            var self=this
            //if(this.head.hide_related_field){
            //    var array = ex.filter(this.head.options,function(item){
            //        return item.value != self.row[self.head.hide_related_field]
            //    })
            //}else{
            //    var array=self.head.options
            //}
            var real_options=self.head.options
            //if(self.options){
            //    real_options=self.options
            //}else if(self._remote_options){
            //    real_options = self._remote_options
            //}

            return self.orderBy(real_options,'label')

        }
    },
    methods:{
        update_options:function(post_data){
            var self=this
            if(this.head.director_name){
                cfg.show_load()
                ex.director_call(self.head.director_name,post_data,function(data){
                    cfg.hide_load()
                    Vue.set(self.head,'options' ,data)
                })
            }
        },
        get_label:function(options,value){
            var option = ex.findone(options,{value:value})
            if(!option){
                return '---'
            }else{
                return option.label
            }
        },
        orderBy:function(array,key){
            if(this.head.order || this.cfg.order){
                return order_by_key(array,key)
            }else{
                return array
            }

        }
    }
}
Vue.component('com-field-multi-chosen',multi_chosen)