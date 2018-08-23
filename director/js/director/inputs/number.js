var number = {
    props:['row','head'],

        template: `<div><span v-if='head.readonly' v-text='row[head.name]'></span>
            		<input v-else type="number" class="form-control input-sm" v-model="row[head.name]" :id="'id_'+head.name"
            		    :name="head.name" :step="head.step"
                        :placeholder="head.placeholder" :autofocus="head.autofocus"></div>`
}

Vue.component('com-field-number',number)