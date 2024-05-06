# Proyecto de Descarga de Audios de Canales de YouTube

## Integrantes:
- Nombre: Ervin Caravali Ibarra
- Código: 1925648
- Correo Electrónico Institucional: ervin.caravali@correonivalle.edu.co

## Descripción de Requerimientos:
El objetivo de este proyecto es descargar audios de videos de diferentes canales de YouTube. Se proporcionan varios scripts para llevar a cabo esta tarea de manera secuencial, multihilo y multiproceso, permitiendo una descarga eficiente y escalable.

Al acceder a la carpeta del proyecto, encontrarás dos archivos ZIP. En estos archivos se encuentran comprimidos los audios de los videos utilizando la versión de un hilo del aplicativo. También encontrarás los informes de descarga de las tres versiones del aplicativo.

## Forma de Uso o Ejecución:

### Ejecución Secuencial:
Para ejecutar el script `single_threaded.py`, sigue estos pasos:
1. Asegúrate de tener instalados los paquetes necesarios especificados en el archivo `requirements.txt`.
2. Ejecuta el siguiente comando en tu terminal:
   ```bash
   python single_threaded.py
   ```
3. El script descargará los audios de los videos de cada canal de manera secuencial.

### Ejecución Multihilo:
Para ejecutar el script `multithreaded.py`, sigue estos pasos:
1. Asegúrate de tener instalados los paquetes necesarios especificados en el archivo `requirements.txt`.
2. Ejecuta el siguiente comando en tu terminal:
   ```bash
   python multithreaded.py
   ```
3. El script descargará los audios de los videos de cada canal utilizando múltiples hilos para una descarga más rápida.

4. Después de la ejecución del script, se recomienda eliminar los archivos generados en la carpeta audio para evitar sobrescrituras y problemas en futuras descargas.Esto hagalo en todas las verciones de este aplicativo.

### Ejecución Multiproceso:
Para ejecutar el script `multiprocessing.py`, sigue estos pasos:
1. Asegúrate de tener instalados los paquetes necesarios especificados en el archivo `requirements.txt`.
2. Ejecuta el siguiente comando en tu terminal:
   ```bash
   python multiprocessing.py
   ```
3. El script descargará los audios de los videos de cada canal utilizando múltiples procesos para una descarga más rápida.

## Descripción de la Lógica del Aplicativo:

### single_threaded.py:
- Este script descarga los audios de los videos de cada canal de manera secuencial.
- Utiliza el módulo `subprocess` para ejecutar comandos de terminal y descargar los videos con `yt-dlp`.
- Utiliza la biblioteca `ffmpeg` para convertir los videos descargados a archivos de audio.
- Crea un registro de las descargas en el archivo `registro_de_los_audios_descargados-1.txt`.

### multithreaded.py:
- Este script descarga los audios de los videos de cada canal utilizando múltiples hilos para una descarga paralela.
- Utiliza el módulo `threading` para crear hilos que descargan los videos de manera simultánea.
- Crea un registro de las descargas en el archivo `registro_de_los_audios_descargados-2.txt`.

### multiprocessing.py:
- Este script descarga los audios de los videos de cada canal utilizando múltiples procesos para una descarga paralela.
- Utiliza el módulo `multiprocessing` para crear procesos que descargan los videos de manera simultánea.
- Crea un registro de las descargas en el archivo `registro_de_los_audios_descargados-3.txt`.

## Archivos Generados:
- Se generarán carpetas dentro de los directorios `audio`, `audio-2` y `audio-3`, donde se almacenarán los archivos de audio descargados. estos directorios antes mencionados se generaran de forma atomatica al correr los archivos.py
- Además, se generarán archivos de registro (`registro_de_los_audios_descargados-1.txt`, `registro_de_los_audios_descargados-2.txt` y `registro_de_los_audios_descargados-3.txt`) que contienen información sobre las descargas realizadas.

