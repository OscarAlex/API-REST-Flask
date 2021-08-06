#Librerías
from flask import Flask, jsonify, request, render_template, redirect, url_for
from config import config
from flask_mysqldb import MySQL
import re
import json

app= Flask(__name__)
conexion= MySQL(app)

#Obtener todos los registros
@app.route('/datos', methods=['GET'])
def datos():
    try:
        #Conexión y consulta
        cursor= conexion.connection.cursor()
        #Devuelve sólo la información "entendible" (nombres de municipios y estados, no sus códigos) 
        #de los registros
        sql= """SELECT d_codigo, d_asenta, d_CP, d_tipo_asenta, 
                id_asenta_cpcons, d_zona, D_mnpio, d_estado FROM `asenta` 
                JOIN tipo_asenta ON asenta.c_tipo_asenta = tipo_asenta.c_tipo_asenta
                JOIN municipio ON asenta.c_estado = municipio.c_estado AND asenta.c_mnpio = municipio.c_mnpio
                JOIN estado ON asenta.c_estado = estado.c_estado
                ORDER BY d_codigo"""
        cursor.execute(sql)
        datos= cursor.fetchall()
        #Pasar a lista de diccionarios
        asentamientos = []
        for asenta in datos:
            asent= {'d_codigo':asenta[0],
                    'd_asenta':asenta[1],
                    'd_CP':asenta[2],
                    'd_tipo_asenta':asenta[3],
                    'id_asenta_cpcons':asenta[4],
                    'd_zona':asenta[5],
                    'D_mnpio':asenta[6],
                    'd_estado':asenta[7]}
            asentamientos.append(asent)
        return jsonify({
            'mensaje':'Todos los registros',
            'datos':asentamientos
            })
    except:
        return jsonify({
            'mensaje': 'Error al mostrar todos los registros'
            })

#Obtener registro mediante su codigo postal
@app.route('/datos/<d_codigo>', methods=['GET'])
def obtener_cp(d_codigo):
    try:
        #Conexion y consulta
        cursor= conexion.connection.cursor()
        #Devuelve la información de la colonia con el código postal consultado
        sql= """SELECT d_codigo, d_asenta, d_CP, d_tipo_asenta, 
                id_asenta_cpcons, d_zona, D_mnpio, d_estado FROM `asenta` 
                JOIN tipo_asenta ON asenta.c_tipo_asenta = tipo_asenta.c_tipo_asenta
                JOIN municipio ON asenta.c_estado = municipio.c_estado AND asenta.c_mnpio = municipio.c_mnpio
                JOIN estado ON asenta.c_estado = estado.c_estado
                WHERE d_codigo = '{0}'""".format(d_codigo)
        cursor.execute(sql)
        datos= cursor.fetchone()
        #Comprobar que existe un registro con el código postal
        if datos != None:
            asenta= {'d_codigo':datos[0],
                    'd_asenta':datos[1],
                    'd_CP':datos[2],
                    'd_tipo_asenta':datos[3],
                    'id_asenta_cpcons':datos[4],
                    'd_zona':datos[5],
                    'D_mnpio':datos[6],
                    'd_estado':datos[7]}
            return jsonify({
                'mensaje':'Registro encontrado',
                'datos':asenta
            })
        #Si no existe un registro, devolver
        else:
            return jsonify({
                'mensaje':'Registro no encontrado'
            })
    except:
        return jsonify({
            'mensaje':'Error al encontrar registro'
            })

