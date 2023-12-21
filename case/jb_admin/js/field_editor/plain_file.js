require('./scss/file_uploader.scss')

/*
 * config={
 *    accept:""
 * }
 * */

function  check_file_size(fl,maxsize){
    if(fl.size > maxsize){
        if(maxsize > 1024*1024){
            var num_msg = (maxsize /(1024*1024) ).toFixed(2) + 'M'
        }else  if(maxsize > 1024){
            var num_msg = (maxsize /(1024) ).toFixed(2) + 'k'
        }else{
            var num_msg = maxsize
        }
        return  num_msg
    }
}

export var field_file_uploader={
    props:['row','head'],
    template:`<div><com-file-uploader-tmp :name="head.name" v-model="row[head.name]" :maxsize="head.maxsize" :config="head.config" :readonly="head.readonly"></com-file-uploader-tmp></div>`
}

export var com_file_uploader = {
    props: {
        value:{},
        readonly:{},
        config:{},
        name:{},
        maxsize:{
            default:1024*1024*100 //
        }
    } ,
    data:function(){

        return {
            picstr: this.value,
            pictures:this.value ? this.value.split(';'):[],
            crt_pic:''
        }
    },

    template:`<div class="file-uploader">
    <div v-if="!readonly">
        <input v-if="cfg.multiple"  v-show="!cfg.com_btn" class="pic-input" type="file" @change="upload_pictures($event)" :accept="cfg.accept" multiple="multiple">
        <input v-else v-show="!cfg.com_btn"  class="pic-input" type="file" @change="upload_pictures($event)" :accept="cfg.accept">
        <input type="text" :name="name" style="display: none" v-model="value">
    </div>

    <div class="wrap" style="display: flex;flex-direction: column;">
           <a v-for="pic in pictures" :href="pic" target="_blank"><span  v-text="pic"></span></a>
    </div>

     <!--<component v-if="cfg.com_btn && ! readonly" :is="cfg.com_btn" @click.native="browse()"></component>-->



    </div>`,
    mounted:function(){
        var self=this
        if(this.cfg.sortable){
            ex.load_js(js_config.js_lib.sortablejs,function(){
                let ele = $(self.$el).find('.sortable')[0]
                if(ele){
                     new Sortable($(self.$el).find('.sortable')[0],{
                        onSort: function (/**Event*/evt) {
                            self.ajust_order()
                        },
                    });
                }
               
            })
        }

    },
    computed:{
        //res_url:function(){
        //    return this.cfg.upload_url ? this.to: "/_face/upload"
        //},
        cfg:function(){
            var def_config = {
                upload_url:'/d/upload',
                accept:'image/*',
                multiple:false,
                sortable:true,
                on_click:function(url){
                    window.open(
                        url,
                        '_blank' // <- This is what makes it open in a new window.
                    );
                }
            }
            if(this.config){
                //if(! this.config.hasOwnProperty('multiple') || this.config.multiple){
                //    def_config.com_btn='file-uploader-btn-plus'
                //}
                ex.assign(def_config,this.config)
            }

            return def_config
        }

    },
    watch:{
        value:function(new_val,old_val){
            if(this.picstr != new_val){
                this.picstr=new_val
                this.pictures = this.value ? this.value.split(';'):[]
            }
            if(!this.picstr){
                $(this.$el).find('.pic-input').val("")
            }
        }
    },
    methods:{
        browse:function(){
            $(this.$el).find('input').click()
        },
        enter:function(pic){
            this.crt_pic= pic
        },
        out:function(){
            this.crt_pic=''
        },
        upload_pictures:function (event){
            var self=this
            var file_list = event.target.files
            if(file_list.length==0){
                return
            }
            if(this.maxsize){

                for(var i=0;i<file_list.length;i++){
                    var item_file = file_list[i]
                    var human_read_size = check_file_size(item_file,this.maxsize)
                    if(human_read_size){
                        return cfg.showMsg(`文件尺寸不能超过${human_read_size}`)
                    }
                }
            }

            var upload_url=this.cfg.upload_url

            //cfg.show_load()
            var ps = {
                progress:0,
            }
            cfg.pop_vue_com('com-pop-progress',{ps:ps,label:'上传中!'}, {
                title:false,
                area: ['300px', '80px'],
                shade: 0.01,
                closeBtn:0,
                resize:false,
                //skin:'background-none',
        })
            fl.uploads(file_list,upload_url,function(resp){
                ps.progress = 100
                if(resp){
                    if(self.cfg.multiple){
                        self.add_value(resp)
                    }else{
                        self.set_value(resp)
                    }
                }
                //hide_upload(300)
            },(progress)=>{
                //console.log(progress)
                if(progress <1){
                    ps.progress = parseInt( progress *100 )
                }
            })
        },
        set_value:function(value){
            //@value: [url1,url2]
            var val= value.join(';')
            this.$emit('input',val)
        },
        add_value:function(value){
            var self=this
            var real_add = ex.filter(value,function(item){
                return !ex.isin(item,self.pictures)
            })
            var real_list= self.pictures.concat(real_add)
            var val= real_list.join(';')
            self.$emit('input',val)
        },
        ajust_order:function (){
            var list = $(this.$el).find('ul.sortable img')
            var url_list=[]
            for(var i=0;i<list.length;i++){
                var ele=list[i]
                url_list.push($(ele).attr('src'))
            }
            var val=url_list.join(';')
            this.picstr=val
            this.$emit('input',val)
        },
        remove:function(pic){
            var pics =this.picstr.split(';')
            ex.remove(pics,function(item){return pic==item})
            var val= pics.join(';')
            this.$emit('input',val)
        },
        is_image:function(url){
            var type = this.get_res_type(url)
            return ex.isin(type.toLowerCase(),['jpg','png','webp','gif','jpeg','ico'])
        },
        get_res_type:function(url){
            var mt = /[^.]+$/.exec(url)
            if(mt.length>0){
                return mt[0]
            }else{
                return ""
            }
        },
        get_res_basename:function(url){
            var mt = /[^/]+$/.exec(url)
            if(mt.length>0){
                return mt[0]
            }else{
                return mt[0]
            }
        }
    }
}


Vue.component('com-file-uploader-tmp',com_file_uploader)
Vue.component('com-field-plain-file',field_file_uploader)

