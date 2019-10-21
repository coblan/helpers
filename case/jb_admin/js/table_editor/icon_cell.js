require('./styl/icon_cell.styl')

var operations={
    props:['rowData','field','index'],
    template:`<div class="com-table-icon-cell">
        <div class="icon-item" v-for="icon in myicons">
            <img :src="icon.url" alt="" :title="icon.label">
        </div>
    </div>`,
    created:function(){
        // find head from parent table
        var table_par = this.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        this.table_par = table_par
        this. head  = ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        myicons(){
            var pp = ex.eval(this.head.icon_express,{row:this.rowData})
            return pp
        }
    },
    mounted:function(){
        this.parStore = ex.vueParStore(this)
    },
    methods:{
        on_operation:function(op){
            if(op.action){
                ex.eval(op.action,{ps:this.parStore,head:this.head,row:this.rowData})
            }
        },
        //on_click:function(op){
        //    if(op.action){
        //        ex.eval(op.action,{ps:this.parStore,head:this.head,row:this.rowData})
        //    }
        //}

    }
}

Vue.component('com-table-icon-cell',operations)
