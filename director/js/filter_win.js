export  function open(info,callback){
   var filter_logic={
        el:'#filter-block',
        data:{
            row_filters:info.row_filters,
            search_args:info.search_args,
            search_tip:info.search_tip,
        },
        mixins:[popup_page],
        methods:{
            selector:function(){
                return '.popup-filter'
            },
            assure:function(){
                this.search()
                this.close()
            },
            search:function () {
                setTimeout(function(){
                    callback(this.search_args)
                    //parent.replace_iframe(ex.appendSearch(search_args))
                },300)
            },

        },
    }
    var mount_str=`<div id="filter-block">
        <div class="popup popup-filter">
            <div class="content-block">
                <com-filter :row_filters="row_filters" :search_args="search_args" :search_tip='search_tip'></com-filter>
            </div>
        </div>
        </div>`

    new Vue(filter_logic)

}


