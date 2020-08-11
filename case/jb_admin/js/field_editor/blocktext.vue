
<template>
    <div class="com-field-blocktext">
        <pre class="mypre" v-if='head.readonly' v-text='row[head.name]'></pre>
            <textarea :style="head.style" v-else :maxlength="head.maxlength" class="form-control input-sm"
                      :name="head.name"
                      :id="'id_'+head.name" v-model="row[head.name]" :placeholder="head.placeholder"
                      :readonly='head.readonly'></textarea>
    </div>
</template>
<script>
export default {
    props:['row','head'],
}
</script>
<style scoped lang="scss">
    .mypre {
        white-space: pre-wrap;
        word-wrap: break-word;
        border: none;
    }
</style>

Vue.component('com-field-blocktext',{
        props:['row','head'],
        template: ``,
})