#Obtener colonias por nombre
@app.route('/datos/colonias/<d_asenta>', methods=['GET'])
def obtener_colonia(d_asenta):
    try:
        cursor= conexion.connection.cursor()
        #Devuelve todas las colonias con el nombre consultado
        sql= """SELECT d_codigo, d_asenta, d_CP, d_tipo_asenta, 
                id_asenta_cpcons, d_zona, D_mnpio, d_estado FROM `asenta` 
                JOIN tipo_asenta ON asenta.c_tipo_asenta = tipo_asenta.c_tipo_asenta
                JOIN municipio ON asenta.c_estado = municipio.c_estado AND asenta.c_mnpio = municipio.c_mnpio
                JOIN estado ON asenta.c_estado = estado.c_estado
                WHERE d_asenta = '{0}'""".format(d_asenta.replace('%20', ' '))
        cursor.execute(sql)
        datos= cursor.fetchall()
        #Pasar a lista de diccionarios
        asentamientos= []
        for asenta in datos:
            asent= {'d_codigo':asenta[0],
                    'd_asenta':asenta[1],
                    'd_CP':asenta[2],
                    'd_tipo_asenta':asenta[3],
                    'id_asenta_cpcons':asenta[4],
                    'd_zona':asenta[5],
                    'D_mnpio':asenta[6],
                    'd_estado':asenta[7]}
            asentamientos.append(asent)
        return jsonify({
            'mensaje':'Registros encontrados',
            'datos':asentamientos
        })
    except:
        return jsonify({
            'mensaje':'Error al encontrar colonia por nombre'
        })

#Obtener por nombre de municipio(s)
@app.route('/datos/municipios/<D_mnpio>', methods=['GET'])
def obtener_municipio(D_mnpio):
    try:
        cursor= conexion.connection.cursor()
        #Devuelve todas las colonias de los municipios consultados por nombre
        sql= """SELECT d_codigo, d_asenta, d_CP, d_tipo_asenta, 
                id_asenta_cpcons, d_zona, D_mnpio, d_estado FROM `asenta` 
                JOIN tipo_asenta ON asenta.c_tipo_asenta = tipo_asenta.c_tipo_asenta
                JOIN municipio ON asenta.c_estado = municipio.c_estado AND asenta.c_mnpio = municipio.c_mnpio
                JOIN estado ON asenta.c_estado = estado.c_estado
                WHERE D_mnpio = '{0}'""".format(D_mnpio.replace('%20', ' '))
        cursor.execute(sql)
        datos= cursor.fetchall()
        #Pasar a lista de diccionarios
        municipios= []
        for asenta in datos:
            asent= {'d_codigo':asenta[0],
                    'd_asenta':asenta[1],
                    'd_CP':asenta[2],
                    'd_tipo_asenta':asenta[3],
                    'id_asenta_cpcons':asenta[4],
                    'd_zona':asenta[5],
                    'D_mnpio':asenta[6],
                    'd_estado':asenta[7]}
            municipios.append(asent)
        return jsonify({
            'mensaje':'Registros encontrados',
            'datos':municipios
        })
    except:
        return jsonify({
            'mensaje':'Error al encontrar municipio por nombre'
        })

#Obtener por nombre de estado
@app.route('/datos/estados/<d_estado>', methods=['GET'])
def obtener_estado(d_estado):
    try:
        cursor= conexion.connection.cursor()
        #Devuelve todas las colonias del estado consultado
        sql= """SELECT d_codigo, d_asenta, d_CP, d_tipo_asenta, 
                id_asenta_cpcons, d_zona, D_mnpio, d_estado FROM `asenta` 
                JOIN tipo_asenta ON asenta.c_tipo_asenta = tipo_asenta.c_tipo_asenta
                JOIN municipio ON asenta.c_estado = municipio.c_estado AND asenta.c_mnpio = municipio.c_mnpio
                JOIN estado ON asenta.c_estado = estado.c_estado
                WHERE d_estado = '{0}'""".format(d_estado.replace('%20', ' '))
        #print(d_asenta)
        cursor.execute(sql)
        datos= cursor.fetchall()
        print(datos[0])
        #Pasar a lista de diccionarios
        estados= []
        for asenta in datos:
            asent= {'d_codigo':asenta[0],
                    'd_asenta':asenta[1],
                    'd_CP':asenta[2],
                    'd_tipo_asenta':asenta[3],
                    'id_asenta_cpcons':asenta[4],
                    'd_zona':asenta[5],
                    'D_mnpio':asenta[6],
                    'd_estado':asenta[7]}
            estados.append(asent)
        return jsonify({
            'mensaje':'Registros encontrados',
            'datos':estados
        })
    except:
        return jsonify({
            'mensaje':'Error al encontrar estado por nombre'
        })

