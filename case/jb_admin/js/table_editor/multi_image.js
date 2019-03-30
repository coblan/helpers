
/*
 options:{
 key:value
 }
 * */
var mapper = {
    props:['rowData','field','index'],
    template:`<div class="com-table-multi-image" style="white-space: nowrap">
    <div v-for="image in image_list" style="display: inline-block;margin: 3px;">
        <img @click="big_win(image)" style="max-height: 100px;max-width:100px;"  :src="image" alt="图片不能显示">
    </div>

    </div>`,
    created:function(){
        // find head from parent table
        //var table_par = this.$parent
        //while (true){
        //    if (table_par.heads){
        //        break
        //    }
        //    table_par = table_par.$parent
        //    if(!table_par){
        //        break
        //    }
        //}
        //this.table_par = table_par
        //this.head= ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        image_list:function(){
            if(this.rowData[this.field]){
                return this.rowData[this.field]
            }else{
                return []
            }
        }
    },
    methods:{
        big_win:function(imgsrc){
            var ctx = {imgsrc:imgsrc}
            pop_layer(ctx,'com-pop-image',function(){},{
                title:false,
                area: ['90%', '90%'],
                shade: 0.8,
                skin: 'img-shower',
                shadeClose: true,
            })
        },
    }
}

Vue.component('com-table-multi-image',mapper)
