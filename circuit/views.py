from django.shortcuts import render
import shutil
import os
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image
from numpy import pi
from qutip import *

N = 2
qc0 = QubitCircuit(N)
qc0.png
# src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
src_file = "/home/darkhan/Final/project/qcirc.png"
# dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
dst_file = "/home/darkhan/Final/project/static/qcirc.png"
if os.path.exists(dst_file):
    os.remove(dst_file)
# shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
if os.path.exists(src_file):
    shutil.move(src_file, "/home/darkhan/Final/project/static/")

if os.path.exists(src_file):
    os.remove(src_file)



@csrf_exempt
def new_circuit(request):
    qubits = request.POST.get('N')
    global qc0
    global N
    N = int(qubits)
    qc0 = QubitCircuit(N)
    if N != 1:
        qc0.png
    matrix = []
    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/home/darkhan/Final/project/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/home/darkhan/Final/project/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    if os.path.exists(src_file):
        shutil.move(src_file, "/home/darkhan/Final/project/static/")

    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })

@csrf_exempt
def remove_gate(request):
    ind = request.POST.get('ind')
    global qc0
    global N
    temp = int(ind)
    qc0.remove_gate(temp)
    qc0.png

    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []


    try:
        for i in range(0, N**2):
           for j in range(0, N**2):
                matrix.append(str(U0.data[i,j]))
    except:
        print 'empty circuit'

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/home/darkhan/Final/project/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/home/darkhan/Final/project/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/home/darkhan/Final/project/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })


@csrf_exempt
def calculate(request):
    types = request.POST.getlist('types[]')
    targets = request.POST.getlist('targets[]')
    controls = request.POST.getlist('controls[]')
    total = len(types)
    global qc0
    global N

    for i in range(total):
        name = types[i]
        if name == 'Hadamard':
            name = 'SNOT'
        target = targets[i]
        control = controls[i]
        tgets = []
        ctrols = []
        if target != '':
            tgets.append(int(target))
            if control != '':
                ctrols.append(int(control))
                qc0.add_gate(name, targets=tgets, controls=ctrols)
            else:
                qc0.add_gate(name, targets=tgets)


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = N**2
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/home/darkhan/Final/project/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/home/darkhan/Final/project/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/home/darkhan/Final/project/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })



@csrf_exempt
def new_rotation(request):
    types = request.POST.getlist('types[]')
    targets = request.POST.getlist('targets[]')
    angles = request.POST.getlist('angles[]')
    total = len(types)
    global qc0
    global N

    for i in range(total):
        name = types[i]
        target = targets[i]
        angle = angles[i]
        if target != '' and angle != '':
            tgets = []
            tgets.append(int(target)) 
            qc0.add_gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle))


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = N**2
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/home/darkhan/Final/project/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/home/darkhan/Final/project/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/home/darkhan/Final/project/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })



@csrf_exempt
def new_swap(request):
    types = request.POST.getlist('types[]')
    targets = request.POST.getlist('targets[]')
    angles = request.POST.getlist('angles[]')
    total = len(types)
    global qc0
    global N

    for i in range(total):
        name = types[i]
        target = targets[i]
        angle = angles[i]
        if target != '' and angle != '':
            tgets = []
            tgets.append(int(target))   
            qc0.add_gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle))
        elif target != '' and angle == '':
            tgets = []
            tgets.append(int(target))      
            qc0.add_gate(name, tgets, None)


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = N**2
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/home/darkhan/Final/project/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/home/darkhan/Final/project/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/home/darkhan/Final/project/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })



def index(request):
    return render(request, 'circuit.html')
