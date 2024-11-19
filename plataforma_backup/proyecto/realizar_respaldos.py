import paramiko
import time
import os
import socket
import logging
from django.utils import timezone
from .models import Equipo, detalle_backup, backup
from django.core.files.base import ContentFile

logging.basicConfig(filename='respaldo.log', level=logging.INFO)

port = '22'
username = 'cisco'
password = 'cisco'
#enable = 'contrasena'
private_key = '/Users/manui/.ssh/id_rsa.pub'
host_name = socket.gethostname()
#ip_tftp = socket.gethostbyname(host_name)
ruta_respaldo = "/home/manu/tftp/"

def realizar_respaldo():
    global ip_tftp
    global port

    equipos = Equipo.objects.all()
    filenameh = f"{'backup'} {time.strftime('%d/%m/%Y %H:%M:%S')}"
    backup_obj = backup.objects.create(name_backup=filenameh)
    for equipo in equipos:
        ip = equipo.ip
        filename = f"{ip}_{time.strftime('%Y%m%d%H%M%S')}.txt"
        filenamerute = os.path.join(ruta_respaldo, filename)

        try:
            with paramiko.SSHClient() as ssh_client:
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #ssh_key = paramiko.RSAKey(filename=private_key)
                ssh_client.connect(ip, port, username, password, allow_agent=False, look_for_keys=False)

                channel = ssh_client.invoke_shell()
                channel.send("copy startup-config tftp:\n")
                channel.send("192.168.1.20\n")
                channel.send(filename + "\n")
                time.sleep(2)
                ssh_client.close()
            with open(filenamerute, 'rb') as file:
                contenido_archivo = file.read()
                detalle = detalle_backup.objects.create(
                    status=0,
                    registro="Respaldo exitoso",
                    id_equipo=equipo,
                    id_backup=backup_obj,
                )
                detalle.contenido.save(filename, ContentFile(contenido_archivo))
                logging.info(f"Respaldo exitoso del equipo {equipo.name_equipo} ({ip})")
        except Equipo.DoesNotExist:
            backup_obj = backup.objects.create(name_backup=filenameh)
            detalle_backup.objects.create(
                status=1,
                registro=f"Respaldo Fallido, No se encontró un equipo con ID {equipo.id}",
                id_equipo=equipo,
            )
        except paramiko.SSHException as ssh_error:
            detalle_backup.objects.create(
                status=1,
                registro=f"Error de SSH: {ssh_error}",
                id_equipo=equipo,
            )
            logging.error(f"Error de SSH: {ssh_error}")
        except FileNotFoundError as file_error:
            detalle_backup.objects.create(
                status=1,
                registro=f"Error al encontrar el archivo: {file_error}",
                id_equipo=equipo,
            )
            logging.error(f"Error al encontrar el archivo : {file_error}")
        except Exception as e:
            detalle_backup.objects.create(
                status=1,
                registro=f"Error desconocido al respaldar: {e}",
                id_equipo=equipo,
            )
            logging.error(f"Error desconocido al respaldar: {e}")

if __name__ == "__main__":
    realizar_respaldo()


