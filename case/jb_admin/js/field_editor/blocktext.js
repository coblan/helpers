Vue.component('com-field-blocktext',{
        props:['row','head'],
        template: `<div>
            <pre v-if='head.readonly' v-text='row[head.name]'></pre>
            <textarea :style="head.style" v-else :maxlength="head.maxlength" class="form-control input-sm"
                :name="head.name"
                :id="'id_'+head.name" v-model="row[head.name]" :placeholder="head.placeholder"
                :readonly='head.readonly'></textarea>
            </div>`
})