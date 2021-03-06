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
            //window.open(this.rowData[this.field])
            var ctx = {imgsrc:this.rowData[this.field]}
            pop_layer(ctx,'com-pop-image',function(){},{
                title:false,
                area: ['90%', '90%'],
                shade: 0.8,
                skin: 'img-shower',
                shadeClose: true,
            })

        }
    }
    }

Vue.component('com-table-picture',picture)
