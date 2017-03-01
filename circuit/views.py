from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image
from numpy import pi
from qutip import *



def index(request):
    return render(request, 'circuit.html')


@require_http_methods("POST")
def remove_gates(request):
	remove_gate(request.POST["index"])


@require_http_methods("POST")
def add_gates(request):
	add_gate(request.POST["name"], targets=request.POST["target"], controls=request.POST["control"])



@require_http_methods("POST")
def insert_gates(request):
	gates.insert(request.POST["index"], Gate(request.POST["name"], targets=request.POST["target"], controls=request.POST["control"]))


@require_http_methods("POST")
def add_rotation_gates(request):
	add_gate(request.POST["name"], request.POST["target"], None, pi/request.POST["angle"],r"\pi/" + request.POST["angle_text"])



@require_http_methods("POST")
def insert_rotation_gates(request):
	gates.insert(request.POST["index"], Gate(request.POST["name"], request.POST["target"], None, pi/request.POST["angle"],r"\pi/" + request.POST["angle_text"]))


# @require_http_methods("POST")
# def clear_circuit(request):
	

# @require_http_methods("POST")
# def repaint_circuit(gates):
	

# def print_result(circuit):




