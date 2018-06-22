
var picture = {
        props:['rowData','field','index'],
        template:`<span>
        <img @load='loaded=true' v-show='loaded' @click="open()" :src="src" alt="" height="96px" style="cursor: pointer;">
        </span>`,
    data:function(){
        return {
            loaded:false
        }
    },
    watch:{
        src:function(){
            this.loaded=false
        }
    },
    computed:{
        src:function(){
            return this.rowData[this.field]
        }
    },
    methods:{
        open:function(){
            window.open(this.rowData[this.field])
        }
    }
    }

Vue.component('com-table-picture',picture)
