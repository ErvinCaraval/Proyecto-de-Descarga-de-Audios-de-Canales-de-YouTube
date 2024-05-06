import json
import os
from datetime import datetime
import subprocess
import threading
import timeit

def get_publish_date(video_url):
    # Obtener la fecha de publicación del video usando yt-dlp
    with subprocess.Popen(['yt-dlp', '--get-publish-date', video_url], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True) as process:
        publish_date = process.stdout.readline().strip()
    return publish_date

def download_and_extract_audio(video_url, channel_name):
    output_folder = f'audio-2/{channel_name}'
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
        print(f"Archivo de audio-2 '{audio_file}' creado correctamente para '{video_title}' en el canal '{channel_name}'")
    except subprocess.CalledProcessError as e:
        print('Error en ffmpeg:', e.stderr)

    # Eliminar el archivo de video después de la conversión
    if os.path.exists(video_file):
        os.remove(video_file)

    # Escribir información en el registro de descargas
    with open('registro_de_los_audios_descargados-2.txt', 'a') as log_file:
        log_file.write(f"Audio-2: {video_title}\n")
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

def main_multithreading(num_threads):
    with open('data/channels.json', 'r') as file:
        channels = json.load(file)

    # Lista para almacenar los hilos
    threads = []

    for channel in channels:
        # Crear un hilo para procesar cada canal
        thread = threading.Thread(target=process_channel, args=(channel,))
        threads.append(thread)
        thread.start()

        # Esperar a que todos los hilos del canal actual terminen
        if len(threads) >= num_threads:
            for t in threads:
                t.join()  # Esperar a que todos los hilos actuales terminen
            threads = []  # Reiniciar la lista de hilos

    # Esperar a que todos los hilos restantes completen su trabajo
    for thread in threads:
        thread.join()

    print("Todos los audios han sido descargados.")

def run_multithreading():
    # Solicitar al usuario que elija el número de hilos
    while True:
        num_threads = input("Por favor, elija el número de hilos (4, 8 o 16): ")
        if num_threads in ['4', '8', '16']:
            num_threads = int(num_threads)
            break
        else:
            print("Opción no válida. Por favor, elija 4, 8 o 16.")

    # Ejecutar el programa con el número de hilos especificado
    main_multithreading(num_threads)

if __name__ == "__main__":
    # Medir el tiempo de ejecución de la función run_multithreading
    execution_time = timeit.timeit(run_multithreading, number=1)
    print(f"Tiempo de ejecución: {execution_time} segundos")
