require('./styl/multi_row.styl')

var multi_row = {
    props:['rowData','field','index'],
    template:`<div class="com-table-multi-row">
    <div class="myrow" v-for="(row,rindex) in rows" >
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
        // 如果整行的高度不是由 本插件撑起来的时候，改列内容会跑到中间，看起来比较怪异，所以设置 顶部对齐
        $(this.$el).parent().parent().css("vertical-align", "top")
        setTimeout(()=>{
            this.update_title()
        },1000)
        this.parStore.$on('header-dragend',this.on_drag)
    },
    computed:{
        rows(){
            if(! Boolean(this.rowData[this.head.rows_field])){
                return []
            }
            if( typeof this.rowData[this.head.rows_field] =='string'){
                var rows = JSON.parse(this.rowData[this.head.rows_field])
            }else{
                var rows = this.rowData[this.head.rows_field]
            }
            return rows
        },
        mydata(){
            //debugger
            //if( typeof this.rowData[this.head.rows_field] =='string'){
            //    var rows = JSON.parse(this.rowData[this.head.rows_field])
            //}else{
            //    var rows = this.rowData[this.head.rows_field]
            //}
            var rows =  this.rows ;//this.rowData[this.head.rows_field]

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
Vue.component('com-table-multi-row',multi_row)
