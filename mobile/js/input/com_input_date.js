require('./scss/com_input_date.scss')

Vue.component('date',{
    mixins:[com_input_date],
    template:` <div class="com-date input-group datetime-picker">
                <input type="text" class="form-control input-sm real-input"
                readonly :placeholder="placeholder" @click="click_input()" v-model="value"/>

                <div class="input-group-addon" >
                    <i v-if="! value" @click="click_input()" class="fa fa-calendar" aria-hidden="true"></i>
                    <i v-else @click="$emit('input','')" class="fa fa-calendar-times-o" aria-hidden="true"></i>
                </div>
                </div>`,
    data:function(){
        return {
            inn_value: this.value
        }
    },
    methods:{
        init:function(){

        },
        click_input:function(){
            var id = new Date().getTime()
            var defvalue = new Date()
            if(this.value){
                var defvalue = this.value.split('-')
            }


            var self=this
            window.bb = weui.datePicker({
                start: 1970,
                end: 2030,
                defaultValue: defvalue,
                className:'com-input-date',
                onChange: function(result){
                },
                onClose:function(){
                    if(named_hub[id]){
                        history.back()
                    }
                    console.log('on close');
                },
                onConfirm: function(result){
                    self.$emit('input',result.join('-'))
                },
                id: 'datePicker_'+id
            });
            named_hub[id] =function(){
                bb.hide()
            }
            history.replaceState({callback:id},'')
            history.pushState({},'')
        },
        watch_value:function(n){
        }
    }
})