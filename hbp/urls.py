from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings

from . import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.index, name='index'),
	url(r'^pc/$', views.personalizedCare, name='personalizedCare'),
	url(r'^iv/$', views.informationalVideos, name='informationalVideos'),
	url(r'^iv/(?P<video_index>[0-9]{1,2})/$', views.informationalVideos, name='informationalVideos'),
	url(r'^cs/$', views.commitAndScheduleIntro ,name='commitAndScheduleIntro'),
	url(r'^cs/delivery-date/$', views.commitAndScheduleDeliveryDate, 
		name='commitAndScheduleDeliveryDate'),
	url(r'^cs/calendar/$', views.commitAndScheduleCalendar, name='commitAndScheduleCalendar'),
	url(r'^cs/signature/$', views.commitAndScheduleSignature, name='commitAndScheduleSignature'),
	url(r'^incentive/$', views.incentive, name='incentive'),
	url(r'^final/$', views.final, name='final'),
	url(r'^consent/$', views.consent, name='consent'),
	url(r'^signatures/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT,
	}),
	url(r'^print-appt/$', views.printAppt, name='printAppt'),
	url(r'^import-appts/$', views.importAppts, name='importAppts'),
)
