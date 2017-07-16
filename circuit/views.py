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
import random, string


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


rules = dict()
circuits = dict()
Ns = dict()
base_dir = '/root/FinalProject'
user = ''
exp_imp = dict()




@csrf_exempt
def new_circuit(request):
    qubits = request.POST.get('N')
    global Ns    
    global circuits
    global user

    user = request.COOKIES['users']
    N = int(qubits)
    qc0 = QubitCircuit(N)
    circuits[user] = qc0
    Ns[user] = N


    if N != 1:
        circuits[user].png
    matrix = []
    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    if os.path.exists(src_file):
        shutil.move(src_file, base_dir + "/static/user/" + user + "/")

    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix,
        "user": user
    })

@csrf_exempt
def remove_gate(request):
    ind = request.POST.get('ind')
    global circuits
    global Ns
    user = request.COOKIES['users']
    user = request.COOKIES['users']
    N = Ns[user]

    temp = int(ind)
    circuits[user].remove_gate(temp)
    circuits[user].png

    U_list0 = circuits[user].propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []


    try:
        for i in range(0, 2**N):
           for j in range(0, 2**N):
                matrix.append(str(U0.data[i,j]))
    except:
        print 'empty circuit'

    # src_file = os.path.join("settings.BASE_DIR", "qcirc.png")
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
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
    global circuits
    global Ns
    user = request.COOKIES['users']
    N = Ns[user]

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
                circuits[user].gates.insert(int(pos), Gate(name, targets=tgets, controls=ctrols))
            else:
                circuits[user].gates.insert(int(pos), Gate(name, targets=tgets))

    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
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
    global circuits
    global Ns
    user = request.COOKIES['users']

    N = Ns[user]

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
                circuits[user].add_gate(name, targets=tgets, controls=ctrols)
            else:
                circuits[user].add_gate(name, targets=tgets)

    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
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
    global circuits
    global Ns
    user = request.COOKIES['users']
    N = Ns[user]

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
            circuits[user].gates.insert(int(pos), Gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle)))


    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
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
    global circuits
    global Ns
    user = request.COOKIES['users']
    N = Ns[user]

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
            circuits[user].add_gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle))


    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
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
    global circuits
    global Ns
    user = request.COOKIES['users']
    N = Ns[user]

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
            circuits[user].gates.insert(int(pos), Gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle)))
        elif target != '' and angle == '':
            tgets = []
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))
            circuits[user].gates.insert(int(pos), Gate(name, tgets, None))


    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
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
    global circuits
    global Ns
    user = request.COOKIES['users']
    N = Ns[user]

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
            circuits[user].add_gate(name, tgets, None, pi/int(angle), r"\pi/"+str(angle))
        elif target != '' and angle == '':
            tgets = []
            if ',' in str(target):
                tgets = str(target).split(',')
                for i in range(len(tgets)):
                    tgets[i] = int(tgets[i])
            else:
                tgets.append(int(target))        
            circuits[user].add_gate(name, tgets, None)


    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })

@csrf_exempt
def find_adj_gates(request):
    global circuits
    global Ns
    user = request.COOKIES['users']
    N = Ns[user]

    circuits[user] = circuits[user].adjacent_gates()

    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })


@csrf_exempt
def export_dump(request):
    global user
    global circuits
    global rules
    global exp_imp


    if user in rules:
        exp_imp[user] = dict()
        exp_imp[user] = rules[user]

    qsave(circuits[user], 'save_temp')
    file_path = os.path.join(base_dir + '/save_temp.qu')
    fsock = open(file_path, "rb")
    response = HttpResponse(fsock)
    response['Content-Disposition'] = 'attachment; filename=' + user
    if os.path.exists(base_dir + '/save_temp.qu'):
        os.remove(base_dir + '/save_temp.qu')
    return response


@csrf_exempt
def import_file(request):
    global circuits
    global Ns
    global user

    user = request.COOKIES['users']

    if request.method == "POST":
        saved_state = request.FILES['file']

        rule_names = []

        if str(saved_state) in exp_imp:
            rules[user] = dict()
            rules[user] = exp_imp[str(saved_state)]
            for rule in rules[user]:
                rule_names.append(rule)            


        if os.path.exists(base_dir + '/upload.qu'):
            os.remove(base_dir + '/upload.qu')

        dump_name = default_storage.save(base_dir + '/upload.qu', ContentFile(saved_state.read()))
        

        circuits[user] = qload('upload')

        N = circuits[user].N
        Ns[user] = N

        circuits[user].png
        U_list0 = circuits[user].propagators()
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
        src_file = base_dir + "/qcirc.png"
        # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
        dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
        if os.path.exists(dst_file):
            os.remove(dst_file)
        # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
        shutil.move(src_file, base_dir + "/static/user/" + user + "/")
        
        if os.path.exists(src_file):
            os.remove(src_file)

        return JsonResponse({
            "matrix": matrix,
            "N"     : N,
            "user": user,
            "rule_names": rule_names
        })



    return render(request, 'import.html')


@csrf_exempt
def create_rule(request):
    global circuits
    global rules
    global user

    name = request.POST.get('name')
    rule_from = request.POST.get('from')
    rule_to = request.POST.get('to')

    temp_rule = []

    for i in range(int(rule_from), int(rule_to) + 1):
        temp_rule.append(circuits[user].gates[i])

    if (user not in rules):
        rules[user] = dict()

    rules[user][name] = temp_rule

    return JsonResponse({
            "name": name
    })


@csrf_exempt
def add_rule(request):
    global circuits
    global rules
    global Ns
    global user

    N = Ns[user]


    name = request.POST.get('name')

    temp_rule = rules[user][name]

    for i in range(0, len(temp_rule)):
        rule = temp_rule[i]
        circuits[user].gates.insert(len(circuits[user].gates), rule)


    circuits[user].png
    U_list0 = circuits[user].propagators()
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
    src_file = base_dir + "/qcirc.png"
    # dst_file = os.path.join(settings.BASE_DIR, "static", "qcirc.png")
    dst_file = base_dir + "/static/user/" + user + "/qcirc.png"
    if os.path.exists(dst_file):
        os.remove(dst_file)
    # shutil.move(src_file, os.path.join(settings.BASE_DIR, "static"))
    shutil.move(src_file, base_dir + "/static/user/" + user + "/")
    
    if os.path.exists(src_file):
        os.remove(src_file)

    return JsonResponse({
        "matrix": matrix
    })


def index(request):
    global user
    user = randomword(6)
    response = render(request, 'circuit.html')


    if not request.COOKIES.has_key(user):
        os.mkdir(os.path.join(base_dir + "/static/user", user))
        response.set_cookie('users', user)
    else:
        print 'has_cookie!!!!!!'
    

    return response