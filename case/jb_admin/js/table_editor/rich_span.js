require('./styl/rich_span.styl')

var label_shower = {
    props:['rowData','field','index'],
//:class="myclass"
template:`<div :class="['com-table-rich-span',myclass]" :style="mystyle">
 <component v-if="head.inn_editor"
            :is="head.inn_editor"
            :row-data="rowData" :field="field" :index="index"></component>
            <span v-else v-text="show_text"></span>
</div>`,
    created(){
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
        this.parStore = ex.vueParStore(this)
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
        this.on_row_change()
    },
    watch:{
        rowData:{
            handler(v){
                this.on_row_change()
            },
            deep:true
        }
    },
    methods:{
        on_row_change(){
            if(this.head.row_change_express){
                ex.eval(this.head.row_change_express,{row:this.rowData,head:this.head,td:$(this.$el).parents('td').first()})
            }
        },
        light_level(h){
            var h=h.slice(1)
            var r = 0, g = 0, b = 0;
            r = parseInt(h[0],16)*16 + parseInt(h[1],16);
            g = parseInt(h[2],16)*16 + parseInt(h[3],16);
            b = parseInt(h[4],16)*16 + parseInt(h[5],16);
            return r * 0.299 + g * 0.587 + b * 0.114;
        },
         hexToReverse(h) {
             var h=h.slice(1)
            var r = 0, g = 0, b = 0;
            r = 255 - parseInt(h[0],16)*16 - parseInt(h[1],16);
            g = 255 - parseInt(h[2],16)*16 - parseInt(h[3],16);
            b = 255 - parseInt(h[4],16)*16 - parseInt(h[5],16);
            var out= (r < 16 ? "0" + r.toString(16).toUpperCase() : r.toString(16).toUpperCase()) + (g < 16 ? "0" + g.toString(16).toUpperCase() : g.toString(16).toUpperCase()) + (b < 16 ? "0" + b.toString(16).toUpperCase() : b.toString(16).toUpperCase());
             return '#'+out
         }
    },
    computed:{
        mystyle(){
            if(this.head.style){
               return ex.eval(this.head.style,{row:this.rowData,head:this.head,vc:this})
            }
        },
        show_text:function(){
            var value = this.rowData[this.field]
            if( value == undefined){
                return ''
            }else if(typeof value == 'object'){
                return JSON.stringify(value)
            } else{
                return this.rowData[this.field]
            }
        },
        myclass(){
            if(this.head.cell_class){
                return ex.eval(this.head.cell_class,{row:this.rowData,head:this.head})
            }else{
                return ''
            }
        }
    }
}

Vue.component('com-table-rich-span',label_shower)
