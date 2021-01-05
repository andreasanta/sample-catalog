
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Filters the returned products by In Stock / Out of Stock
        """
        queryset = Product.objects.all()
        stock_status = self.request.query_params.get('stock', None)

        if stock_status == 'available':
            queryset = queryset.filter(qty__gt=0)
        elif stock_status == 'notavailable':
            queryset = queryset.filter(qty__exact=0)
        elif stock_status is not None:
            raise ParseError('Invalid stock parameter value, supported only available and notavailable', 400)

        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    """
        This function handles a PATCH request.

        We admit patch requests only with the "qty"
        parameter and we make sure it's valid and does
        not reduce the quantity below zero.

        All other parameters in the request raise an error.
    """
    def partial_update(self, request, *args, **kwargs):

        # We only allow partial updates to quantity
        # and ensure no additional params are specified
        if (not 'qty' in request.data or len(request.data) > 1
                or request.data.get('qty') is None or not type(request.data.get('qty')) == int):
            raise ParseError('Only qty parameter can be updated (with a +/- val) and must be valid int also :)')

        # Check valid quantity
        qs = self.get_queryset()
        product = qs.first()

        if product is None:
            raise Http404

        if product.qty + int(request.data.get('qty')) < 0:
            raise ParseError('Cannot set negative quantity for object', 400)
        
        # Increase quantity to update serializer accordingly
        request.data['qty'] = product.qty + int(request.data.get('qty'))

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
            We block PUT updates, because the product cannot be updated entirely according to specs.
        """
        raise ParseError('Only qty parameter can be updated with a +/- increment with the PATCH method')