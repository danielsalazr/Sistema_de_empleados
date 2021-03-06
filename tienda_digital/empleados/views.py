from ast import Delete
from django.shortcuts import render
from  .models import *
from django.http import HttpResponse, JsonResponse
from urllib import request
from .serializers import EmpleadosSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    template_name= "empleados/index.html"
    context_object_name = "empleados"

    def get_queryset(self):
        """return de last five published questions"""
        #traerlas desde las mas recientes hasta las mas antiguas con el -pub_date
        return Empleados.objects.order_by("nombre")[:5]

# def index(request):
#     #return render(request, 'shop/index.html', {'productos': productos})
#     return render(request, 'empleados/index.html', )

def crearEmpleado(request):
    return render(request, 'empleados/crearEmpleado.html')

def actualizarEmpleado(request):
    return render(request, 'empleados/actualizarEmpleado.html')

def eliminarEmpleado(request):
    return render(request, 'empleados/eliminarEmpleado.html')

def consultarEmpleado(request):
    return render(request, 'empleados/consultarEmpleado.html')

def devolverConsulta(request):
    print (request.data)

class EmpleadosView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):

        personal = Empleados.objects.all()
        serializer = EmpleadosSerializer(personal, many =True)
        return Response(serializer.data)

    def post(self, request,*args, **kwargs):
        print(request.data)
        #print(request.data['nombre'])
        #q=Empleados(nombre ="daniel", apellido= "salazar", tipo_documento = "cc", numero_documento=56987826, correo="salazar@hotmail.com",telefono= 3240160, tipo_sangre="A+")
        empleados_serializer = EmpleadosSerializer(data=request.data)
        if empleados_serializer.is_valid():
            empleados_serializer.save()
            print(empleados_serializer.data)
            print("se guardo correctamente")
            #print(empleados_serializer.data)
        return Response("Empleado creado")

    #por cuestiones de tiempo la actualizacion y elminacion formulario lo realizo sin verificacion
    def delete(self, request,*args, **kwargs):
        print(request.data)
        print(request.data["nombre"])
        Empleados.objects.filter(nombre=request.data["nombre"], numero_documento=request.data["numero_documento"]).delete()

        return Response("Eliminado")

    def put(self, request,*args, **kwargs):
        print(request.data)
        print(request.data["numero_documento"])
        Empleados.objects.filter(numero_documento=request.data["numero_documento"]).update( nombre=request.data["nombre"], apellido=request.data["apellido"], tipo_documento = request.data["tipo_documento"], correo = request.data["correo"], telefono= request.data["telefono"], tipo_sangre= request.data["tipo_sangre"])
        pass

        return Response("Actualizado")