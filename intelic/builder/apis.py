from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils import simplejson
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import models, forms

def get_baselines(request):
    baselines = models.Baseline.objects.all()
    if request.REQUEST.get('q'):
        query = simplejson.loads(request.REQUEST['q'])
        baselines = baselines.filter(**query)
    return HttpResponse(serializers.serialize("json", baselines))

def get_components_form(request, template_name = 'bootstrapform/form.html'):
    baseline_pk = request.REQUEST.get('baseline_pk')
    product_pk  = request.REQUEST.get('product_pk')
    
    if not baseline_pk or not product_pk:
        return HttpResponseBadRequest('Parameters required.')
    try:
        baseline = models.Baseline.objects.get(pk = baseline_pk)
        product = models.Product.objects.get(pk = product_pk)
    except ObjectDoesNotExist, err:
        raise Http404(err)

    form_class = getattr(forms, product.form_class.name)
    form = form_class(init_baseline = baseline, init_product = product)
    return render(request, template_name, {
        'form': form,
    })

def trigger_process(request):
    try:
        pk = request.REQUEST.get('pk')
        process = models.Process.objects.get(pk = pk)
    except models.Process.DoesNotExist, err:
        raise Http404(err)
    if request.REQUEST.get('a') == 'start':
        process.start()
    if request.REQUEST.get('a') == 'cancel':
        process.cancel()
    return HttpResponse(simplejson.dumps({
        'rc': 200,
        'message': 'OK',
        'process': {
            'pk': process.pk,
            'started_at': process.started_at,
            'progress': process.progress
        }
    },  cls=DjangoJSONEncoder))
