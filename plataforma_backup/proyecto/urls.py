from django.urls import path
from . import views
from .views import DescargarContenidoView, respaldo_individual_view, realizar_respaldo_view, respaldo_backup

urlpatterns = [
    path('', views.home, name='home'),
    path('admin', views.admin, name='admin'),
    path('respaldo/<int:equipo_id>/', views.respaldo, name="respaldo"),
    path('historial/', views.respaldo_backup, name="respaldo_backup"),
    path('historial/<int:backup_id>/', views.respaldo_historial, name="respaldo_historial"),
    path('descargar/<int:detalle_backup_id>/', DescargarContenidoView.as_view(), name='descargar'),
    path('realizar_respaldo/', realizar_respaldo_view, name='realizar_respaldo'),
    path('respaldo_individual/<int:equipo_id>/', respaldo_individual_view , name='respaldo_individual'),
]