from django.shortcuts import render, Http404
from .models import CmsPageModel
from .base_data import cms_page
import json

# Create your views here.

def cms_view(request, name): 
    try:
        page = CmsPageModel.objects.get(name = name)
    except CmsPageModel.DoesNotExist:
        raise Http404('页面不存在')
    if page.content:
        page_data = json.loads(page.content)
    else:
        page_data = {}
    par_chain = []
    par_ctx = get_par_ctx(page, request, par_chain)
    pageCls = cms_page.get( page.temp_cls )
    page_obj = pageCls(request )
    
    ctx = page_obj.mergeCtx(par_ctx, page_data)
    
    return page_obj.render(ctx)

def get_par_ctx(page, request, par_chain): 
    if page in par_chain:
        return {}
    else:
        par_chain.append(page)
        
    if page.par:
        par_par_ctx = get_par_ctx(page.par, request, par_chain)
        par_obj = cms_page.get( page.par.temp_cls )(request)
        par_content = json.loads( page.par.content )
        
        ctx = par_obj.mergeCtx(par_par_ctx, par_content)
        return ctx
    else:
        return {}
    