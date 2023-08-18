from django.urls import path, include

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),

    path('auth/', include('api.v1.auth.urls')),
    path('users/', include('api.v1.users.urls')),

    # path('users/', include('api.v1.users.urls')),
]
