var line_text={
    props:['row','head'],
    template:`<div :class="['com-field-linetext',head.class]" :style="head.style">
    	<span class="readonly-info" v-if='head.readonly' v-text='row[head.name]'></span>
      <div  v-else  class="form-inline">
          <div class="input-group" >
                    <div class="input-group-addon" v-if="head.prefix" v-html="head.prefix"></div>
            			<input type="text" :class="['form-control input-sm',head.input_class]" v-model="row[head.name]"
            		 	    :id="'id_'+head.name" :name="head.name"
                        	:placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>
                     <div class="input-group-addon" v-if="head.suffix" v-html="head.suffix"></div>
                     </div>
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