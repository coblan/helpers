from .base_data import cms_page

def get_global(): 
    return globals()

def get_cms_content_fields_ctx(name,request): 
    cmsCls=cms_page[name]
    cmsobj=cmsCls(request)
    tabs = cmsobj.get_tabs()
    if tabs:
        return {
            'tabs':tabs
        }
    else:
        field_ctx = cmsobj.get_head_context()
        return {
            'fields_ctx':field_ctx
        }
