from django.shortcuts import render
from .models import CmsPageModel
from .base_data import cms_page
import json

# Create your views here.

def cms_view(request, name): 
    page = CmsPageModel.objects.get(name = name)
    if page.content:
        page_data = json.loads(page.content)
    else:
        page_data = {}
    par_ctx = get_par_ctx(page, request)
    pageCls = cms_page.get( page.temp_cls )
    page_obj = pageCls(request )
    return page_obj.render(par_ctx, page_data)

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
    