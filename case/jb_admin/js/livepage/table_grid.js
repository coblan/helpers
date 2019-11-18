var live_table_grid={
    props:['ctx'],
    basename:'live-table-type',
    mixins:[live_table_type],
    data(){
        if(this.ctx.inn_editor){
            this.ctx.inn_editor ='com-table-layout-picture-grid'
        }
    }
}

window.live_table_grid =live_table_grid