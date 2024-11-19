from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Equipo, detalle_backup, backup
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from .realizar_respaldos import realizar_respaldo
from django.views.decorators.http import require_POST
from .respaldo_individual import respaldo_individual
from django.http import JsonResponse
from django.urls import reverse

@login_required
def home(request):
    equipos = Equipo.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(equipos, 8)
        equipos = paginator.page(page)
    except:
        equipos = paginator.page(1)

    for equipo in equipos:
        ultimo_respaldo = detalle_backup.objects.filter(id_equipo=equipo).order_by('-fecha_creacion').first()
        equipo.ultimo_respaldo = ultimo_respaldo

    data = {
        'entity': equipos,
        'paginator': paginator
    }
    return render(request, 'myfirst.html', data)

def admin(request):
    return redirect('admin:index')

@login_required
def respaldo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    respaldos = detalle_backup.objects.filter(id_equipo=equipo, contenido__isnull=False).exclude(contenido__exact='').order_by('-fecha_creacion')

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(respaldos, 8)
        respaldos = paginator.page(page)
    except:
        respaldos = paginator.page(1)

    data = {
        'equipo': equipo,
        'entity': respaldos,
        'paginator': paginator
    }

    return render(request, 'view_respaldo.html', data)

@login_required
def respaldo_backup(request):
    backups = backup.objects.all().order_by('-date')

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(backups, 8)
        backups = paginator.page(page)
    except:
        backups = paginator.page(1)

    data = {
        'entity': backups,
        'paginator': paginator
    }

    return render(request, 'view_backup.html', data)

@login_required
def respaldo_historial(request, backup_id):
    backup_historial = get_object_or_404(backup, id=backup_id)
    respaldos = detalle_backup.objects.filter(id_backup=backup_historial, contenido__isnull=False).exclude(contenido__exact='').order_by('-fecha_creacion')

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(respaldos, 8)
        respaldos = paginator.page(page)
    except:
        respaldos = paginator.page(1)

    data = {
        'backup_historial': backup_historial,
        'entity': respaldos,
        'paginator': paginator
    }

    return render(request, 'view_historial.html', data)

class DescargarContenidoView(View):
    def get(self, request, detalle_backup_id):
        detalle_backup_obj = get_object_or_404(detalle_backup, id=detalle_backup_id)

        if detalle_backup_obj.contenido:
            try:
                contenido = detalle_backup_obj.contenido

                file_extension = contenido.name.split('.')[-1]

                content_type_mapping = {
                    'txt': 'text/plain',
                    'pdf': 'application/pdf',
                    'png': 'image/png',
                }

                content_type = content_type_mapping.get(file_extension, 'application/octet-stream')

                response = HttpResponse(contenido.read(), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{detalle_backup_obj.contenido}"'
                return response
            except Exception as e:
                return HttpResponse(f"Error al procesar el contenido: {str(e)}")
        else:
            return HttpResponse("El contenido no está disponible para descargar.")

@require_POST
def realizar_respaldo_view(request):
    try:
        realizar_respaldo()
        mensaje = 'Respaldo Procesado'
        return JsonResponse({'mensaje': mensaje, 'redirect_url': '/'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def respaldo_individual_view(request, equipo_id):
    try:
        respaldo_individual(equipo_id)
        mensaje = 'El respaldo individual se ha realizado'
        url_respaldo_individual = reverse('respaldo', kwargs={'equipo_id': equipo_id})
        return JsonResponse({'mensaje': mensaje, 'redirect_url': url_respaldo_individual})
    except Exception as e:
        mensaje = f'Error al realizar el respaldo: {str(e)}'
        return JsonResponse({'error': mensaje}, status=500)