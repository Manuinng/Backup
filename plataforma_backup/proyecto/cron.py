from .realizar_respaldos import realizar_respaldo
import os

def programa():
   directorio = '/home/manu/backup/plataforma_backup'
   os.chdir(directorio)
   realizar_respaldo()

