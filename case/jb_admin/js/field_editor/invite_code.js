var com_field_invite_code =  {
    props:['row','head'],
    created:function(){

        if(search_args[this.head.key]){
            this.row[this.head.name] = search_args[this.head.key]
        }
    },
    template:`<div class="com-field-invite-code">
        <com-field-linetext :head="head" :row="row"></com-field-linetext>
    </div>`,
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        }
    }
}

Vue.component('com-field-invite-code',com_field_invite_code)