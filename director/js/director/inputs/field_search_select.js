/*
*  这个模块被淘汰了。新的 com-field-search-select 在 jbadmin中使用element组件构建
*  但是这个模块 是按照第一个字母来搜索的， 这个与element不一样，element用的任意字母。介于此，这个模块以后可能会用得上。
* */
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