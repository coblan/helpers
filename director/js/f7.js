
var ff={
    app:parent.myApp,
    push:function(obj){
        parent.state_stack.push(obj)
    },
    pop:function(){
        parent.state_stack.pop()
    },
    back:function(callback){
        parent.back(callback)
    },
    load:function(url,name){
        var name=name.replace(/\./g,'_')
        parent.show_load()
        parent.load_iframe(url,name)
    },
    replace:function(url){
        parent.show_load()
        parent.replace_iframe(url)
    },
    pop_menu:function(buttons){
        parent.pop_menu(buttons)
    },
    show_load:function(){
        parent.show_load()
    },
    hide_load:function(time){
        parent.hide_load(time)
    },
    init_page:function(str){
        ff.hide_load(200)
        var str= str || page_label
        parent.init_page()
        parent.set_title(str)
    },
    show_nav:function(){
        parent.show_nav()
    },
    hide_nav:function(){
        parent.hide_nav()
    },
    add_nav:function(str){
        parent.add_nav(str)
    },
    alert:function(str){
        parent.myApp.alert(str)
    },
    confirm:function(info,callback){
        parent.myApp.confirm(info, callback);
    },
    open_image:function(str){
        var myPhotoBrowser = parent.myApp.photoBrowser({
            zoom: 400,
            photos: [str]
        });
        myPhotoBrowser.open(); // open photo browser
        ff.push(function(){
            myPhotoBrowser.close()
        })
    }

}

if(!parent.myApp){
  var  ff={
        app:{
            actions:function(){

            }
        },
        push:function(obj){
        },
        pop:function(){
        },
        back:function(callback){
        },
        load:function(url,name){
            location=url
        },
        replace:function(url){
            location=url
        },
        pop_menu:function(buttons){

        },
        show_load:function(){
        },
        hide_load:function(time){
        },
        init_page:function(){
        },
        show_nav:function(){
        },
        hide_nav:function(){
        },
        add_nav:function(str){
        },
        alert:function(str){
            alert(str)
        },
        confirm:function(info,callback){
            confirm(info, callback);
        },
        open_image:function(str){
            alert(str)
        }
    }
}

window.ff=ff