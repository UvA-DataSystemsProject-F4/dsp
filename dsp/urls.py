"""dsp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from dspdata import views
from dspui.views import IndexView, DatasourceView, SubDatasourceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loaddata/', views.loaddata_view),
    path('pipeline/', views.pipeline_view),
    path('', IndexView.as_view()),
    path('datasource/', DatasourceView.as_view()),
    path('datasource/<int:id>', DatasourceView.as_view()),
    path('subdatasource/<int:id>', SubDatasourceView.as_view()),

]
