from django.conf.urls import url
from encuestas import views

urlpatterns = [
    # ex: /encuestas/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /encuestas/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetallesView.as_view(), name='detalles'),
    # ex: /encuestas/5/resultados/
    url(r'^(?P<pk>[0-9]+)/resultados/$', views.ResultadosView.as_view(), name='resultados'),
    # ex: /encuestas/5/voto/
    url(r'^(?P<question_id>[0-9]+)/votos/$', views.votos, name='votos'),
    ]
