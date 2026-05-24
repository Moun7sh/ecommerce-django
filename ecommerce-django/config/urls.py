from django.contrib import admin
from django.urls import path, include

# import the built-in LogoutView
from django.contrib.auth.views import LogoutView

# allow GET as well as POST
class AllowGetLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options']

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # built-in auth
    # override logout to allow GET and redirect to home
    path('accounts/logout/', AllowGetLogoutView.as_view(next_page='/'), name='logout'),
]
