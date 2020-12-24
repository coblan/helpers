export function find_par(self){

        var table_par = self.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        self.table_par = table_par
        self.head = ex.findone(self.table_par.heads,{name:self.field})
    }
