
var line_text={
    props:['row','head'],
    template:`<div :class="['com-field-linetext',head.class]" :style="head.style">
    	<span class="readonly-info" v-if='head.readonly' v-text='row[head.name]'></span>
        <div  v-else  class="form-inline">
            <!--<input type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]">-->
            <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder"
                :id="'id_'+head.name" :name="head.name"
                :maxlength="head.maxlength">
            <template slot="prepend" >
                <span  v-if="head.prefix" v-html="head.prefix"></span>
            </template>
             <template slot="append">
               <span  v-if="head.suffix" v-html="head.suffix"></span>
             </template>
            </el-input>
             <!--<div class="input-group" >-->
                    <!--<div class="input-group-addon" v-if="head.prefix" v-html="head.prefix"></div>-->
            			<!--<input type="text" class="form-control input-sm" v-model="row[head.name]"-->
            		 	    <!--:id="'id_'+head.name" :name="head.name"-->
                        	<!--:placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>-->
                     <!--<div class="input-group-addon" v-if="head.suffix" v-html="head.suffix"></div>-->
              <!--</div>-->
         </div>
    </div>`,
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
        if(this.head.on_mounted){
            ex.eval(this.head.on_mounted,{vc:this})
        }
    }
}
Vue.component('com-field-linetext',line_text)