from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet, PDFUploadViewSet, PDFDeleteViewSet

router = DefaultRouter()
router.register(r'modules', ModuleViewSet, basename='module')

urlpatterns = [
    path('', include(router.urls)),
    path('modules/<int:module_id>/upload-pdf/', PDFUploadViewSet.as_view({'post': 'create'})),
    path('pdf/<int:pk>/', PDFDeleteViewSet.as_view({'delete': 'destroy'})),
]
