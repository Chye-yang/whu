"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import re_path as url
from django.contrib import admin
from django.urls import path
from model import views, identify, analysis, record

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.analysis_empty),
    url(r'^analysis', views.analysis),
    url(r'^0analysis', views.analysis_empty),

    # record
    url(r'^record_speed', record.record_speed),
    url(r'^record_ping', record.record_ping),
    url(r'^record', views.record),
    url(r'^0record', views.record_empty),
    # url(r'^identify', views.identify),

    # analysis
    url(r'^table1', analysis.table1),
    url(r'^table2', analysis.table2),
    url(r'^table3', analysis.table3),
    url(r'^table4', analysis.table4),
    url(r'^mainTop', analysis.mainTop),
    url(r'^mainBottom', analysis.mainBottom),
    url(r'^readPcap', analysis.readPcap),
    url(r'^readCsv/', analysis.readCsv),

    # prediction
    # url(r'^chart1/', views.chart1),
    # url(r'^chart2/', views.chart2),
    # url(r'^chart3/', views.chart3),
    # url(r'^chart4/', views.chart4),
    # url(r'^chart5/', views.chart5),
    url(r'^numberShow/', views.numberShow),
    # url(r'^predict/', views.predict),
    # url(r'^mockData/', views.mockData),
    # url(r'^func1/', views.func1),
    #
    # url(r'^behavior_input/', identify.behavior_input),
    # url(r'^real_time_statistics/', identify.real_time_statistics),
    # url(r'^protocol_classification/', identify.protocol_classification),
    # url(r'^behavior_classification/', identify.behavior_classification),

    # url(r'^behavior_overview/', identify.behavior_overview),
    # url(r'^flow_analysis/', identify.flow_analysis),
    # url(r'^mock_data/', identify.mock_data),
    # url(r'^mock_data2/', identify.mock_data2),

    url(r'^test/', analysis.analysis_request),
    url(r'^mock_data3/', analysis.mock_data3),
    url(r'^clear_analysis/', analysis.clear_analysis),
    url(r'behavior_count/', identify.behavior_count),


]
