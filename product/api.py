
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import BasePermission
from .serializers import ProductSerializer
from .models import Product



class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
    
    
    
    
class ProductCrreateApi(CreateAPIView):
    serializer_class   = ProductSerializer
    permission_classes = [IsStaff]




class ProductDeleteApi(DestroyAPIView):
    serializer_class   = ProductSerializer
    permission_classes = [IsStaff]
    
    def get_queryset(self):
        user     = self.request.user
        if user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(created_by = user)
        