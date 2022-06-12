import cfg from 'weblib/pc_cfg'
if(!window.cfg){
    window.cfg = cfg
    cfg.js_lib = js_config.js_lib
    cfg.ui_editor ={}
    cfg.bus = new Vue()
}
import  ex from 'weblib/ex'
if(!window.ex){
    window.ex = ex
}