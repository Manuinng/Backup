import paramiko
import time
from .models import Equipo, detalle_backup, backup
import socket
import os
import logging
from django.core.files.base import ContentFile

logging.basicConfig(filename='respaldo_individual.log', level=logging.INFO)

def respaldo_individual(equipo_id):
    port = '22'
    username = 'cisco'
    password = 'cisco'
    #enable = 'contrasena'
    private_key = '/Users/manui/.ssh/id_rsa.pub'
    host_name = socket.gethostname()
    #ip_tftp = socket.gethostbyname(host_name)
    ruta_respaldo = "/home/manu/tftp/"

    try:
        equipo = Equipo.objects.get(id=equipo_id)
        ip_equipo = equipo.ip
        filename = f"{ip_equipo}_{time.strftime('%Y%m%d%H%M%S')}.txt"
        filenameh = f"{'backup'} {time.strftime('%d/%m/%Y %H:%M:%S')}"
        filenamerute = os.path.join(ruta_respaldo, filename)

        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #ssh_key = paramiko.RSAKey(filename=private_key)
            ssh_client.connect(ip_equipo, port, username, password, allow_agent=False, look_for_keys=False)

            channel = ssh_client.invoke_shell()
            channel.send("copy startup-config tftp:\n")
            channel.send("192.168.1.20\n")
            channel.send(filename + "\n")
            time.sleep(2)
            ssh_client.close()

        with open(filenamerute, 'rb') as file:
                contenido_archivo = file.read()
                backup_obj = backup.objects.create(name_backup=filenameh)
                detalle = detalle_backup.objects.create(
                    status=0,
                    registro="Respaldo exitoso",
                    id_equipo=equipo,
                    id_backup=backup_obj,
                )
                detalle.contenido.save(filename, ContentFile(contenido_archivo))
                print(f"Respaldo exitoso del equipo con IP {ip_equipo}")
    except Equipo.DoesNotExist:
        backup_obj = backup.objects.create(name_backup=filenameh)
        detalle_backup.objects.create(
            status=1,
            registro=f"Respaldo Fallido, No se encontró un equipo con ID {equipo_id}",
            id_equipo=equipo,
        )
    except paramiko.SSHException as ssh_error:
        backup_obj = backup.objects.create(name_backup=filename)
        detalle_backup.objects.create(
            status=1,
            registro=f"Respaldo Fallido: {ssh_error}",
            id_equipo=equipo,
        )
    except FileNotFoundError as file_error:
        backup_obj = backup.objects.create(name_backup=filename)
        detalle_backup.objects.create(
            status=1,
            registro=f"Respaldo Fallido: {file_error}",
            id_equipo=equipo,
        )
    except Exception as e:
        backup_obj = backup.objects.create(name_backup=filename)
        detalle_backup.objects.create(
            status=1,
            registro=f"Respaldo Fallido: {e}",
            id_equipo=equipo,
        )
