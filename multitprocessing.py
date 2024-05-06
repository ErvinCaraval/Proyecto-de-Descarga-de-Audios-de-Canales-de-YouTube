import json
import os
from datetime import datetime
import subprocess
import multiprocessing
import timeit

def get_publish_date(video_url):
    # Obtener la fecha de publicación del video usando yt-dlp
    with subprocess.Popen(['yt-dlp', '--get-publish-date', video_url], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True) as process:
        publish_date = process.stdout.readline().strip()
    return publish_date

def download_and_extract_audio(video_url, channel_name):
    output_folder = f'audio-3/{channel_name}'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Obtener la fecha de publicación del video
    publish_date = get_publish_date(video_url)

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
    with open('registro_de_los_audios_descargados-3.txt', 'a') as log_file:
        log_file.write(f"Audio-3: {video_title}\n")
        log_file.write(f"Canal: {channel_name}\n")
        log_file.write(f"Fecha de publicación: {publish_date}\n")
        log_file.write(f"Fecha de descarga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 50 + "\n")

def process_channel(channel):
    channel_name = channel['nombre']
    print(f"Descargando audios del canal '{channel_name}'...")

    for video in channel['videos']:
        video_url = video['url']
        # Descargar y extraer audio de cada video
        download_and_extract_audio(video_url, channel_name)

    print(f"Todos los audios del canal '{channel_name}' han sido descargados.")

def run_multiprocessing(num_processes):
    with open('data/channels.json', 'r') as file:
        channels = json.load(file)

    # Lista para almacenar los procesos
    processes = []

    for channel in channels:
        # Crear un proceso para procesar cada canal
        process = multiprocessing.Process(target=process_channel, args=(channel,))
        processes.append(process)
        process.start()

        # Limitar el número de procesos en ejecución
        if len(processes) >= num_processes:
            for p in processes:
                p.join()  # Esperar a que todos los procesos actuales terminen
            processes = []  # Reiniciar la lista de procesos

    # Esperar a que todos los procesos restantes completen su trabajo
    for process in processes:
        process.join()

    print("Todos los audios han sido descargados.")

if __name__ == "__main__":
    while True:
        num_processes = input("Por favor, elija el número de procesos (4, 8 o 16): ")
        if num_processes in ['4', '8', '16']:
            num_processes = int(num_processes)
            break
        else:
            print("Opción no válida. Por favor, elija 4, 8 o 16.")

    # Medir el tiempo de ejecución de la función run_multiprocessing
    execution_time = timeit.timeit(lambda: run_multiprocessing(num_processes), number=1)
    print(f"Tiempo de ejecución: {execution_time} segundos")
