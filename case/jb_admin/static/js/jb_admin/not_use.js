(window.webpackJsonp=window.webpackJsonp||[]).push([["not_use"],{230:function(e,a,t){"use strict";t.r(a);var s=t(0),o=t.n(s),i=t(231),d={insert:"head",singleton:!1};o()(i.a,d);a.default=i.a.locals||{}},231:function(e,a,t){"use strict";var s=t(1),o=t.n(s)()((function(e){return e[1]}));o.push([e.i,".com-tab-fields .oprations{background:#fbfbf8;padding:0.2rem 1rem;margin:0.2rem 0;border-bottom:1px solid #cccccc}.com-tab-fields .table-fields{border:1px solid #efefef;background-color:#f8f8f8;margin:5px 15px;padding:10px 30px}.fields-group-title{padding:.3rem 0 .3rem 2rem;font-size:120%;color:gray}\n",""]),a.a=o},275:function(e,a,t){"use strict";t.r(a),t(230),a.default={props:["tab_head","par_row"],data:function(){var e=this.tab_head.row||{},a=new Vue({data:{vc:this}}),t=ex.vueParStore(this);return{head:this.tab_head,heads:this.tab_head.heads||this.tab_head.fields_ctx.heads,ops:this.tab_head.ops||this.tab_head.fields_ctx.ops,errors:{},row:e,org_row:e,childStore:a,parStore:t}},mixins:[mix_fields_data,mix_nice_validator],template:'<div class="com-tab-fields flex-v"  style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;">\n\n   <div class="oprations" >\n        <component v-for="op in ops" :is="op.editor" :ref="\'op_\'+op.name" :head="op" :ctx="op" @operation="on_operation(op)"></component>\n    </div>\n    <div style="overflow: auto;" class="flex-grow fields-area">\n        <div v-if="heads[0].name !=\'_meta_head\'" class=\'field-panel suit\' id="form" >\n            <field  v-for=\'head in normed_heads\' :key="head.name" :head="head" :row=\'row\'></field>\n        </div>\n        <template v-else>\n               <div v-if="heads[0].fields_group" :class="heads[0].class">\n                    <div v-for="group in heads[0].fields_group" :class="\'group_\'+group.name">\n                        <div class="fields-group-title" v-html="group.label"></div>\n                        <com-fields-table-block v-if="heads[0].table_grid"\n                            :heads="group_filter_heads(group)" :meta-head="heads[0]" :row="row">\n                            </com-fields-table-block>\n                         <div v-else class=\'field-panel suit\' id="form" >\n                            <field  v-for=\'head in group_filter_heads(group)\' :key="head.name" :head="head" :row=\'row\'></field>\n                       </div>\n                    </div>\n                </div>\n                <div v-else :class="heads[0].class">\n                    <com-fields-table-block v-if="heads[0].table_grid"\n                        :heads="normed_heads.slice(1)" :row="row" :metaHead="heads[0]"></com-fields-table-block>\n                </div>\n        </template>\n\n\n    </div>\n    </div>',mounted:function(){this.heads[0]&&"_meta_head"==this.heads[0].name&&this.heads[0].style&&ex.append_css(this.heads[0].style),this.tab_head.row||this.get_data(),ex.vueEventRout(this,this.tab_head.event_slots)},methods:{back:function(){this.parStore.pop_tab_stack()},group_filter_heads:function(e){return ex.filter(this.normed_heads,(function(a){return ex.isin(a.name,e.head_names)}))},data_getter:function(){var e=this;if(e.tab_head.get_data){var a=s[e.tab_head.get_data.fun],t=e.tab_head.get_data.kws;a(e,(function(a){e.org_row=a,e.row=ex.copy(a),e.childStore.$emit("row.update_or_insert",a)}),t)}},after_save:function(e){this.tab_head.after_save?"string"==typeof this.tab_head.after_save?ex.eval(this.tab_head.after_save,{vc:this}):(this.tab_head.after_save&&this.parStore&&this.parStore.update_or_insert(e),ex.vueAssign(this.org_row,e)):this.tab_head.after_save_express?ex.eval(this.tab_head.after_save_express,{vc:this}):this.parStore.update_or_insert(e)}}};var s={get_row:function(e,a,t){var s=t.director_name,o=t.relat_field,i={director_name:s};i[o]=e.par_row[o],cfg.show_load(),ex.director_call("d.get_row?dname="+s,i).then((function(e){cfg.hide_load(),a(e)}))},table_row:function(e,a,t){a(e.par_row)}}}}]);