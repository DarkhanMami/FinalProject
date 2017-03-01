from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image
from numpy import pi
from qutip import *


@csrf_exempt
def calculate(request):
    types = request.POST.getlist('types[]')
    targets = request.POST.getlist('targets[]')
    controls = request.POST.getlist('controls[]')
    total = len(types)
    N = 2
    qc0 = QubitCircuit(N)
    for i in range(total):
        type = types[i]
        target = targets[i]
        control = controls[i]
        tgets = []
        ctrols = []
        tgets.append(int(target))
        if control != '':            
            ctrols.append(int(control))
            qc0.add_gate(type, targets=tgets, controls=ctrols)
        else:
            qc0.add_gate(type, targets=tgets)
            

    qc0.png
    U_list0 = qc0.propagators()
    U0 = gate_sequence_product(U_list0)
    matrix = []

    for i in range(0, N):
       for j in range(0, N): 
            matrix.append(str(U0.data[i,j]))


    return JsonResponse({
        "matrix": matrix
    })


def index(request):
    return render(request, 'circuit.html')
