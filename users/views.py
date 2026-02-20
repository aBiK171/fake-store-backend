from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .models import Favorite


@api_view(['POST'])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    name = request.data.get("name")

 
    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "User already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

 
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=name
    )

    # Generate JWT token
    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "User created successfully",
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "username": request.user.username,
        "id": request.user.id
    })


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):


    if request.method == 'GET':
        items = CartItem.objects.filter(user=request.user)

        data = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity
            }
            for item in items
        ]

        return Response(data)

    # =======================
    # POST - Add to cart
    # =======================
    if request.method == 'POST':
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "product_id required"}, status=400)

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product_id=product_id
        )

        if not created:
            item.quantity += int(quantity)
            item.save()

        return Response({"message": "Added to cart"})


    if request.method == 'PUT':
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or quantity is None:
            return Response({"error": "product_id and quantity required"}, status=400)

        try:
            item = CartItem.objects.get(user=request.user, product_id=product_id)
            item.quantity = int(quantity)
            item.save()
            return Response({"message": "Quantity updated"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

  


    if request.method == 'DELETE':

        product_id = request.data.get("product_id")

        # 🔴 Delete all
        if not product_id:
            CartItem.objects.filter(user=request.user).delete()
            return Response({"message": "All items deleted"})

        # 🔴 Delete single
        try:
            item = CartItem.objects.get(user=request.user, product_id=product_id)
            item.delete()
            return Response({"message": "Item deleted"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)





@api_view(['POST'])
def signup(request):

    username = request.data.get("username")
    password = request.data.get("password")
    name = request.data.get("name")

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "User already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        username=username,
        first_name=name,
        password=make_password(password)
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "User created successfully",
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Favorite

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorites(request):

    if request.method == 'GET':
        items = Favorite.objects.filter(user=request.user)

        data = [
            {
                "product_id": item.product_id
            }
            for item in items
        ]

        return Response(data)

    if request.method == 'POST':
        product_id = request.data.get("product_id")

        Favorite.objects.get_or_create(
            user=request.user,
            product_id=product_id
        )

        return Response({"message": "Added to favorites"})

    if request.method == 'DELETE':
        product_id = request.data.get("product_id")

        Favorite.objects.filter(
            user=request.user,
            product_id=product_id
        ).delete()

        return Response({"message": "Deleted from favorites"})
