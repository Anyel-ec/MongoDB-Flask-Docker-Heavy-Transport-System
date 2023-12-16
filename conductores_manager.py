from flask import render_template
from data_manager import DataManager
# importar dependencias
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash

def clientes_home(data_manager):
    clientes = data_manager.get_clientes()
    return render_template('clientes/index.html', clientes=clientes)