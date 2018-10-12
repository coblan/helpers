def qn(s):  
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%"]  
    for stuff in dirty_stuff:  
        s = s.replace(stuff,"")  
    #return "'"+s+"'"  
    return s 