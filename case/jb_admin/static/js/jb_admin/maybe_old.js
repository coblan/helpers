(window.webpackJsonp=window.webpackJsonp||[]).push([["maybe_old"],{210:function(e,t,n){"use strict";n.r(t),n.d(t,"com_sim_fields",(function(){return s})),n(87);var s={props:{heads:"",row:"",okBtn:{default:function(){return"确定"}},crossBtn:"",autoWidth:{default:function(){return!0}},btnCls:{default:function(){return"btn-primary btn-sm"}}},data:function(){return{env:cfg.env,small:!1}},mounted:function(){},watch:{},computed:{small_srn:function(){return this.env.width<760},label_width:function(){this.autoWith;var e=4;return ex.each(this.heads,(function(t){e<t.label.length&&(e=t.label.length)})),{width:(e+=1)+"em"}}},components:window._baseInput,mixins:[mix_fields_data,mix_nice_validator],template:' <div :class="[\'field-panel sim-fields\',]"\n    style="text-align:center;">\n           <table class="table-fields">\n        <tr v-for="head in normed_heads">\n            <td class="field-label-td"  valign="top" >\n            <div class="field-label" :style="label_width">\n                <span class="label-content">\n                     <span v-text="head.label"></span>\n                     <span class="req_star" v-if=\'head.required\'>*</span>\n                </span>\n            </div>\n\n            </td>\n            <td class="field-input-td" >\n                <div class="field-input">\n                    <component v-if="head.editor" :is="head.editor"\n                         @field-event="$emit(\'field-event\',$event)"\n                         :head="head" :row="row"></component>\n\n                </div>\n            </td>\n            <td>\n                <span v-if="head.help_text" class="help-text clickable">\n                            <i style="color: #3780af;position: relative;top:10px;"   @click="show_msg(head.help_text,$event)" class="fa fa-question-circle" ></i>\n                </span>\n            </td>\n        </tr>\n        <slot :row="row">\n            \x3c!--按钮横跨两列 ！小尺寸时 强制 --\x3e\n             <tr v-if="crossBtn || small_srn" class="btn-row">\n                <td class="field-input-td" colspan="3">\n                    <div class="submit-block">\n                        <button @click="panel_submit" type="btn"\n                            :class="[\'form-control btn\',btnCls]"><span v-text="okBtn"></span></button>\n                    </div>\n                </td>\n            </tr>\n            \x3c!--按钮在第二列--\x3e\n               <tr v-else class="btn-row">\n                   <td class="field-label-td"></td>\n                    <td class="field-input-td" colspan="1">\n                        <div class="submit-block">\n                            <button @click="panel_submit" type="btn"\n                                :class="[\'btn\',btnCls]"><span v-text="okBtn"></span></button>\n                        </div>\n                     </td>\n                     <td></td>\n               </tr>\n        </slot>\n\n    </table>\n\n\n        </div>',methods:{update_small:function(){var e=this;$(e.$el).width()<450?e.small=!0:e.small=!1,setTimeout((function(){e.update_nice()}),100)},panel_submit:function(){this.$listeners&&this.$listeners.submit?this.isValid()&&this.$emit("submit",this.row):this.submit()},show_msg:function(e,t){layer.tips(e,t.target)},after_save:function(e){this.$emit("after-save",e)}}}},260:function(e,t,n){"use strict";n.r(t),n.d(t,"suit_fields",(function(){return s}));var s={props:["row","heads","ops"],mixins:[n(210).com_sim_fields],template:'<div class="flex-v" style="margin: 0;height: 100%;">\n    <div class = "flex-grow" style="overflow: auto;margin: 0;">\n        <div class="field-panel suit" >\n            <field  v-for="head in normed_heads" :key="head.name" :head="head" :row="row"></field>\n        </div>\n      <div style="height: 1em;">\n      </div>\n    </div>\n    <slot>\n         <div style="text-align: right;padding: 8px 3em;">\n         <button @click="submit" type="btn"\n                            :class="[\'btn\',btnCls]"><span v-text="okBtn">保存</span></button>\n        \x3c!--<component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>--\x3e\n        </div>\n    </slot>\n\n     </div>'}},261:function(e,t,n){"use strict";n.r(t);var s=n(0),a=n.n(s),i=n(262),o={insert:"head",singleton:!1};a()(i.a,o);t.default=i.a.locals||{}},262:function(e,t,n){"use strict";var s=n(1),a=n.n(s)()((function(e){return e[1]}));a.push([e.i,".com-fields-table-block.field-panel{background-color:#fafafa;padding:5px 20px;position:relative;border:1px solid #f6f6f6}.com-fields-table-block.field-panel td{padding:8px 5px;position:relative}.com-fields-table-block.field-panel td .field-label{font-weight:bold}.com-fields-table-block .field-label{display:flex}.com-fields-table-block .field-label .label-content{min-width:4em}.com-fields-table-block .field-label .req_star{position:relative;color:#f00}.com-fields-table-block .field-input{position:relative;display:flex}.com-fields-table-block .field-input .help-text{display:inline-block;padding:0 3px;position:relative;top:6px}.com-fields-table-block .field-input span.readonly-info{color:#808080;height:30px;display:inline-block;padding:3px;line-height:26px}",""]),t.a=a},263:function(e,t,n){"use strict";var s=n(1),a=n.n(s)()((function(e){return e[1]}));a.push([e.i,"\n.div-item[data-v-e5597960]{margin:2px;vertical-align:top\n}\n",""]),t.a=a},264:function(e,t,n){"use strict";function s(e){return e.search_args=e.search_args||{},e.row_sort=e.row_sort||{sortable:[]},e.footer=e.footer||[],e.ops=e.ops||[],e.row_pages=e.row_pages||{crt_page:1,total:0,perpage:20},e.row_filters=e.row_filters||[],e.director_name=e.director_name||"",null==e.selectable&&(e.selectable=!0),e}n.r(t),n.d(t,"init_table_ctx",(function(){return s})),n.d(t,"ele_table",(function(){return a})),n.d(t,"ele_operations",(function(){return i})),n.d(t,"ele_filter",(function(){return o})),n.d(t,"ele_page",(function(){return l}));var a={props:["bus"],created:function(){this.bus.table=this},data:function(){return{heads:this.bus.heads,search_args:this.bus.search_args,row_sort:this.bus.row_sort}},mounted:function(){this.bus.eventBus.$on("search",this.bus_search),this.bus.eventBus.$on("pageindex-change",this.get_page),this.bus.eventBus.$on("operation",this.on_operation),this.bus.eventBus.$on("perpage-change",this.on_perpage_change)},methods:{bus_search:function(e){ex.assign(this.search_args,e),this.search()}},computed:{rows:{get:function(){return this.bus.rows},set:function(e){this.bus.rows=e}},footer:{get:function(){return this.bus.footer},set:function(e){this.bus.footer=e}}},mixins:[mix_table_data,mix_ele_table_adapter],template:'  <el-table class="table flat-head" ref="e_table"\n                              :data="rows"\n                              border\n                              show-summary\n                              :fit="false"\n                              :stripe="true"\n                              size="mini"\n                              @sort-change="sortChange($event)"\n                              @selection-change="handleSelectionChange"\n                              :summary-method="getSum">\n                        <el-table-column v-if="bus.selectable"\n                                type="selection"\n                                width="55">\n                        </el-table-column>\n\n                        <template  v-for="head in heads">\n\n                            <el-table-column v-if="head.editor"\n                                             :show-overflow-tooltip="is_show_tooltip(head) "\n                                             :label="head.label"\n                                             :prop="head.name.toString()"\n                                             :sortable="is_sort(head)"\n                                             :width="head.width">\n                                <template slot-scope="scope">\n                                    <component :is="head.editor"\n                                               @on-custom-comp="on_td_event($event)"\n                                               :row-data="scope.row" :field="head.name" :index="scope.$index">\n                                    </component>\n\n                                </template>\n\n                            </el-table-column>\n\n                            <el-table-column v-else\n                                             :show-overflow-tooltip="is_show_tooltip(head) "\n                                             :prop="head.name.toString()"\n                                             :label="head.label"\n                                             :sortable="is_sort(head)"\n                                             :width="head.width">\n                            </el-table-column>\n\n                        </template>\n\n                    </el-table>\n'},i={props:["bus"],template:'<div class="oprations" style="padding: 5px;">\n                <component v-for="op in ops"\n                           :is="op.editor"\n                           :ref="\'op_\'+op.name"\n                           :head="op"\n                           @operation="on_operation(op)"></component>\n            </div>',data:function(){return{ops:this.bus.ops}},methods:{get_attr:function(e){return this.bus.table.get_attr(e)},on_operation:function(e){this.bus.eventBus.$emit("operation",e)}}},o={props:["bus"],computed:{},template:' <com-filter class="flex" :heads="bus.row_filters" :search_args="bus.search_args"\n                        @submit="search()"></com-filter>',methods:{search:function(){this.bus.eventBus.$emit("search",this.bus.search_args)}}},l={props:["bus"],data:function(){return{row_pages:this.bus.row_pages,search_args:this.bus.search_args}},methods:{on_page_change:function(e){this.bus.eventBus.$emit("pageindex-change",e)},on_perpage_change:function(e){this.bus.eventBus.$emit("perpage-change",e)}},template:' <el-pagination\n                         @size-change="on_perpage_change"\n                        @current-change="on_page_change"\n                        :current-page="row_pages.crt_page"\n                        :page-sizes="[20, 50, 100]"\n                        :page-size="row_pages.perpage"\n                        layout="total, sizes, prev, pager, next, jumper"\n                        :total="row_pages.total">\n                </el-pagination>'}},265:function(e,t,n){"use strict";n.r(t),t.default={props:["tab_head","par_row"],data:function(){var e=this,t=this.tab_head.table_ctx,n={data:function(){return{head:t,heads:t.heads,row_filters:t.row_filters,row_sort:t.row_sort,director_name:t.director_name,footer:t.footer||[],ops:t.ops||[],rows:[],row_pages:{},selectable:null==t.selectable||t.selectable,advise_heads:t.advise_heads||[],selected:[],del_info:[],search_args:t.search_args||{},vc:e,parStore:ex.vueParStore(e)}},mixins:[table_store],watch:{search_args:function(e){console.log(e)}},methods:{switch_to_tab:function(e){window.root_live?table_store.methods.switch_to_tab(e):this.parStore.switch_to_tab(e)},getRows:function(){if(e.tab_head.filter_express){var t=ex.eval(e.tab_head.filter_express,{par_row:e.par_row,vc:e,ps:this});ex.assign(this.search_args,t)}else if(e.tab_head.pre_set){var n=ex.eval(e.tab_head.pre_set,{par_row:e.par_row,vc:e,ps:this});ex.assign(this.search_args,n)}else e.tab_head.tab_field?this.search_args[e.tab_head.tab_field]=e.par_row[e.tab_head.par_field]:e.tab_head.par_field&&(this.search_args[e.tab_head.par_field]=e.par_row[e.tab_head.par_field]);table_store.methods.getRows.call(this)}}};return{childStore:new Vue(n),parStore:ex.vueParStore(e),loaded:!1}},mounted:function(){var e=this;ex.vueEventRout(this,this.tab_head.event_slots),this.childStore.head.init_express||Vue.nextTick((function(){e.childStore.search()})),this.tab_head.mounted_express&&ex.eval(this.tab_head.mounted_express,{vc:this,ps:this.parStore,cs:this.childStore,par_row:this.par_row})},methods:{on_show:function(){}},template:'<div class="com-tab-table flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;">\n       <div v-if="childStore.row_filters.length > 0"\n       style="background-color: #fbfbf8;padding: 2px 1em;border-radius: 4px;border-bottom: 1px solid  #ebebeb;">\n            <com-table-filters></com-table-filters>\n        </div>\n        <div  v-if="childStore.ops.length>0 ">\n            <com-table-operations></com-table-operations>\n        </div>\n\n        <div v-if="childStore.parents.length>0">\n            <com-table-parents></com-table-parents>\n        </div>\n\n        \x3c!--<ol v-if="parents.length>0" class="breadcrumb jb-table-parent">--\x3e\n            \x3c!--<li v-for="par in parents"><a href="#" @click="get_childs(par)"  v-text="par.label"></a></li>--\x3e\n        \x3c!--</ol>--\x3e\n\n        <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">\n            <div class="table-wraper flex-grow" style="position: relative;">\n                <com-table-rows></com-table-rows>\n               </div>\n        </div>\n        <div style="background-color: white;">\n            <com-table-pagination></com-table-pagination>\n        </div>\n    </div>'}},272:function(e,t,n){"use strict";n.r(t),t.default={props:["ctx"],data:function(){var e=this;null==this.ctx.selectable&&(this.ctx.selectable=!0);var t={props:["ctx"],propsData:{ctx:e.ctx},data:function(){return{head:e.ctx,vc:e,par_row:e.ctx.par_row||{},heads:e.ctx.heads||[],selectable:e.ctx.selectable,search_args:e.ctx.search_args||{},row_filters:e.ctx.row_filters||{},row_sort:e.ctx.row_sort||{sortable:[]},director_name:e.ctx.director_name||"",ops:e.ctx.ops||[],row_pages:e.ctx.row_pages||{crt_page:1,total:0,perpage:20},rows:[],footer:[],selected:[]}},mixins:[table_store]},n=this.get_custom_store(t);return{childStore:new Vue(n),par_row:this.ctx.par_row||{},del_info:[]}},mixins:[mix_table_data,mix_ele_table_adapter],mounted:function(){this.childStore.$on("finish",this.emit_finish),this.ctx.event_slots&&ex.vueEventRout(this,this.ctx.event_slots),this.ctx.mounted_express?ex.eval(this.ctx.mounted_express,{vc:this}):(this.ctx.autoload||null==this.ctx.autoload)&&this.childStore.search()},methods:{get_custom_store:function(e){return e},emit_finish:function(e){this.$emit("finish",e)}},template:'<div class="com-table-panel" style="height: 100%;">\n\n            <div class="rows-block flex-v" style="height: 100%">\n\n\n              <div v-if="childStore.row_filters.length > 0" style="background-color: #fbfbf8;padding: 8px 1em;border-radius: 4px;margin-top: 8px">\n\n                     <com-table-filters></com-table-filters>\n\n               </div>\n\n               \x3c!--<div  v-if="childStore.ops.length>0 && childStore.tab_stack.length ==0">--\x3e\n               <div  v-if="childStore.ops.length>0">\n                        <com-table-operations></com-table-operations>\n               </div>\n\n                <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">\n                    <div class="table-wraper flex-grow" style="position: relative;">\n\n                        <com-table-rows></com-table-rows>\n                    </div>\n                </div>\n            <div style="background-color: white;">\n                <com-table-pagination></com-table-pagination>\n            </div>\n\n        </div>\n    </div>'}},273:function(e,t,n){"use strict";n.r(t);var s=n(86);t.default={props:["ctx"],data:function(){return{fields_editor:this.ctx.fields_editor||com_pop_field}},mixins:[s.a],template:'<div :class="[\'flex-v com-fields-panel\',cssCls,{\'small_srn\':small_srn}]" style="height: 100%">\n     <component class="msg-bottom"  :is="fields_editor" :heads="heads" :row="row" :ops="ops"\n       :cross-btn="crossBtn" @finish="on_finish($event)"></component>\n     </div>'}},274:function(e,t,n){"use strict";n.r(t);var s=n(210);t.default={mixins:[s.com_sim_fields],methods:{submit:function(){this.isValid()&&this.$emit("finish",this.row)}}}},275:function(e,t,n){"use strict";n.r(t);var s=n(260);t.default={mixins:[s.suit_fields],methods:{submit:function(){this.isValid()&&this.$emit("finish",this.row)}}}},276:function(e,t,n){"use strict";n.r(t),n(261),t.default={props:["heads","row","option"],template:'<div class="com-fields-table-block field-panel msg-bottom">\n           <table >\n            <tr v-for="heads_row in table_grid_heads">\n                <template v-for="head in heads_row">\n                    <td class="field-label-td" :class="head.class"  :colspan="head.label_colspan" :rowspan="head.label_rowspan">\n                        <div class="field-label">\n                            <span class="label-content">\n                                 <span v-text="head.label"></span>\n                            </span>\n                             <span class="req_star" v-if=\'head.required\'>*</span>\n                        </div>\n                    </td>\n                    <td class="field-input-td" :class="head.class" :colspan="head.colspan" :rowspan="head.rowspan">\n                        <div class="field-input">\n                            <component v-if="head.editor" :is="head.editor"\n                                 @field-event="$emit(\'field-event\',$event)"\n                                 :head="head" :row="row"></component>\n                            <span v-if="head.help_text" class="help-text clickable" @mouseenter="show_msg(head.help_text,$event)" @mouseleave="hide_msg()">\n                                 <i style="color: #3780af;"   class="fa fa-question-circle" ></i>\n                            </span>\n                        </div>\n                    </td>\n                </template>\n            </tr>\n        </table>\n       </div>',computed:{table_grid_heads:function(){var e=this,t=this.option.table_grid,n=[];return ex.each(t,(function(t){var s=[];ex.each(e.heads,(function(e){ex.isin(e.name,t)&&s.push(e)})),s&&n.push(s)})),n}},methods:{show_msg:function(e,t){this.msg_index=layer.tips(e,t.target,{time:0})},hide_msg:function(){layer.close(this.msg_index)}}}},281:function(e,t,n){"use strict";n.r(t);var s=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"com-layout-div",class:e.ctx.class},[e.ctx.label?n("b",{domProps:{textContent:e._s(e.ctx.label)}}):e._e(),e._v(" "),n("div",{staticClass:"div-wrap"},e._l(e.ctx.items,(function(e){return n(e.editor,{key:e.name,tag:"component",staticClass:"div-item",attrs:{ctx:e}})})),1)])};s._withStripped=!0;var a={props:["ctx"],mounted:function(){this.ctx.css&&ex.append_css(this.ctx.css)}},i=n(0),o=n.n(i),l=n(263),r={insert:"head",singleton:!1},c=(o()(l.a,r),l.a.locals,n(3)),d=Object(c.a)(a,s,[],!1,null,"e5597960",null);d.options.__file="layout\\layout_div.vue";t.default=d.exports}}]);