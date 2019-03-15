var field_bool={
    props:['row','head'],
        template:`<div class="checkbox">
	        <input type="checkbox" :id="'id_'+head.name" v-model='row[head.name]' :name="head.name" :disabled="head.readonly">
			 <label :for="'id_'+head.name"><span v-text='head.check_label'></span></label>
					  </div>`,
        computed:{
            my_label:function(){
                if(this.head.check_label){
                    return this.head.check_label
                }else{
                    return this.head.label
                }
            }
    }
}
Vue.component('com-field-bool',field_bool)