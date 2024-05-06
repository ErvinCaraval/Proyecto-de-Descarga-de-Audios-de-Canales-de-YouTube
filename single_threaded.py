import json
import os
from datetime import datetime
import subprocess
import timeit
import threading

def download_and_extract_audio(video_url, channel_name):
    output_folder = f'audio/{channel_name}'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Descargar el video con yt-dlp
    subprocess.run(['yt-dlp', '-o', f'{output_folder}/%(title)s.%(ext)s', video_url])

    # Obtener el título del video descargado
    with subprocess.Popen(['yt-dlp', '--get-title', video_url], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True) as process:
        video_title = process.stdout.readline().strip()

    # Construir la ruta del archivo de audio
    audio_file = f'{output_folder}/{video_title}.mp3'

    # Obtener todos los archivos en la carpeta de salida
    all_files = os.listdir(output_folder)

    # Buscar cualquier archivo de video dentro de la carpeta de salida
    video_files = [file for file in all_files if any(file.endswith(extension) for extension in ('.webm', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.part'))]
    if not video_files:
        print(f"Error: No se pudo encontrar ningún archivo de video en '{output_folder}' para '{video_title}' en el canal '{channel_name}'")
        return
    video_file = os.path.join(output_folder, video_files[0])

    print(f"Archivo de video '{video_file}' encontrado para '{video_title}' en el canal '{channel_name}'")

    # Convertir el archivo de video a mp3 usando ffmpeg
    try:
        subprocess.run(['ffmpeg', '-i', video_file, '-vn', '-acodec', 'libmp3lame', audio_file], check=True)
        print(f"Archivo de audio '{audio_file}' creado correctamente para '{video_title}' en el canal '{channel_name}'")
    except subprocess.CalledProcessError as e:
        print('Error en ffmpeg:', e.stderr)

    # Eliminar el archivo de video después de la conversión
    if os.path.exists(video_file):
        os.remove(video_file)

    # Escribir información en el registro de descargas
    with open('registro_de_los_audios_descargados-1.txt', 'a') as log_file:
        log_file.write(f"Audio: {video_title}\n")
        log_file.write(f"Canal: {channel_name}\n")
        log_file.write(f"Fecha de descarga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 50 + "\n")

def main_single_thread():
    with open('data/channels.json', 'r') as file:
        channels = json.load(file)

    for channel in channels:
        channel_name = channel['nombre']
        print(f"Descargando audios del canal '{channel_name}'...")

        for video in channel['videos']:
            video_url = video['url']
            # Descargar y extraer audio en un solo hilo
            download_and_extract_audio(video_url, channel_name)

    print("Todos los audios descargados.")

if __name__ == "__main__":
    # Medir el tiempo de ejecución de toda la aplicación
    execution_time = (timeit.timeit(main_single_thread, number=1))
    print(f"Tiempo de ejecución: {execution_time} segundos")
