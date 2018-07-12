
/*
 >->front/fields.rst>
 =========
 fields
 =========

 fields模块的目标是利用vuejs快速生成form表单。

 主要结构
 ===========
 1. field_base
 基类，包括操作逻辑，专用input组件。如果需要修改整个field的外观，可以继承field_base，然后自定义wrap template

 2. field
 wrap功能，在field_base外面套上了一层外观template，例如label，error,help_text等的显示。

 参数结构
 ==============
 field_base的参数都是采用的关键字参数，结构如下：
 使用的 kw 结构
 kw={
 errors:{},
 row:{
 username:'',
 password:'',
 pas2:'',
 },
 heads:[
 {name:'username',label:'用户名',type:'text',required:true,autofocus:true},
 ]
 }
 <field name='username' :kw='kw' ></field>


 <-<
 *配合jsonpost使用，效果最好
 */

/*
 自动处理form.errors
 $.post('',JSON.stringify(post_data),function (data) {
 is_valid(data.do_login,self.meta.errors,function () {
 location=next;
 })
 */

//import {use_color} from '../dosome/color.js'
//import {load_js,load_css} from '../dosome/pkg.js'
require('./scss/fields_panel.scss')

import {hook_ajax_msg,hook_ajax_csrf,show_upload,hide_upload} from './ajax_fun.js'
import * as f from './file.js'
import * as ck from './ckeditor.js'
import * as multi from './multi_sel.js'
import * as inputs from './inputs.js'
import * as ln from './link.js'
import * as form_btn from './com_form_btn.js'
//import * as fb from './field_base.js'
//import * as js from './adapt.js'
import  {field_base} from  './fields_base.js'
import  {field_fun} from './field_fun.js'
import  {order_by_key} from './order.js'

import  table_fields from  './table_fields.js'


hook_ajax_msg()
hook_ajax_csrf()



var field={
    mixins:[field_base],
    methods:{
        show_msg:function(msg,event){
            layer.tips(msg, event.target);
        }
    },
    template:`
    		<div :class='["form-group field",{"error":head.error}]' v-if="head" style="position: relative;">
                <label :for="'id_'+head.name"  class="control-label" v-if='head.label && head.label!=""'>
                    <span v-text="head.label"></span><span class="req_star" v-if='head.required'>*</span>
                </label>
                <div class="field_input">
                    <component :is='head.editor'
                        :row='row'
                        :head='head'>
                    </component>
                </div>
                <slot></slot>
                <!--<i class="help-text" v-if="head.help_text" v-text="head.help_text"></i>-->
                <span class="help-text clickable">
                    <i style="color: #3780af;position: relative;top:10px;"  v-if="head.help_text" @click="show_msg(head.help_text,$event)" class="fa fa-question-circle" ></i>
                </span>

                 <!--<div class="msg" style="position: absolute;right: 5px;top: 1px;">-->

                        <!--&lt;!&ndash;<i v-if="head.help_text" @click="show_msg(head.help_text,$event)" class="fa fa-shield" ></i>&ndash;&gt;-->

                        <!--<span class="fa-stack error" v-if="head.error" @click="show_msg(head.error,$event)" style="font-size: 0.5em;">-->
                              <!--<i class="fa fa-cloud fa-stack-2x" style="color: black"></i>-->
                              <!--<i class="fa fa-close fa-stack-1x" style="color: red"></i>-->
                        <!--</span>-->

                        <!--&lt;!&ndash;<i v-if="head.error" @click="show_msg(head.error,$event)" class="fa fa-shield  error" ></i>&ndash;&gt;-->
                        <!--&lt;!&ndash;<span class="help_text" v-text="head.help_text"></span>&ndash;&gt;-->
                        <!--&lt;!&ndash;<span v-if="head.error_msg" class="error_msg error"  v-text='head.error_msg'></span>&ndash;&gt;-->
                 <!--</div>-->
		</div>


	`,

}

Vue.component('field',field)



window.field_fun=field_fun
window.hook_ajax_msg=hook_ajax_msg
//window.update_vue_obj=update_vue_obj
//window.use_ckeditor= ck.use_ckeditor
window.show_upload =show_upload
window.hide_upload =hide_upload
//window.merge=merge;
//window.BackOps=BackOps
//window.back_ops=back_ops
window.order_by_key=order_by_key

