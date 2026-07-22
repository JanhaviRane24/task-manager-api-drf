from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Task, CustomUser
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Invalid credentials"}, status=401)

    if not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_tasks(request):

    if request.method == "GET":

        tasks = Task.objects.filter(user=request.user)


        serializer = TaskSerializer(
            tasks,
            many=True
        )

        return Response(serializer.data)


    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request, id):

    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    serializer = TaskSerializer(
        task,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, id):

    task = get_object_or_404(Task,id=id,user=request.user)


    task.delete()

    return Response(
        status=204
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            
            status=201
        )

    return Response(serializer.errors, status=400)