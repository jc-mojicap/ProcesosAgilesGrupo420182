# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login, logout
from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

from .models import Imagen, ImageForm, User, UserForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


# Create your views here.
@csrf_exempt
def index(request):
    if request.user.is_authenticated():
        lista_imagenes = Imagen.objects.filter(user=request.user)
    else:
        lista_imagenes = Imagen.objects.all()
    context = {'lista_imagenes': lista_imagenes}
    # return render(request, 'polls/index.html', context)
    return HttpResponse(serializers.serialize("json", lista_imagenes))


@csrf_exempt
def add_image(request):
    if request.method == 'POST':
        # form = ImageForm(request.POST, request.FILES)
        # if form.is_valid():
        new_imagen = Imagen(url=request.POST['url'],
                            title=request.POST['title'],
                            descripcion=request.POST['descripcion'],
                            type=request.POST['type'],
                            imageFile=request.FILES['imageFile'],
                            user=request.user)

        new_imagen.save()
        # return HttpResponseRedirect(reverse('images:index'))
    # else:
        # form = ImageForm()

    # return render(request, 'polls/image_form.html', {'form': form})
    return HttpResponse(serializers.serialize("json", [new_imagen]))

@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        # form = UserForm(request.POST)
        # if form.is_valid():
            # cleaned_data = form.cleaned_data
            jsonUser = json.loads(request.body)
            # username = cleaned_data.get('username')
            username =jsonUser['username']
            # first_name = cleaned_data.get('first_name')
            first_name = jsonUser['first_name']
            # last_name = cleaned_data.get('last_name')
            last_name = jsonUser['last_name']
            # password = cleaned_data.get('password')
            password =jsonUser['password']
            # email = cleaned_data.get('email')
            email =jsonUser['email']

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()

            # return HttpResponseRedirect(reverse('images:index'))
    # else:
        # form = UserForm()

    # context = {
    #    'form': form
    # }
    # return render(request, 'polls/registro.html', context)
    return HttpResponse(serializers.serialize("json", [user_model]))

@csrf_exempt
def login_view(request):
    # if request.user.is_authenticated():
    #    return redirect(reverse('images:index'))

    # mensaje = ''
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        # username = request.POST.get('username')
        username = jsonUser['username']
        # password = request.POST.get('password')
        password = jsonUser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            mensaje = 'ok'
            # return redirect(reverse('images:index'))
        else:
            mensaje = 'Nombre de usuario o contraseña incorrectos'

    # return render(request, 'polls/login.html', {'mensaje': mensaje})
    return JsonResponse({"mensaje":mensaje})

@csrf_exempt
def logout_view(request):
    logout(request)
    # return HttpResponseRedirect(reverse('images:index'))
    return JsonResponse({"mensaje": 'ok'})

@csrf_exempt
def isLogged_view(request):
    if request.user.is_authenticated():
        mensaje = 'ok'
    else:
        mensaje = 'no'
    return JsonResponse({"mensaje": mensaje})


def ver_imagenes(request):
    return render(request, "polls/index.html")


def agregar_imagen(request):
    return render(request, "polls/image_form.html")


def agregar_usuario(request):
    return render(request, "polls/registro.html")


def ingresar(request):
    return render(request, "polls/login.html")