
import pandas as pd
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Convierte un archivo .xlsx a .csv con codificación UTF-8'

    def add_arguments(self, parser):
        parser.add_argument('input_path', type=str, help='Ruta completa del archivo .xlsx de entrada.')
        parser.add_argument('output_path', type=str, help='Ruta completa del archivo .csv de salida.')

    def handle(self, *args, **options):
        input_path = options['input_path']
        output_path = options['output_path']

        try:
            self.stdout.write(self.style.NOTICE(f'Iniciando conversión de {input_path}...'))
            
            # Leer el archivo Excel
            df = pd.read_excel(input_path, engine='openpyxl')
            
            # Guardar como CSV con codificación UTF-8
            df.to_csv(output_path, index=False, sep=',', encoding='utf-8')
            
            self.stdout.write(self.style.SUCCESS(f'Archivo convertido exitosamente a {output_path}'))
        
        except FileNotFoundError:
            raise CommandError(f'Error: El archivo {input_path} no existe.')
        
        except PermissionError:
            raise CommandError(f'Error: No se tiene permiso para escribir en {output_path}.')
        
        except Exception as e:
            raise CommandError(f'Error inesperado durante la conversión: {e}')
