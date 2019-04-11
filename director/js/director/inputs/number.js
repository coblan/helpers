var number = {
    props:['row','head'],

        template: `<div><span v-if='head.readonly' v-text='row[head.name]'></span>
            		<input v-else type="text" class="form-control input-sm" v-model="row[head.name]" :id="'id_'+head.name"
            		    :name="head.name" :step="head.step"
            		     @keypress="isNumber($event)"
                        :placeholder="head.placeholder" :autofocus="head.autofocus"></div>`,
        methods:{
            isNumber:function(evt){
                evt = (evt) ? evt : window.event;
                var charCode = (evt.which) ? evt.which : evt.keyCode;
                if ((charCode >= 48 && charCode <= 57) || charCode== 46) {
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