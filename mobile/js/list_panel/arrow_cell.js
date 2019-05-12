Vue.component('com-listpanel-arrow-cell',{
    props:['heads','rows','option'],
    template:`<div class="com-list-arrow-cell">
    <van-cell v-for="row in rows" title="单元格" :is-link="option.nextlevel" clickable>
                <template slot="title">
                    <div class="material-wave content"  @click="on_click(row)">
                        <component :is="head.editor" v-for="head in heads"
                            :class="head.class" :head="head" :row="row"></component>
                    </div>
                </template>
     </van-cell>
    </div>`,
    mounted(){
      ex.append_css(this.option.style)
    },
    methods:{
        on_click(row){
            this.$emit('select',row)
        }
    }
})