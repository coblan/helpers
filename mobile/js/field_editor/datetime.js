require('./styl/field_date.styl')

Vue.component('com-field-datetime',{
    props:['head','row'],
    data(){
        if(this.row[this.head.name]){
            var inn_value = new Date(this.row[this.head.name])
        }else if(this.head.init_value ){
            var inn_value = new Date(this.head.init_value)
        }
        else{
            var inn_value = new Date()
        }

        return {
            show:false,
            inn_value :inn_value,
            minDate: this.head.start?new Date(this.head.start):undefined,
            maxDate: this.head.end?new Date(this.head.end):undefined,
        }
    },
    template:`<van-cell class="com-field-date com-field-datetime" :title="head.label">
     <span :class="{empty_value:!row[head.name]}" v-text="row[head.name] || '请输入'+head.label"
        style="width: 5rem;display: inline-block;min-height: .4rem;text-align: left"  @click.stop="open()"></span>
        <!--<van-icon v-if="row[head.name]" slot="right-icon" name="cross" @click.stop="clear()" class="custom-icon" />-->
   <van-popup v-model="show" position="bottom" overlay>
    <van-datetime-picker
      v-model="inn_value"
      type="datetime"
       :min-date="minDate"
       :max-date="maxDate"
       cancel-button-text="清空"
      @confirm="on_confirm"
      @cancel = "on_cancel"
    />
</van-popup>

    </van-cell>`,
    methods:{
        open(){
            this.show =true
        },
        clear(){
            Vue.set(this.row,this.head.name,'')
        },
        on_confirm(){
            this.show =false
            if(this.inn_value){
                Vue.set(this.row,this.head.name,this.inn_value.Format('yyyy-MM-dd hh:mm:ss'))
                //this.row[this.head.name] = this.inn_value.Format('yyyy-MM-dd')
            }else {
                Vue.set(this.row,this.head.name,'')
                //this.row[this.head.name] = ''
            }

        },
        on_cancel(){
            this.show =false
            Vue.set(this.row,this.head.name,'')
        }

    }

})

Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}