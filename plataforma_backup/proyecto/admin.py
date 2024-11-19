from django.contrib import admin
from .models import Marca, backup, detalle_backup, Equipo, TareaProgramada
from crontab import CronTab
# Register your models here.
admin.site.register(Marca)
admin.site.register(Equipo)
admin.site.register(backup)
admin.site.register(detalle_backup)
def programar_tarea(tarea_programada):
    cron = CronTab(user=True)
    tarea = cron.new(command="python3 /home/manu/backup/plataforma_backup/manage.py shell -c 'from proyecto.cron import programa; programa()'")
    tarea.setall(tarea_programada.minutos, tarea_programada.hora, tarea_programada.dia, tarea_programada.mes, tarea_programada.dia_semana)
    cron.write()

class TareaProgramadaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        programar_tarea(obj)

admin.site.register(TareaProgramada, TareaProgramadaAdmin)
