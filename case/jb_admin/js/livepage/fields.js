// import {fields_all_in_one} from '../misc/form_one.js'
// 2023-12-1日改为引入formOne。注释掉了../misc/form_one.js文件，如果后面调试不通，可以恢复 form_one.js文件
import formOne from "../misc/formOne.vue";
var live_fields={
    props:['ctx'],
    basename:'live-fields',
    // mixins:[fields_all_in_one]
    mixins:[formOne]
}

window.live_fields = live_fields