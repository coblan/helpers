//
var picture = {
        props:['rowData','field','index'],
        template:`<span>
        <img @load='loaded=true' :style="cusStyle"  @click="open()" :src="src" alt="" height="96px" style="cursor: pointer;">
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
        },
        cusStyle:function(){
            if(!this.loaded){
                return {
                    visibility:'hidden'
                }
            }else{
                return {
                    visibility:'visible'
                }
            }
        }
    },
    methods:{
        open:function(){
            window.open(this.rowData[this.field])
        }
    }
    }

Vue.component('com-table-picture',picture)
