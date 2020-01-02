<template>
    <div class="com-field-password">
        <input type="password" :id="'id_'+head.name" class="form-control input-sm" v-model="row[head.name]"
               :name="head.name" :placeholder="head.placeholder" :readonly='head.readonly'>
    </div>
</template>
<script>
    export default {
        props:['row','head'],
    }
</script>