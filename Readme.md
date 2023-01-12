# Roberto, el robot que siente

El proyecto consiste en ojos animatrónicos que fijan la mirada en las personas e imitam sus movimientos de cabeza y emociones.

## Descripción

Roberto puede:
* Emitir sonidos de risa al ver sonreír a una persona y sonidos de llanto al detectar que una persona está con cara triste.
* Imitar el movimiento de inclinar la cabeza al costado.
* Seguir con la mirada a las personas y girando el cuello (Como haciendo el gesto de "No")

![Image text](https://github.com/gmfv/Roberto-el-robot-que-siente/blob/main/Roberto_Frontal%20(1).jpg)

[Videos ilustrativos del funcionamiento](https://drive.google.com/drive/folders/1FE7oooqcs98mvzBAV36Hg5GqQWTchDLI?usp=share_link)

## Iniciando
### Materiales
* Raspberry pi +3B
* Módulo de Cámara para Raspberry pi 1080P HD 
* Adafruit 16-Channel 12 bit PWM/Servo driver
* Arduino 
* Micro servo motores x4
* Servo motores de alto torque x3
* Impresiones 3D de los ojos y sus soportes (Se han utilizado las piezas de [James Bruton](https://github.com/XRobots/ServoSmoothing/tree/main/CAD)). 
* Tornillos M3 y M2
* Parlante pequeño

![Image text](https://github.com/gmfv/Roberto-el-robot-que-siente/blob/main/Isometrico_Roberto%20(1).jpg)

* Impresión del porta-cámara (Diseño propio. Incluido en el proyecto)

![Image text](https://github.com/gmfv/Roberto-el-robot-que-siente/blob/main/Soporte_Camara1%20(1).jpg)  ![Image text](https://github.com/gmfv/Roberto-el-robot-que-siente/blob/main/Soporte_Camara2%20(1).jpg)   ![Image text](https://github.com/gmfv/Roberto-el-robot-que-siente/blob/main/Soporte_Camara3%20(1).jpg)

### Prerequisitos
* Descargar el modelo de marcadores faciales de [esta página](https://www.kaggle.com/datasets/codebreaker619/face-landmark-shape-predictor). El archivo se llama shape_predictor_68_face_landmarks.dat, colocarla en la misma carpeta que el código de video_facial_landmark.py

### Ejecutar el programa (Windows)
* Clonar el repositorio
* Abrir el command prompt en la carpeta y ejecutar la siguiente línea: 
      python video_facial_landmark.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1
      
## Autores
* [Giohanna Martínez](https://github.com/gmfv)
* [Diego Valenzuela](https://github.com/ValenzuelaDiego)
