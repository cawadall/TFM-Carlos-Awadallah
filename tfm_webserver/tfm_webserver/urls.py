from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import handler404, handler500
from local_execution_app.views import error_handler404, error_handler500
from local_execution_app.admin import admin_site

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'^admin/', include(admin_site.urls)),
    # Add urls to custom views for Admin
    url(r'', include('local_execution_app.urls')),
]

handler404 = error_handler404
handler500 = error_handler500