#Agregar nuevo registro
@app.route('/datos', methods=['POST'])
def agregar_registro():
    try:
        #Comprobar que los códigos tengan 5 caracteres
        if len(request.json['d_codigo']) != 5 or len(request.json['d_CP']) != 5:
            return jsonify ({ 
                    'mensaje':'Ambos códigos deben tener 5 caracteres'
                })
        #Comprobar que no hayan caracteres invalidos en los códigos
        a1= re.search("[A-Za-z@,;.\'\"¡!¿?\-/\s]", request.json['d_codigo'])
        a2= re.search("[A-Za-z@,;.\'\"¡!¿?\-/\s]", request.json['d_CP'])
        a3= re.search("[A-Za-z@,;.\'\"¡!¿?\-/\s]", request.json['id_asenta_cpcons'])
        print(a1, a2)
        if a1 or a2 or a3:
            return jsonify ({ 
                    'mensaje':'Todos los códigos deben tener caracteres válidos'
                })

        cursor= conexion.connection.cursor()
        #Obtener los id de las colonias y los códigos de los municipios
        sql= """SELECT id_asenta_cpcons, c_estado, c_mnpio FROM `asenta`"""
        cursor.execute(sql)
        datos_ids= cursor.fetchall()
        #Convertir a lista de diccionarios
        ids = []
        for asenta in datos_ids:
            asent= {'id_asenta_cpcons':asenta[0],
                    'c_estado':asenta[1],
                    'c_mnpio':asenta[2]
                    }
            ids.append(asent)
        #Diccionario con el código y nombre del registro nuevo
        id_aux= {
            'id_asenta_cpcons':request.json['id_asenta_cpcons'], 
            'c_estado':int(request.json['c_estado']),
            'c_mnpio':request.json['c_mnpio']
            }
        print(ids[:5])
        print(id_aux)
        #Comprobar que el id de municipio del nuevo registro no exista ya en un municipio
        #Si no es así, continua
        if id_aux not in ids:
            #Obtener los códigos y nombres de las colonias
            sql= """SELECT d_codigo, d_asenta FROM `asenta`"""
            cursor.execute(sql)
            datos= cursor.fetchall()
            #Convertir a lista de diccionarios
            asentamientos = []
            for asenta in datos:
                asent= {'d_codigo':asenta[0],
                        'd_asenta':asenta[1]
                        }
                asentamientos.append(asent)
            #Diccionario con el código y nombre del registro nuevo
            aux= {
                'd_codigo':request.json['d_codigo'], 
                'd_asenta':request.json['d_asenta']
                }
            
            #Comprobar que el nuevo registro no tenga un código y nombre ya existentes
            #Si no es así, lo agrega
            if aux not in asentamientos:
                #Agrega a la tabla 'asenta'
                sql= """INSERT INTO `asenta` (d_codigo, d_asenta, d_CP, c_tipo_asenta, 
                id_asenta_cpcons, d_zona, c_estado, c_mnpio) 
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')""".format(
                    request.json['d_codigo'], request.json['d_asenta'], request.json['d_CP'], request.json['c_tipo_asenta'],
                    request.json['id_asenta_cpcons'], request.json['d_zona'], request.json['c_estado'], request.json['c_mnpio']
                )
                cursor.execute(sql)
                #Confirmar
                conexion.connection.commit()
                return jsonify ({
                    'mensaje':'Recurso registrado'
                })
            #Si el nuevo registro tiene un código y nombre ya existentes
            else:
                return jsonify ({
                    'mensaje':'Ya existe una colonia con este código'
                })
        #Si el nuevo registro tiene un id ya existente en un municipio
        else:
            return jsonify ({
                'mensaje':'Este id ya existe en el municipio que intentas agregar'
            })
    except:
        return jsonify({
            'mensaje':'Error al registrar'
        })

#Error por defecto
def error_defecto(err):
    return jsonify({
            'mensaje':'Página no encontrada'
        }), 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, error_defecto)
    app.run()