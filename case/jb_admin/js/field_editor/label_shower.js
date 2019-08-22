var label_shower =  {
    props:['row','head'],
        template:`<div class="com-field-label-shower">
        <span class="readonly-info" v-text='label'></span>
        </div>`,
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        }
    }
}

Vue.component('com-field-label-shower',label_shower)