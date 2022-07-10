import  { ref, reactive,computed ,onMounted,getCurrentInstance ,onBeforeMount} from '@vue/composition-api'

export function find_head(props){
    debugger
    var vc = getCurrentInstance()
    var head = ref({})
    var parStore = ref({})
    // onCreated(()=>{
    //
    // })

    // onCreate(()=>{
    //     debugger
    //     var aa = vc.proxy
    //     debugger
    //     console.log('create')
    // })
    // onMounted(()=>{
    //     debugger
    //     var aa = vc.proxy
    //     debugger
    // })
    onBeforeMount(()=>{
        debugger
        var table_par = vc.proxy.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        head.value = ex.findone(table_par.heads,{name:vc.proxy.field})
        parStore.value = ex.vueParStore(vc.proxy)
    })
    // const onCreate = ()=>{
    //     debugger
    //
    //     var table_par = vc.proxy.$parent
    //     while (true){
    //         if (table_par.heads){
    //             break
    //         }
    //         table_par = table_par.$parent
    //         if(!table_par){
    //             break
    //         }
    //     }
    //     head.value = ex.findone(table_par.heads,{name:vc.proxy.field})
    //     parStore.value = ex.vueParStore(vc.proxy)
    // }
    // const head =computed(()=>{
    //     var table_par = vc.proxy.$parent
    //     while (true){
    //         if (table_par.heads){
    //             break
    //         }
    //         table_par = table_par.$parent
    //         if(!table_par){
    //             break
    //         }
    //     }
    //    return ex.findone(table_par.heads,{name:vc.proxy.field})
    // })
    // const  parStore = computed(()=>{
    //     return ex.vueParStore(vc.proxy)
    // })


    // onCreated(() => {
    //     debugger
    //     var table_par = vc.proxy.$parent
    //     while (true){
    //         if (table_par.heads){
    //             break
    //         }
    //         table_par = table_par.$parent
    //         if(!table_par){
    //             break
    //         }
    //     }
    //     // this.table_par = table_par
    //     head.value  = ex.findone(vc.proxy.table_par.heads,{name:vc.proxy.field})
    //     parStore.value = ex.vueParStore(vc.proxy)
    // })

    // debugger
    // var table_par = vc.proxy.$parent
    // while (true){
    //     if (table_par.heads){
    //         break
    //     }
    //     table_par = table_par.$parent
    //     if(!table_par){
    //         break
    //     }
    // }
    // // this.table_par = table_par
    // head.value  = ex.findone(vc.proxy.table_par.heads,{name:vc.proxy.field})
    // parStore.value = ex.vueParStore(vc.proxy)

    return {
        head,
        parStore,
        // onCreate,
    }
}