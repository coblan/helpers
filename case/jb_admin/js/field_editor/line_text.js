var line_text={
    props:['row','head'],
    template:`<div :class="['com-field-linetext',head.class]" :style="head.style">
            			<span class="readonly-info" v-if='head.readonly' v-text='row[head.name]'></span>
            			<input v-else type="text" :class="['form-control input-sm',head.input_class]" v-model="row[head.name]"
            		 	    :id="'id_'+head.name" :name="head.name"
                        	:placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>
                       </div>`,
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    }
}
Vue.component('com-field-linetext',line_text)