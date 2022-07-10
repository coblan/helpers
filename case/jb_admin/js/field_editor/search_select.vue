<template>
    <div class="com-field-search-select">
        <el_select :row="row" :head="head"></el_select>
    </div>

</template>
<script>
    import el_select from './select.vue'
    export default {
      /*
      * 这个组件应该是无用了，可以使用com-field-select   head.filterable=true 替代
      * */
        props:['row','head'],
        components:{
            el_select
        },
        data(){
            this.head.filterable = true
            return {
                inn_value:this.row[this.head.name],
                options:this.head.options || [],
                parStore:ex.vueParStore(this)
            }
        },
        mounted:function(){
            if(this.head.css){
                ex.append_css(this.head.css)
            }
            if(this.head.mounted_express){
                ex.eval(this.head.mounted_express,{vc:this,row:this.row,head:this.head})
            }
        },

        computed:{
            value:function(){
                return this.row[this.head.name]
            },
            normed_options(){
                return this.options
            },
        },
        methods:{

        }

    }
</script>


