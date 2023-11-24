"""
URL configuration for Newz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from noticias import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from noticias.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.noticias_principais, name='noticias_principais'),
    path('bbc/', views.noticias_bbc, name='noticias_bbc'),
    path('wsj/', views.noticias_wsj, name='noticias_wsj'),
    path('science/', views.noticias_ciencia, name='noticias_ciencia'),
    path('sports/', views.noticias_esportes, name='noticias_esportes'),
    path('entertainment/', views.noticias_entretenimento, name='noticias_entretenimento'),
    path('health/', views.noticias_saude, name='noticias_saude'),
    path('technology/', views.noticias_tecnologia, name='noticias_tecnologia'),
    path('cnn/', views.noticias_cnn, name='noticias_cnn'),
    path('noticias/<path:url_noticia>/', views.detalhes_noticia, name='detalhes_noticia'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('signup/', views.signup, name='signup'),
    path('resultados_pesquisa/', views.resultados_pesquisa, name='resultados_pesquisa'),
    path('obter_ultimas_noticias/', views.obter_ultimas_noticias, name='obter_ultimas_noticias'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
