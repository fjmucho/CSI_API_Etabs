#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Autor: F. JMucho. <fjmucho0@gmail.com>
Date: 
Description:
* Ejecuta aplicacion Etabs

    [evaluar si, esta instalado etabs: ...ejecutar otras acciones...
    caso contrario: lanzar un menzaje 'no tienes intalada etabs']->en evaluacion para incluir o no!, este algoritmo

    algoritmo de instrucciones:

        evaluar si, esta en ejecucion una instalcia de etabs
            adjuntar la instancia a la existente
        caso contrario:
            busco la ultima verion instalada e intentar conectarme 
            si coneccion es esitosa:
                ejecutar etabs

    Methods.:
        comtypes.client
            .GetActiveObject()
            .ApplicationStart()
            .CreateObject()
                .QueryInterface()
                .CreateObjectProgID()
            .ApplicationStart()
"""
import os
import sys
import comtypes.client

try:
    #get the active ETABS object
    ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    print("Coneccion exitosa!.\nadjuntando a una instancia existente.")
except (OSError, comtypes.COMError):
    # No running instance of the program found or failed to attach.
    print("No se encontró ninguna instancia en ejecución del programa(Etabs).")


    print("Tratando de Ejecutar etabs!.")
    #create API helper object
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    try: 
        #create an instance of the ETABS object from the latest installed ETABS
        ETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject") 
        print("Coneccion esitosa!.")
    except (OSError, comtypes.COMError):
        print("Cannot start a new instance of the program.")
        sys.exit(-1)

    print("Ejecutando etabs!.")
    #start ETABS application | ejecutar la Aplicacion ETABS.
    ETABSObject.ApplicationStart()

#create SapModel object | crea instancia del objeto SapModel
SapModel = ETABSObject.SapModel


# Unlocking model | Mantener Cerrado modelo (hace referencia al candadito de etabs)
SapModel.SetModelIsLocked(False)

# 'initialize model | Inicializa nuevo modelo en blanco
resUnit = SapModel.InitializeNewModel()

# === FORMAS DE INICIALIZAR UN MODELO ===
# create new blank model | crea una nueva hoja en blanco
# resUnit = SapModel.File.NewBlank()
# create grid-only template model | Crea una nueva hoja con grilla
# resUnit = SapModel.File.NewGridOnly(4,12,12,4,4,24,24)
# create steel deck template model | Crea una nueva hoja de tipo ...
resUnit = SapModel.File.NewSteelDeck(4,12.0,12.0,4,4,24.0,24.0)



# clean up variables | limpiamos las variables y eliminamos
ETABSObject, SapModel, resUnit = None, None, None
del ETABSObject, SapModel, resUnit