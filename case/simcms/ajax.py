from .base_data import cms_page

def get_global(): 
    return globals()

def get_cms_content_fields_ctx(name): 
    return cms_page[name].get_head_context()
