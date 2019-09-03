require('./styl/list_ctn.styl')

var list_ctn_field={
    props:['row','head'],
    template:`<div :class="['com-field-list-ctn',head.class]" >
            	<component class="list-ctn-field" v-for="head2 in myhead" :is="head2.editor" :head="head2" :row="row"></component>
              </div>`,
    data(){
        var parStore = ex.vueParStore(this)
        return {
            parStore:parStore,
        }
    },
    computed:{
        myhead(){
            var out_heads=[]
            ex.each(this.head.children,(item_name)=>{
               var head2 = ex.findone( this.parStore.vc.heads,{name:item_name})
                if(head2){
                    out_heads.push(head2)
                }
            })
            return out_heads
        }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    },
}
Vue.component('com-field-list-ctn',list_ctn_field)