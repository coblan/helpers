
<template lang="pug">
div.com-field-blocktext(:class="head.class")
    pre.mypre(v-if='head.readonly' v-text='row[head.name]')
    textarea.form-control.input-sm(v-else :style="head.style" :maxlength="head.maxlength" :name="head.name" :id="'id_'+head.name" v-model="row[head.name]" :placeholder="head.placeholder" :readonly='head.readonly')

</template>
<!--<template>-->
    <!--<div class="com-field-blocktext" :class="head.class">-->
        <!--<pre class="mypre" v-if='head.readonly' v-text='row[head.name]'></pre>-->
            <!--<textarea :style="head.style" v-else :maxlength="head.maxlength" class="form-control input-sm"-->
                      <!--:name="head.name"-->
                      <!--:id="'id_'+head.name" v-model="row[head.name]" :placeholder="head.placeholder"-->
                      <!--:readonly='head.readonly'></textarea>-->
    <!--</div>-->
<!--</template>-->
<script>
export default {
    props:['row','head'],
    mounted(){
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,})
        }
        if(this.head.css){
            ex.append_css(this.head.css)
        }
    }
}
</script>
<style scoped lang="scss">
    .mypre {
        white-space: pre-wrap;
        word-wrap: break-word;
        border: none;
    }
</style>
