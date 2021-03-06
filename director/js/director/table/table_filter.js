/**
 >5>front/table.rst>

 table的过滤器
 ============
 ::

 class SalaryFilter(RowFilter):
 names=['is_checked']
 range_fields=[{'name':'month','type':'month'}]
 model=SalaryRecords


 <-<
 */
import * as com_search from './filters/com_search.js'
import * as com_search_select from './filters/com_search_select.js'

import * as com_select from './filters/com_select.js'
//import * as com_date_range from './filters/com_date_range.js'
import * as related_select from './filters/related_select.js'
import * as date_datetimefield_range from './filters/date_datetimefield_range'
//import * as filter_search_select from './filters/filter_search_select'
import * as filter_date from './filters/filter_date'
import * as filter_single_select2 from './filters/filter_single_select2'


require('./scss/table_filter.scss')

Vue.component('com-filter',{
    /*
    * 过滤器的 容器
    * */
    props:['heads','search_args'],
    template:`<div v-if='heads.length>0' class="com-filter flex flex-grow flex-ac" >
            <com-auto-more org-height="2.8em">
                <div class="flex" style="flex-wrap: wrap;padding: 0.3em">
                     <div v-for="filter in heads" :id="'filter-'+filter.name" class="filter-item" style="margin-bottom: 0.3em">
                            <component @submit="m_submit()" :is="filter.editor" :head="filter" :search_args='search_args' > </component>
                     </div>
                </div>
            </com-auto-more>

                <button name="go" type="button" class="btn btn-success btn-sm" @click='m_submit()' >
                  <i class="fa fa-search"></i>
                  <span v-text="search_lable"></span>
                </button>
        </div>
    `,
    created:function(){
        var self=this
        ex.each(self.heads,function(filter){
            if(ex.isin(filter.type,['month','date'])){
                if(!self.search['_start_'+filter.name]){
                    Vue.set(self.search,'_start_'+filter.name,'')
                }
                if(!self.search['_end_'+filter.name]){
                    Vue.set(self.search,'_end_'+filter.name,'')
                }

            }
        })
    },
    computed:{
        search_lable:function(){
            return cfg.tr.search
        }
    },
    methods:{
        m_submit:function () {
            this.$emit('submit')
        },
        orderBy:function (array,key) {
            return  array.slice().sort(function (a,b) {
                if(isChinese(a[key])&&isChinese(b[key])){
                    return a[key].localeCompare(b[key],'zh')
                }else{
                    return compare(a[key],b[key])
                }
            })
        },
    }
})





var sim_filter_with_search={
    props:['filter','value'],
    data:function(){
        return{
            myvalue:this.value
        }

    },
    mounted:function(){
        var self=this
        ex.load_js("/static/lib/bootstrap-select.min.js",function(){
            $(self.$el).selectpicker()
        })
        ex.load_css("/static/lib/bootstrap-select.min.css")
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)
        }
    },
    methods:{
        orderBy:function (array,key) {
            return  array.slice().sort(function (a,b) {
                if(isChinese(a[key])&&isChinese(b[key])){
                    return a[key].localeCompare(b[key],'zh')
                }else{
                    return compare(a[key],b[key])
                }
            })
        },
    },
    template:`<select class="selectpicker form-control"  data-live-search="true" v-model='myvalue'>
        <option :value="undefined" v-text='filter.label'></option>
        <option value="">-------</option>
        <option v-for='option in orderBy( filter.options,"label")' :value="option.value"
           :data-tokens="option.label" v-text='option.label'>
        </option>
        </select>
    `
}
Vue.component('sel-search-filter',sim_filter_with_search)

