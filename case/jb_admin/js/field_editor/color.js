export default {
    props:['row','head'],
    template:`<div :class="['com-field-color',head.class]">
   	<input type="text"  v-model="row[head.name]"
            		 	    :id="'id_'+head.name" :name="head.name" style="display: none;">
    <el-color-picker
  v-model="row[head.name]"
  color-format="hex"
   :show-alpha="head.has_opacity"
  :predefine="predefineColors">
</el-color-picker>
            			<!--<span class="readonly-info" v-if='head.readonly' v-text='row[head.name]'></span>-->
            			<!--<input v-else type="text" :class="['form-control input-sm',head.input_class]" v-model="row[head.name]"-->
            		 	    <!--:id="'id_'+head.name" :name="head.name" data- -->
                        	<!--:placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>-->
                       </div>`,
    data(){
        return {
            predefineColors: [
                '#ff4500',
                '#ff8c00',
                '#ffd700',
                '#90ee90',
                '#00ced1',
                '#1e90ff',
                '#c71585',
            ]
        }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    }
}
