require('./styl/multi_row.styl')

var multi_row = {
    props:['rowData','field','index'],
    template:`<div class="com-field-multi-row">
    <div class="myrow" v-for="(row,rindex) in rowData[head.rows_field]" >
        <component :is="head.row_editor" :rowData="row" :field="head.name" :index="rindex"></component>
    </div>
    </div>`,
    data(){
        this.init_head()
        return {
            parStore:ex.vueParStore(this)
        }
    },

    mounted(){
        setTimeout(()=>{
            this.update_title()
        },1000)
        this.parStore.$on('header-dragend',this.on_drag)
    },
    computed:{
        mydata(){
            var rows = this.rowData[this.head.rows_field]
            return  ex.map(rows,(row)=>{return row[this.field]})
        }
    },
    watch:{
        mydata(){
            setTimeout(()=>{
                this.update_title()
            },1000)
        }
    },
    methods:{
        init_head(){
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
            this.head = ex.findone(this.table_par.heads,{name:this.field})
        },
        on_drag(kws){
            //newWidth, oldWidth, column, event
            if(kws.column.property == this.field){
                setTimeout(()=>{
                    this.update_title()
                },1000)
            }
        },
        update_title(){

            ex.each($(this.$el).find('.myrow'),mydiv=>{
                if( $(mydiv).width() <  $(mydiv).find('span').width() ){
                    $(mydiv).attr('title',mydiv.textContent)
                }else{
                    $(mydiv).attr('title','')
                }
            })
        },

    }

}


Vue.component('com-field-multi-row',multi_row)
