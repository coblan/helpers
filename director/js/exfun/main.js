import {old} from './old.js'
import {network} from './network.js'
import {urlparse} from './urlparse.js'
import {collection} from  './collection.js'
import * as path from './patch.js'
import {cookie} from './cookie.js'
import {obj_control} from  './obj'
import {vuetool} from  './vuetools'
import {code} from  './code'
import {sortOrder} from  './order'
import {layout} from  './layout'
var ex={
    assign:function (dst,src) {
        for(var key in src){
            dst[key]=src[key]
        }
    },
}

//import {md5} from  './md5.min'

ex.assign(ex,old)
ex.assign(ex,network)
ex.assign(ex,urlparse)
ex.assign(ex,collection)
ex.assign(ex,cookie)
ex.assign(ex,obj_control)
ex.assign(ex,vuetool)
ex.assign(ex,code)
ex.assign(ex,layout)
ex.sortOrder=sortOrder

//ex.md5=md5
window.ex = ex



import * as cfg from './cfg.js'
import * as uis from  './uis/main.js'