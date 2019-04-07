var line_text={
    props:['row','head'],
    template:`<div :class="['com-field-linetext',head.class]" :style="head.style">
            			<span v-if='head.readonly' v-text='row[head.name]'></span>
            			<input v-else type="text" :class="['form-control input-sm',head.input_class]" v-model="row[head.name]"
            		 	    :id="'id_'+head.name" :name="head.name" data-
                        	:placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>
                       </div>`,
}
Vue.component('com-field-linetext',line_text)