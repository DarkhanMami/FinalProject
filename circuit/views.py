from django.shortcuts import render
import shutil
import os
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import json

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image
from numpy import pi
from qutip import *

N = 2
qc0 = QubitCircuit(N)

rules = dict()

qc0.png
# src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
src_file = "/root/FinalProject/qcirc.png"
# dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
dst_file = "/root/FinalProject/static/qcirc.png"
if os.path.exists(dst_file):
    os.remove(dst_file)
# shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
if os.path.exists(src_file):
    shutil.move(src_file, "/root/FinalProject/static/")

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
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    if os.path.exists(src_file):
        shutil.move(src_file, "/root/FinalProject/static/")

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
        for i in range(0, 2**N):
           for j in range(0, 2**N):
                matrix.append(str(U0.data[i,j]))
    except:
        print 'empty circuit'

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })


@csrf_exempt
def insert_gate(request):
    pos = request.POST.get('pos')
    types = request.POST.getlist('types[]')
    targets = request.POST.getlist('targets[]')
    controls = request.POST.getlist('controls[]')
    total = len(types)
    global qc0
    global N

    for i in range(total):
        name = types[i]
        if name == 'HADAMARD':
            name = 'SNOT'
        target = targets[i]
        control = controls[i]
        tgets = []
        ctrols = []
        if target != '':
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))
            if control != '':
                if ',' in str(control):
                    ctrols = str(control).split(',')
                    for i in range(len(ctrols)):
                        ctrols[i] = int(ctrols[i])
                else:
                    ctrols.append(int(control))
                qc0.gates.insert(int(pos), Gate(name, targets=tgets, controls=ctrols))
            else:
                qc0.gates.insert(int(pos), Gate(name, targets=tgets))

    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
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
    global all_gates

    for i in range(total):
        name = types[i]
        if name == 'HADAMARD':
            name = 'SNOT'
        target = targets[i]
        control = controls[i]
        tgets = []
        ctrols = []
        if target != '':
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))
            if control != '':
                if ',' in str(control):
                    ctrols = str(control).split(',')
                    for i in range(len(ctrols)):
                        ctrols[i] = int(ctrols[i])
                else:
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
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })


@csrf_exempt
def insert_rotation(request):
    pos = request.POST.get('pos')
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
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))
            qc0.gates.insert(int(pos), Gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle)))


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
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
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))
            qc0.add_gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle))


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })

@csrf_exempt
def insert_swap(request):
    pos = request.POST.get('pos')
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
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))
            qc0.gates.insert(int(pos), Gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle)))
        elif target != '' and angle == '':
            tgets = []
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))
            qc0.gates.insert(int(pos), Gate(name, tgets, None))


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
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
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))   
            qc0.add_gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle))
        elif target != '' and angle == '':
            tgets = []
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))        
            qc0.add_gate(name, tgets, None)


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })

@csrf_exempt
def find_adj_gates(request):
    global qc0
    global N

    qc0 = qc0.adjacent_gates()

    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })


@csrf_exempt
def export_dump(request):
    global qc0
    qsave(qc0, 'save_temp')
    file_path = os.path.join('/root/FinalProject/save_temp.qu')
    fsock = open(file_path, "rb")
    response = HttpResponse(fsock)
    response['Content-Disposition'] = 'attachment; filename=dump.txt'
    return response


@csrf_exempt
def import_file(request):
    global qc0
    global N

    if request.method == "POST":
        saved_state = request.FILES['file']

        dump_name = default_storage.save('/root/FinalProject/upload.qu', ContentFile(saved_state.read()))
 

        qc0 = qload('upload')

        N = qc0.N

        qc0.png
        U_list0 = qc0.propagators()
        U0 = gate_sequence_product(U_list0)
        matrix = []

        if N == 1:
            tmp = 2
        else:
            tmp = 2**N
        for i in range(0, tmp):
           for j in range(0, tmp):            
                matrix.append(str(U0.data[i,j]))

        # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
        src_file = "/root/FinalProject/qcirc.png"
        # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
        dst_file = "/root/FinalProject/static/qcirc.png"
        if os.path.exists(dst_file):
            os.remove(dst_file)
        # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
        shutil.move(src_file, "/root/FinalProject/static/")
        
        if os.path.exists(src_file):
            os.remove(src_file)

        return JsonResponse({
            "matrix": matrix,
            "N"     : N
        })



    return render(request, 'import.html')


@csrf_exempt
def create_rule(request):
    global qc0
    global rules
    name = request.POST.get('name')
    rule_from = request.POST.get('from')
    rule_to = request.POST.get('to')

    temp_rule = []

    for i in range(int(rule_from)-1, int(rule_to)):
        temp_rule.append(qc0.gates[i])

    rules[name] = temp_rule

    return JsonResponse({
            "name": name
    })


@csrf_exempt
def add_rule(request):
    global qc0
    global rules
    global N


    name = request.POST.get('name')

    temp_rule = rules[name]

    for rule in temp_rule:
        qc0.gates.insert(len(qc0.gates), rule)


    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    if N == 1:
        tmp = 2
    else:
        tmp = 2**N
    for i in range(0, tmp):
       for j in range(0, tmp):            
            matrix.append(str(U0.data[i,j]))

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = "/root/FinalProject/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = "/root/FinalProject/static/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, "/root/FinalProject/static/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })


def index(request):
    return render(request, 'circuit.html')