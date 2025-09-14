
from product.models import Product, Category, Review, ProductImage
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from product.permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
from order.serializers import QuantitySerializer
from rest_framework import status
from order.models import CartItem
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(ModelViewSet):
    # serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price','updated_at']
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Retrive a list of products'
    )
    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allow an admin to create a product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: "Bad Request"
        }
    )

    def get_queryset(self):
        return (
        Product.objects
        .select_related("category")   # fetch category in the same query
        .prefetch_related("images")   # fetch product images in one go
        .all()
    )

    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        product = self.get_object()
        # Get quantity from request data for POST, default to 1 for GET
        if request.method == 'POST':
            serializer = QuantitySerializer(data=request.data)
            if serializer.is_valid():
                quantity = serializer.validated_data['quantity']
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:  # GET request
            quantity = 1
        try:
            cart_item = OrderService.add_to_cart(product=product, user=request.user, quantity=quantity)
            return Response({
                        'status': f'{quantity} x {product.name} added to your cart',
                        'cart_item_quantity': cart_item.quantity
                    })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'],permission_classes=[IsAuthenticated])
    def buy_now(self, request, pk=None):
        product = self.get_object()
        if request.method == "POST":
            serializer = QuantitySerializer(data=request.data)
            if serializer.is_valid():
                quantity = serializer.validated_data['quantity']
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            quantity =1
        try:
            order = OrderService.buy_now(
                product=product,
                user=request.user,
                quantity=quantity,
            )
            
            return Response({
                'message': f'Order created successfully!',
                'order_id': str(order.id),
                'total_amount': order.total_price,
                'status': order.status
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get_serializer_class(self):
        if self.action == 'add_to_cart' and self.request.method == 'POST':
            return QuantitySerializer
        if self.action == 'buy_now' and self.request.method == 'POST':
            return QuantitySerializer
        return ProductSerializer


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(
        product_count=Count('products')).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}