<template>
  <div class="com-filter-date-range">
    <datetimeRange :head="head" :search_args="search_args">
      <template v-slot:start-input="def_props">
           <com-field-date :head="def_props.heads[0]" :row.sync="search_args"></com-field-date>
      </template>
      <template v-slot:end-input="def_props">
        <com-field-date :head="def_props.heads[1]" :row.sync="search_args"></com-field-date>
      </template>
    </datetimeRange>
  </div>
</template>
<script>
import datetimeRange from "./datetimeRange.vue";
export default {
  props:['head','search_args'],
  components:{
    datetimeRange
  }
}
</script>