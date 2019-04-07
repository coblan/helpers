var search_select = {
    props:['row','head'],
    data:function(){
        return {
            model:this.row[this.head.name]
        }
    },
        template:`<div>
                <span v-if='head.readonly' v-text='get_label(head.options,row[head.name])'></span>
                <select v-else v-model='row[head.name]'  :id="'id_'+head.name"  class="selectpicker form-control" data-live-search="true">
                    <option v-for='opt in orderBy(head.options,"label")' :value='opt.value'
                     :data-tokens="opt.label" v-text='opt.label'></option>
                </select>
                </div>`,
            mounted:function(){
        var self=this
        if(this.head.default && !this.row[this.head.name]){
            Vue.set(this.row,this.head.name,this.head.default)
        }
        ex.load_css("/static/lib/bootstrap-select.min.css")
        ex.load_js("/static/lib/bootstrap-select.min.js",function(){
            $(self.$el).find('.selectpicker').selectpicker()
        })
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
                return order_by_key(array,key)
            }
        }
    }

Vue.component('com-field-search-select',search_select)