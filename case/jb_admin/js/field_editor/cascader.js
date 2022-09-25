
var cascader_field =  {
    props:['row','head'],
    methods:{
    },
    data:function(){
        return {
            selected:[1,2],
            // demon 数据
            options: [{
                value:'1',
                label: '一级 1',
                children: [{
                    value:'21',
                    label: '二级 1-1',
                    children: [{
                        value:'31',
                        label: '三级 1-1-1',
                        children:[
                            {
                                value:'41',
                                label:'四级1'
                            }
                        ]
                    }]
                }]
            }, {
                value:'2',
                label: '一级 2',
                children: [{
                    value:'22',
                    label: '二级 2-1',
                    children: [{
                        value:'32',
                        label: '三级 2-1-1',
                        pk:3
                    }]
                }, {
                    value:'23',
                    label: '二级 2-2',
                    children: [{
                        value:'33',
                        label: '三级 2-2-1'
                    }]
                }]
            },
            ],
        }
    },
    template:`
<!--:show-all-levels="false"-->
<div class="com-field-cascader">
 <input type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]">
<el-cascader class="com-field-cascader"
            v-model="row[head.name]"
            :options="head.options"
            :props="myprops"
            size="small"
            clearable>
        </el-cascader>
</div>
      `,
    //default-expand-all
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        },
        myprops(){
            if(this.head.onlyLeaf){
                return  {emitPath:false}
            }else{
                return {checkStrictly: true,emitPath:false }
            }

        }
    }
}

Vue.component('com-field-cascader',cascader_field)
//Vue.component('com-field-ele-tree-name-layer',function(resolve,reject){
//ex.load_css('https://unpkg.com/element-ui/lib/theme-chalk/index.css')
//ex.load_js('https://unpkg.com/element-ui/lib/index.js',function(){
//resolve(label_shower)
//})
//})