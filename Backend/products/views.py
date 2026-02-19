from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .permissions import ProductPermission


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ProductPermission]
    queryset = Product.objects.all()  # ✅ required for DRF to generate actions

    def get_queryset(self):
        return Product.objects.filter(
            business=self.request.user.business
        )

    def perform_create(self, serializer):
        serializer.save(
            business=self.request.user.business,
            created_by=self.request.user,
            status='DRAFT'
        )

    # Submit draft for approval
    @action(detail=True, methods=['post'])
    def submit_for_approval(self, request, pk=None):
        product = self.get_object()
        if product.status != 'DRAFT':
            return Response(
                {"error": "Only draft products can be submitted."},
                status=status.HTTP_400_BAD_REQUEST
            )
        product.status = 'PENDING'
        product.save()
        return Response({"message": "Product submitted for approval."})

    # Approve pending product
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        product = self.get_object()
        role = request.user.role
        if not role or not role.can_approve_product:
            return Response(
                {"error": "You do not have approval permission."},
                status=status.HTTP_403_FORBIDDEN
            )
        if product.status != 'PENDING':
            return Response(
                {"error": "Only pending products can be approved."},
                status=status.HTTP_400_BAD_REQUEST
            )
        product.status = 'APPROVED'
        product.save()
        return Response({"message": "Product approved successfully."})


class PublicProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Product.objects.filter(status='APPROVED')
