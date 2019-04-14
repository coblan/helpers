Vue.component('com-field-phone',{
    props:['head','row'],
    template:` <van-field class="com-field-linetext" v-model="row[head.name]" type="tel"
    center
    clearable
    :label="head.label"
    :placeholder="head.placeholder || '请输入'+head.label"
  ></van-field>`
})