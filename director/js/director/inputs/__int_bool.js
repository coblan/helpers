var field_bool={
    props:['row','head'],
    template:`<div class="checkbox">
	        <input type="checkbox" :id="'id_'+head.name" v-model='my_value' :disabled="head.readonly">
			 <label :for="'id_'+head.name"><span v-text='my_label'></span></label>
					  </div>`,
    computed:{
        my_label:function(){
            if(this.head.check_label){
                return this.head.check_label
            }else{
                return this.head.label
            }
        },
        my_value:{
            set:function(v){
                if(v){
                    this.row[this.head.name] = 1
                }else{
                    this.row[this.head.name] = 0
                }
            },
            get:function(){
                return Boolean(parseInt( this.row[this.head.name]) )
            }
        }
    }
}
Vue.component('com-field-int-bool',field_bool)