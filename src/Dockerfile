FROM python:3
# añade los ficheros de la carperta actual a la carpeta del disco duro que vamos a crear en el que arrancaremos c
# contenedores de docker
ADD . .
#el run se ejecuta en la compilación de la imagen
RUN pip3 intall -r requirements.txt
#de este ordenador expon a internet el puert 8080
EXPOSE  8080
# qué queremos que haga cuando arranque este ordenador
CMD('python3','-u','app.py')