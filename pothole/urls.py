from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
app_name='pothole'
from .views import *

urlpatterns=[

	url(r'^$',views.index,name="index"),
	url(r'^checkuser$',views.check),
	url(r'^login$', views.login_user,name='login'),
    url(r'^logout$',views.logout_user, name='logout'),
    url(r'^loginpage/success$',views.login),
    url(r'^authenticate$',views.login),
    url(r'^dashboard$',views.dashboard),
    url(r'^potholedetail$',views.pothole),
    url(r'^map$',views.map),
    url(r'^analytics$',views.line_chart,
        name='line_chart'),
    # url(r'^line_chart/$', ),
    url(r'^line_chart/json/$', views.line_chart_json,
        name='line_chart_json'),
    url(r'^line_chart_ride/json/$', views.line_chart_json_ride,
        name='line_chart_json_ride'),
    url(r'^radar_chart/json/$', views.radar_chart_json,
        name='radar_chart_json'),
    url(r'^test$',views.sessionfn),
    url(r'^locations$',views.locations),
    # url(r'^convert$', views.convert, name='convert')
]
'''
{'template_name': 'pothole/success.html'}
'''