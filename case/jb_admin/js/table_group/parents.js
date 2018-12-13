var table_parents={
    data:function(){
        var self=this
        return {
            parStore:ex.vueParStore(self)
        }
    },
    template:`<div class="com-table-parents">
          <ol v-if="parStore.parents.length>0" class="breadcrumb jb-table-parent">
            <li v-for="par in parStore.parents"><a href="#" @click="on_click(par)"  v-text="par.label"></a></li>
        </ol>
    </div>`,
    methods:{
        on_click:function(par){
            this.parStore.$emit('parent_changed',par)
            this.parStore.get_childs(par.value)
        }
    }
}
Vue.component('com-table-parents',table_parents)