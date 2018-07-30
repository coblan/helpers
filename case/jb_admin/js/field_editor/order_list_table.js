var order_list =  {
    props:['row','head'],
    template:`<div>
    <button @click="add_new()">添加</button>
    <table>
    <tr> <th v-for="col in head.heads" v-text="head.label"></th></tr>
    <tr v-for="item in row[head.name]">
        <td v-for="col in head.heads">
            <component :is="col.editor" :row="item" :head="col"></component>
        </td>
        <td><button>编辑</button><button>删除</button><button>确定</button></td>
     </tr>
    </table>
    </div>`,
    mounted:function(){
        if(!this.row[this.head]){
            this.row[this.head] = []
        }
    },
    methods:{
        add_new:function(){
            this.row[this.head].append({})
        },
        norm_head:function(head,row){
            if(row._editing){
                
            }
        }
    }

}

Vue.component('com-field-order-list',order_list)