# Cloud Conversion Tool

Este tutorial está diseñado con el propósito de presentar los pasos a seguir para ejecutar la aplicación Cloud Conversion Tool. La aplicación utiliza el framework Flask junto con la biblioteca Celery, una base de datos PostgreSQL y un servidor Redis como broker de mesajería.

### Requisitos previos

Debe tener Docker Engine y Docker Compose en su máquina. Para ello, puede realizar cualquiera de las siguientes acciones:

* Instalar Docker Engine y Docker Compose como archivos binarios independientes.
* Instale Docker Desktop, que incluye Docker Engine y Docker Compose.

> No necesita instalar Python, PostgreSQL o Redis, ya que estos son proporcionados por las imágenes de Docker.

### Instrucciones

1. Desde el directorio raiz de la aplicación inicie la aplicación ejecutando el siguiente comando:
   
    ```
    docker compose up
    ```

    Compose crea las imágenes necesarias para el código de la aplicación e inicia los servicios que se definieron. En este caso, el código se copia estáticamente en las imágenes en el momento de la compilación.

2. Ya puede empezar a utilizar los Servicios Web de la aplicación Cloud Conversion Tool