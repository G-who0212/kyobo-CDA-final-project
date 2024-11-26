from django.contrib import admin
from django.urls import path, include
from. import views
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', views.login, name='login'), 
    path('employ/', views.employ, name='employ'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('create/', views.create, name='create'), 
    path('employdetail/<int:pk>', views.employdetail, name='employdetail'),
    path('', include('django_prometheus.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])