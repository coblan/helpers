var validate_code =  {
    props:['row','head'],
    template:`<div style="position: relative;">
    <input type="text" class="form-control input-sm" v-model="row[head.name]" :id="'id_'+head.name" :name="head.name">
    <div>
    <div style="display: inline-block;border: 1px solid #9e9e9e;">
        <img  :src="row.validate_img" alt="">
    </div>
    <!--<span class="clickable" @click="change_code" style="white-space:nowrap;">看不清，换一张</span>-->
    </div>
    </div>`,
    methods:{
        change_code:function(){
            var self=this
            var post_data=[{fun:'new_validate_code'}]
            cfg.show_load()
            ex.post('/d/ajax/authuser',JSON.stringify(post_data),function(resp){
                self.head.code_img=resp.new_validate_code
                cfg.hide_load()
            })
        }
    }

}

Vue.component('com-field-auth-validate-code',validate_code)