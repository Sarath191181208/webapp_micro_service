import random 

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status

from .models import Product, User
from .serializers import ProductSerializer
from .producer import publish

class ProductViewSet(viewsets.ViewSet):
    def list(self, _: Request):
        """
            List all products in the database
        """
        # TODO: Implement pagination
        objs = Product.objects.all() # Get all products from the database
        serialized_objs = ProductSerializer(objs, many=True) # Serialize the products
        return Response(serialized_objs.data) # Return the serialized products

    def create(self, req: Request):
        """
            Create a new product in the database
        """
        ser = ProductSerializer(data=req.data) # Deserialize the request data
        ser.is_valid(raise_exception=True) # Validate the data
        publish('product_created', ser.data) # Sending the event to rabbit mq
        ser.save() # Save the data to the database
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def retrieve(self, _: Request, primary_key: str | None = None):
        """
            Retrieve a single product from the database
        """
        product = Product.objects.get(id=primary_key) # Get the product from the database
        ser = ProductSerializer(product) # Serialize the product
        return Response(ser.data) # Return the serialized product

    def update(self, req: Request, primary_key: str | None = None):
        """
            Update a single product in the database
        """
        product = Product.objects.get(id=primary_key) # Get the product from the database
        serializer = ProductSerializer(instance=product, data=req.data) # Deserialize the request data
        serializer.is_valid(raise_exception=True) # Validate the data
        serializer.save() # Save the data to the database
        publish('product_updated', ser.data) # Sending the event to rabbit mq
        return Response(serializer.data, status=status.HTTP_201_CREATED) # Return the serialized product

    def destroy(self, _: Request, primary_key: str | None = None): 
        """
            Delete a single product from the database
        """
        product = Product.objects.get(id=primary_key) # Get the product from the database
        product.delete() # Delete the product from the database
        publish('product_deleted', primary_key) # Sending the event to rabbit mq
        return Response(status=status.HTTP_204_NO_CONTENT) # Return a 204 status code

class UserAPIView(APIView):
    def get(self, _: Request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            "id": user.id,
        })# Return a simple message
