
var depart={
    props:['url','root'],
    data:function(){
        return {
            parents:[this.root],
            items:[],

            checked:[],
            clip:[],
        }
    },
    computed:{
        par:function(){
            return this.parents[this.parents.length-1]
        } ,
        root:function(){
            return this.parents[0]
        }
    },
    mounted:function(){
        this.dir_data(this.par)
    },
    methods:{
        dir_data:function(item){
            var self=this
            this.checked=[]
            dp_back_call([{fun:'dir_data',root:this.root,par:item}],function(resp){
                self.parents=resp.dir_data.parents
                self.items=resp.dir_data.items
            })
        },
    },
    template:`
        <div class="scroll-wraper">

            <ul class="breadcrumb">
                <li v-for="par in parents" @click="dir_data(par)">
                    <span v-text="par._label"></span>
                </li>
            </ul>
            <ul style="margin-left: 1em;">
                <li v-for="item in items" class="flex" style="justify-content:space-between;">

                    <span v-text="item._label" @click="dir_data(item)"></span>

                </li>
            </ul>
        </div>
    `

}

Vue.component('com-depart-browser',depart)