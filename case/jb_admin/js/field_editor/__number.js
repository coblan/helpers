var number = {
    props:['row','head'],

        template: `<div :class="['com-field-number','field-'+head.name,head.class]" >
       <span v-if='head.readonly && !head.prefix && !head.suffix' v-text='row[head.name]'></span>
       <div  v-else class="form-inline">
           <!--<input type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]" >-->
            <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder" :readonly="head.readonly"
            :name="head.name"
            :id="'id_'+head.name"
                @keypress.native="isNumber($event)"
             :autofocus="head.autofocus">
                <template slot="prepend" >
                    <span  v-if="head.prefix" v-html="head.prefix"></span>
                </template>
                 <template slot="append">
                   <span  v-if="head.suffix" v-html="head.suffix"></span>
                 </template>
            </el-input>
       </div>

         </div>`,

    mounted(){
        //if(this.head.width){
        //    var width = this.head.width
        //    var myclass ='.com-field-number.field-'+this.head.name
        //    ex.append_css(`${myclass} input{width:${width} !important`)
        //}
    },
        methods:{
            isNumber:function(evt){
                evt = (evt) ? evt : window.event;
                var charCode = (evt.which) ? evt.which : evt.keyCode;
                if ((charCode >= 48 && charCode <= 57) || charCode== 46 || charCode== 45) {
                    if(charCode==46 && this.row[this.head.name].indexOf('.')!=-1){
                        return evt.preventDefault();
                    }else{
                        return true
                    }
                }else{
                    return evt.preventDefault();
                }
                //if (charCode==101 ||charCode==69 ) { // 排除掉E
                //    evt.preventDefault();
                //} else if(charCode==46 && this.row[this.head.name].indexOf('.')!=-1){
                //    return evt.preventDefault();
                //} else  {
                //    return true;
                //}
            }
        }
}

Vue.component('com-field-number',number)