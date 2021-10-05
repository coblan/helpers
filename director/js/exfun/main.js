import {old} from './old.js'
import {network} from './network.js'
import {urlparse} from './urlparse.js'
//import {collection} from  './collection.js'
import * as path from './patch.js'
import {cookie} from './cookie.js'
import {obj_control} from  './obj'
import {vuetool} from  './vuetools'
import {code} from  './code'
import {sortOrder} from  './order'
import {layout} from  './layout'
import {file_proc} from  './file_proc'
// import {rabbit} from  './rabbit'
import {rabbit} from  'weblib/ex/rabbit'
import {sys} from  './sys'
import  * as defPromise from  './defPromise'
import  {os} from  './os'
import {localCatch} from  './catch'
import {utile} from  './utile'

import {collection} from  'weblib/ex/collection.js'
var dayjs = require('dayjs')

var ex={
    assign:function (dst,src) {
        for(var key in src){
            dst[key]=src[key]
        }
        return dst
    },
    dayjs:dayjs,
    count:0,
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
ex.assign(ex,file_proc)
ex.assign(ex,rabbit)
ex.assign(ex,sys)
ex.assign(ex,localCatch)
ex.assign(ex,utile)
ex.os = os
ex.sortOrder=sortOrder
ex.DefPromise = defPromise.default
//ex.md5=md5
window.ex = ex


import * as uis from  './uis/main.js'
import * as cfg from './cfg.js'