from django.shortcuts import render
from .models import CmsPageModel
# Create your views here.

def cms_view(request, name): 
    page = CmsPageModel.objects.get(name = name)
    
    par_ctx = get_par_ctx(page, request)
    pageCls = page.page_cls
    page = pageCls(request)
    return page.render(par_ctx)

def get_par_ctx(page, request): 
    if page.par:
        parCls = page.par.page_cls
        par = parCls(request)
        par_par_ctx = get_par_ctx(par, request)
        ctx = dict(par_par_ctx)
        ctx.update(par.getContext())
        return ctx
    else:
        return {}
    