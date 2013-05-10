from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from coffin.shortcuts import render_to_response
from csmapper import forms
import csmap
import pdb


def index(request):
    upload_form = forms.UploadFileForm()
    return render_to_response('csmapper/index.jinja2',
                              {'upload_error': False,
                               'upload_form': upload_form},
                              context_instance=RequestContext(request))


def upload(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            score_filepath = {'ucsc15': settings.CSMAP_SCOREDATA_UCSC15,
                              'vista12': settings.CSMAP_SCOREDATA_VISTA12,
                              'vista6': settings.CSMAP_SCOREDATA_VISTA6}

            if request.POST.get('partial') == 'on':
                partial = True
            else:
                partial = False

            csmap_result, error_line = csmap.parse(request.FILES['upload_file'],
                                                   score_filepath.get(request.POST.get('score_data')),
                                                   partial)

            if csmap_result is None:
                # Format Error
                upload_form = forms.UploadFileForm()
                return render_to_response('csmapper/index.jinja2',
                                          {'error_line': error_line,
                                           'upload_form': upload_form},
                                          context_instance=RequestContext(request))

            else:
                response = HttpResponse(csmap_result, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=%s' % request.POST.get('score_data') + '_score.txt'
                return response
        else:
            return HttpResponseRedirect('/bioweb/csmapper/')
    else:
        return HttpResponseRedirect('/bioweb/csmapper/')
