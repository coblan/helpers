require('./styl/range.styl')

var range_field={
    props:['row','head'],
    template:`<div :class="['com-field-range',head.class]" >
            	    <component class="range-field" :is="start_head.editor" :head="start_head" :row="row"></component>
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                     <component class="range-field" :is="end_head.editor" :head="end_head" :row="row"></component>
              </div>`,
    data(){
        var parStore = ex.vueParStore(this)
        var start_head = ex.findone(parStore.vc.heads,{name:this.head.start_name})
        var end_head = ex.findone(parStore.vc.heads,{name:this.head.end_name})
        return {
            start_head:start_head,
            end_head :end_head

        }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    },
}
Vue.component('com-field-range',range_field)