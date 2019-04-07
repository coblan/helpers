function isChinese(temp){
    var re=/[^\u4E00-\u9FA5]/;
    if (re.test(temp[0])){return false  ;}
    return true ;
}
function compare(temp1, temp2) {
    if (temp1 < temp2) {
        return -1;
    } else if (temp1 == temp2) {
        return 0;
    } else {
        return 1;
    }
}

export function	sortOrder (array,key) {

    return  array.slice().sort(function (a,b) {
        if(key){
           var val_a=a[key]
            var  val_b=b[key]
        }else{
            var  val_a=a
            var  val_b=b
        }
        if(isChinese(val_a)&&isChinese(val_b)){
            return val_a.localeCompare(val_b,'zh')
        }else{
            return compare(val_a,val_b)
        }
    })
}