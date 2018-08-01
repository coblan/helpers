require('./scss/change_order.scss')
var change_order = {
    props:['rowData','field','index'],
    template:`<span class="change-order">
    <span class="arrow" @click="up()">
    <i  class="fa fa-long-arrow-up"></i>
    </span>
    <span class="arrow" @click="down()">
     <i  class="fa fa-long-arrow-down"></i>
    </span>
    </span>`,
    methods:{
        up:function(){
            this.$emit('on-custom-comp',{fun:'row_up',row:this.rowData})
        },
        down:function(){
            this.$emit('on-custom-comp',{fun:'row_down',row:this.rowData})
        }
    }

}

Vue.component('com-table-change-order',change_order)
