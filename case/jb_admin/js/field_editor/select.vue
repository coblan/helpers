<template>
    <div class="com-field-select" :class="head.class" >
        <span v-if='head.readonly' v-text='get_label'></span>
        <div v-else :class="com_id">
            <input type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]"><!-- :clearable="!head.required"-->

          <el-select v-show="loaded"  :class="{start:!loaded || !is_select }"  v-model="row[head.name]"
                        :collapse-tags="head.no_wrap"
                        :multiple="head.multiple"
                        :filterable="head.multiple ||  head.filterable "
                        :placeholder="head.placeholder"
                        size="small"
                        :clearable="!head.multiple && !head.required"
                      :popper-class="head.no_wrap?'com-field-select-on-wrap':'com-field-select-wrap'"
            >
                <el-option
                        v-for="item in normed_options .concat(invalid_options) "
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                </el-option>
            </el-select>
          <i v-if="head.add_express" @click="onAddNew" title="新建" class="el-icon-circle-plus" style="color: #0aa938;cursor: pointer"></i>
        </div>
    </div>
</template>
<script>
    export default {
        props: ['row', 'head'],
      /*
      * filterable=true, 取代了 search_select
      * */
        data: function () {
            var inn_config = {
//orgin_order:true,
                order: false
            }
            if (this.head.config) {
                ex.assign(inn_config, this.head.config)
            }

            this.head.placeholder = this.head.placeholder || cfg.tr('请选择')

            return {
                model: this.row[this.head.name],
                cfg: inn_config,
                parStore:ex.vueParStore(this),
                options:this.head.options || [],
                loaded:false,
                oldstyle:null,
                com_id:`select-${Date.now()}`
            }
        },
        mounted: function () {
            // 如果有默认值，
            if (this.head.default && !this.row[this.head.name]) {
                Vue.set(this.row, this.head.name, this.head.default)
            }
            var self=this
            // 兼容老的调用,新的请在 on_mounted 里面调用
            // remote_options 只用在初始化的时候，请求远端服务器获取options。如果需要动态切换options，请设置 director_name 。
            // TODO 清除这段代码
            if(this.head.remote_options){
                ex.director_call(this.head.remote_options,{crt_value:this.row[this.head.name]},function(resp){
                    self.head.options=resp
                    self.options = resp
                })
            }
            // TODO 清除这段代码
            if(this.head.on_mounted){
                ex.eval(this.head.on_mounted,{vc:this})
            }

            if(this.head.mounted_express){
                ex.eval(this.head.mounted_express,{vc:this})
            }
            // 这种方式，一般是与filter共用options的时候
            // TODO 清除这段代码。用 mounted_express 代替
            if(this.head.ctx_name){
                self.head.options = named_ctx[this.head.ctx_name]
            }
            ex.vueEventRout(this)

            if(this.head.css){
                ex.append_css(this.head.css)
            }

            // 为了纠正多选情况下，启动时 布局 错乱问题。
          if (this.head.multiple){

            this.$nextTick(()=>{
              setTimeout(()=>{
                this.loaded=true
              },100)
            })
          }else {
            this.loaded=true
          }

          // setTimeout(()=>{

            this.lightInvalidLabel()

          // },5000)


        },

        watch:{
            my_value:function(v){
              // this.$emit('input',v)
              // update_label 可能是用在单选上面，更新_label用的，会在table组件里面显示用到。
              if(this.head.update_label){
                var item = ex.findone(this.options,{value:v})
                if(item){
                  this.row[`_${this.head.name}_label`] = item.label
                }else{
                  this.row[`_${this.head.name}_label`] =''
                }

              }
                Vue.nextTick(()=>{
                  this.lightInvalidLabel()
                  // 2023/8/11 ，如果不注释改行，启动form后，用户还没任何动作时，会自动验证（显示必填之类的提示语）, 感觉是有问题的。
                  // $(this.$el).find(`input`).trigger("validate")
                })

            }
        },

        computed:{
            // mystyle(){
            //     return {
            //       '--invalid_array':'.el-tag:nth-child(1)',
            //       '--color':'blue',
            //     }
            // },
            novalue(){
                if(this.row[this.head.name] ==0){
                    var novalue = undefined
                }else if(! this.row[this.head.name]){
                    var novalue = this.row[this.head.name]
                }else{
                    var novalue = undefined
                }
                return novalue
            },
            my_value:function(){
                return this.row[this.head.name]
            },
            is_select:function(){
                var v = this.row[this.head.name]
                if(this.head.multiple){
                  return  v.length !=0
                }else{
                  return v !== this.novalue
                }
            },
            place_value:function(){
                var v = this.row[this.head.name]
                if(v === undefined){
                    return undefined
                }else  if(v === null){
                    return null
                }else{
                    return ''
                }
            },
            invalid_options(){
                var ls= []
                if(this.head.multiple && this.my_value){
                  var valid_options = ex.map(this.normed_options,item=>item.value)
                  this.my_value.forEach(v=>{
                      if(!valid_options.includes(v)){
                        var one =  ex.findone(this.options,{value:v})
                        if(one){
                          ls.push(one)
                        }

                      }
                  })
                }
                return ls
            },

            normed_options:function(){
                /*
                 head.hide_related_field设置 隐藏与 row.hide_related_field 相等的选项

                 * */
                var self=this
                if(this.head.hide_related_field){
                    var array = ex.filter(this.options,function(item){
                        return item.value != self.row[self.head.hide_related_field]
                    })
                }else{
                    if(this.head.option_show || this.head.option_show_express ){
                      var show_express = this.head.option_show || this.head.option_show_express
                        var array = ex.filter(this.options,(item)=>{
                                    return ex.eval(show_express,{option:item,row:self.row,ps:self.parStore,vc:self})
                                })
                    }else {
                        var array = ex.filter(this.options,(item)=>{
                                    if(item.show){
                            return ex.eval(item.show,{option:item,row:self.row,ps:self.parStore,vc:self})
                        }else{
                            return true
                        }
                    })
                    }
                }
                return array

//                return self.orderBy(array,'label')

            },
            get_label(){
                var value=this.row[this.head.name]
                if(value !=0 && !value){
                    return ''
                }
                if(this.head.multiple){
                    var list = ex.map(value,item=>{
                                var option = ex.findone(this.options,{value:item})
                                if(option){
                                    return option.label
                                }else{
                                    return item
                                }


                            })
                    return list.join(';')
                } else{
                    //                var option = ex.findone(options,{value:value})
                    var option = ex.findone(this.options,{value:value})
                    if(!option){
                        return '---'
                    }else{
                        return option.label
                    }
                }

            },
        },
        methods:{
          clearOldStyle(){
            if(this.oldstyle){
              this.oldstyle.remove()
              this.oldstyle=null
            }
          },
          lightInvalidLabel(){
            if(this.head.multiple){
              this.clearOldStyle()
              if(!this.invalid_options){
                  return
              }
              console.log(`value=${this.my_value}`)
              var invalid=[]
              this.invalid_options.forEach(item=>{
                invalid.push(this.my_value.indexOf(item.value) +1)
              })
              console.log(`invalid=${invalid}`)
              var invalid_class=''
              invalid.forEach(index=>{
                if(invalid_class){
                  invalid_class +=','
                }
                invalid_class += `.${this.com_id} .el-tag:nth-child(${index}) .el-select__tags-text`
              })
              var css=  `
               ${invalid_class}{
                    color: #d96565;
                    text-decoration:line-through;
                 }`
              var style_obj = document.createElement("STYLE");
              style_obj.innerText = css;
              document.head.appendChild(style_obj);
              this.oldstyle= style_obj
            }
          },
          onAddNew(){
              ex.eval(this.head.add_express,{vc:this,row:this.row,head:this.head})
          },
            update_options:function(post_data){
              // 废弃， 使用 mounted_express 替代
                var self=this
                if(this.head.director_name){
                    cfg.show_load()
                    ex.director_call(self.head.director_name,post_data,function(data){
                        cfg.hide_load()
                        Vue.set(self.head,'options' ,data)
                    })
                }
            },

            orderBy:function(array,key){
                if(this.head.order || this.cfg.order){
                    return order_by_key(array,key)
                }else{
                    return array
                }

            }
        }
    }
</script>
<style scoped lang="scss">
.com-field-select{
    .novalue{
        color: #b7b7b7;
    }
    option{
        color: black;
    }

  //.isempty

   /deep/{
      .el-select.start > .el-input > input {
        // 遇到multiple的时候开启
        //min-height:34px!important;
      }
    }


  ::v-deep{
        //.el-tag:nth-child(1) .el-select__tags-text{
        //  color: darkred;
        //}

        //.el-tag:nth-child(1){
        //  .el-select__tags-text{
        //    color: var(--color);
        //  }
        //}

      .el-tag.invalid{
          .el-select__tags-text{
            color: yellow;
          }
        }
      //var(--invalid_array){
      //  .el-select__tags-text{
      //    color: yellow;
      //  }
      //}



      }

 }

</style>
<style lang="scss">
// 输入框可以换行的时候，把下拉框的选择项隐藏。
// 如果输入框不能换行，比如是用count来计数，所以下拉框的选择项不能隐藏
.com-field-select-wrap.el-select-dropdown.is-multiple li.selected{
    display: none;
  }

.com-filter-multi-select{
    .el-select-dropdown.is-multiple li.selected{
        display: block;
    }
}
</style>

