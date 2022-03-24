from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("user.urls")),
    path("api/v1/profile/", include("referal.urls")),
]

urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
