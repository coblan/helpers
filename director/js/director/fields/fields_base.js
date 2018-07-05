import {baseInput} from  '../inputs/basic'
export var field_base={
    props: {
        head:{
            required:true
        },
        row:{
            required:true
        },
        //kw:{
        //    required:true
        //},
    },
    computed:{
        //row:function(){return this.kw.row},
        //errors:function() {
        //    if(!this.kw.errors){
        //        Vue.set(this.kw,'errors',{})
        //    }
        //    return this.kw.errors
        //},
        //head:function(){
        //    var heads = this.kw.heads
        //    for (var x=0;x<heads.length;x++) {
        //        var head = heads[x]
        //        if (head.name == this.name) {
        //            return head
        //        }
        //    }
        //
        //}
    },
    methods: {
        //error_data: function (name) {
        //    if (this.errors[name]) {
        //        return this.errors[name]
        //    } else {
        //        return ''
        //    }
        //}
    },
    components: baseInput

}


