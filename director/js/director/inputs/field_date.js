var field_date = {
    props:['row','head'],
        template:`<div><span v-if='head.readonly' v-text='row[head.name]'></span>
                                <date v-else v-model="row[head.name]" :id="'id_'+head.name"
                                    :placeholder="head.placeholder"></date>
                               </div>`,
}
Vue.component('com-field-date',field_date)