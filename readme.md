## Proyecto Final Coderhouse Python
+ Comision:40440
+ Alumno: Joaquin Guerrero

## Version
1.0

## Descripcion del Proyecto
Página web destinada a usuarios que deseen subir sus publicaciones (estilo noticias).

El usuario tendrá la oportunidad de navegar por el sitio sin estar logueado, pero para aprovechar el sitio al 100%, deberá ingresar con su cuenta. Si no tiene una cuenta, se le dará la oportunidad de registrarse.

Las personas que utilizan el sitio web sin estar logueadas podrán:
+ Ver las publicaciones
+ Buscar las publicacines
+ Ver la página "Acerca de mí"
+ Acceder a la página para iniciar sesión. En caso de no tener una cuenta, podrán ingresar a la página de registro

Las personas que ingresan con su usuario podrán hacer lo mismo que las personas no logueadas y además podrán realizar las siguientes acciones:
+ Crear publicacion
+ El usuario que creó la publicación también podrá editarla y eliminarla
+ Editar el perfil del usuario
+ Agregar una foto de perfil
+ Ver el perfil del creador de la publicación
+ Cambiar la contraseña del usuario

## Tecnología Utilizada
+ HTML 5
+ CSS 3
+ Bootstrap 5
+ Python 
+ Django

## Instrucciones instalar proyecto en local
+ Crea una carpeta contenedora madre
+ Abre la consola y ubicate en la carpeta madre
+ Crea y activa el ambiente virtual
+ Clona este proyecto en la carpeta madre
+ Entra en la carpeta que acabas de clonar
+ Para instalar las dependencias corre este comando:

```
pip install -r requirements.txt
```
## Instrucciones para entrar al panel aministrativo de Django
+ En consola, crear un superuser:
```
python manage.py createsuperuser
```
+ Acceder con user y password via:
```
127.0.0.1:8000/admin
```

## Tests
Los tests estan ubicados en las app
+ Para el tests de la app usuario:
```
python manage.py test usuarios.tests
```
+ Para el tests de la app publicaciones:
```
python manage.py test publicaciones.tests
```
## Video
https://youtu.be/U4rIuyFfXt8