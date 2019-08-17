Vue.component('com-field-compute',{
    props:['row','head'],
    template: `<div class="com-field-compute">
           <input type="text" :class="['form-control input-sm',head.input_class]" v-model="row[head.name]"
            		 	    :id="'id_'+head.name" :name="head.name" readonly
                        	:placeholder="head.placeholder"  :maxlength='head.maxlength'>
            </div>`,
    watch:{
        row(v){
            ex.eval(this.head.express,{row:v,head:this.head})
        }
    }
})