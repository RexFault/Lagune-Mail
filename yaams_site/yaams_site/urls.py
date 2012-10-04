from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yaams_site.views.home', name='home'),
    # url(r'^yaams_site/', include('yaams_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'yaams.views.index', name='index'),
    url(r'^check_inbox/(.*)/$', 'yaams.views.check_inbox', name='check_inbox'),
    url(r'^json/check_inbox/(.*)/$', 'yaams.views.check_inbox_json_api', name='check_inbox_json_api'),
    url(r'^json/check_message/(.*)/(.*)/$', 'yaams.views.check_message_json_api', name='check_message_json_api'),
    url(r'^check_message/(.*)/(.*)/$', 'yaams.views.check_message', name='check_message'),
    url(r'^check_email/?$', 'yaams.views.redirect_to_email', name='form_redirect'),
    url(r'^about/?$', 'yaams.about_view.show_about', name='about_page'),
    url(r'^faq/?$', 'yaams.faq_view.show_faq', name='faq_page'),
    url(r'^protect_email/?$', 'yaams.views.protect_email', name='protect_email'),
    url(r'^logout/?$', 'yaams.views.logout', name='logout'),
    url(r'^delete_message/(.*)/(.*)/$', 'yaams.views.delete_message', name='delete_message'),
    url(r'^send_email/?$', 'yaams.views.send_message', name='send_message'),
    url(r'^json/send_email/?$', 'yaams.views.send_message_json_api', name='send_message_json_api'),
)
