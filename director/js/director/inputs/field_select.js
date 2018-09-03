var sim_select= {
    props: ['row', 'head'],
    data: function () {
        var inn_config = {
            //orgin_order:true,
            order: false
        }
        if (this.head.config) {
            ex.assign(inn_config, this.head.config)
        }
        return {
            model: this.row[this.head.name],
            cfg: inn_config
        }
    },
    template: `<div>
            <span v-if='head.readonly' v-text='get_label(head.options,row[head.name])'></span>
            <select v-else v-model='row[head.name]'  :id="'id_'+head.name" :name="head.name"  class="form-control input-sm">
                <option v-if="head.placeholder" :value="place_value" disabled selected style='display:none;' class="placeholder" v-text="head.placeholder"></option>
            	<option v-for='opt in normed_options' :value='opt.value' v-text='opt.label'></option>
            </select>
            </div>`,
    mounted: function () {
        // 如果有默认值，
        if (this.head.default && !this.row[this.head.name]) {
            Vue.set(this.row, this.head.name, this.head.default)
        }

    },

    watch:{
        my_value:function(){
            if(this.head.remote_options){
                var self=this
                ex.director_call(this.head.remote_options,{row:self.row},function(data){
                    Vue.set(self.head,'options' ,data)
                })
            }
        }
    },

    computed:{
        my_value:function(){
            return this.row[this.head.name]
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
            if(this.head.hide_related_field){
                var array = ex.filter(this.head.options,function(item){
                    return item.value != self.row[self.head.hide_related_field]
                })
            }else{
                var array=self.head.options
            }

            return self.orderBy(array,'label')

        }
    },
    methods:{
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
Vue.component('com-field-select',sim_select)