var simcms_table_logic={
    mounted:function(){
        var self=this
        ex.assign(this.op_funs, {
            edit_page_content: function (kws) {
                var post_data=[{fun:'get_cms_content_fields_ctx',name:kws.row.temp_cls}]
                ex.post('/d/ajax/simcms',JSON.stringify(post_data),function(resp){
                    if(kws.row.content){
                        var content_row=JSON.parse(kws.row.content)
                    }else{
                        var content_row={}
                    }

                    var cms_resp_content=resp.get_cms_content_fields_ctx
                    if(cms_resp_content.tabs){
                        self.tabgroup.tabs=cms_resp_content.tabs
                        self.crt_row=kws.row
                        self.show_tab(self.tabgroup.tabs[0].name)
                    }else{
                        var cms_content_fields_ctx = cms_resp_content.fields_ctx
                        content_row._director_name=cms_content_fields_ctx.director_name
                        content_row._page=kws.row.pk
                        pop_fields_layer(content_row,cms_content_fields_ctx,function(resp){
                            var new_row=resp.new_row
                            kws.row.content=JSON.stringify(new_row)
                            //var crt_row=ex.findone(self.rows,{pk:kws.row.pk})
                            //crt_row.content=JSON.stringify(new_row)
                        })
                    }

                })

            }
        })
    }

}
window.simcms_table_logic=simcms_table_logic