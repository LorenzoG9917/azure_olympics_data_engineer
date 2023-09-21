# Olympics Data Engineering Project

## Objetivo
Este repositorio busca emular un proyecto 'end to end' que simula casos del mundo laboral, empleando herramientas empresariales basadas en la nube como Azure Data Lake Gen2, Data Factory, Azure Databricks, Azure Synapse Analytics y Power BI Desktop. El enfoque principal es realizar un proceso ETL y generar informes de inteligencia empresarial (BI).

## Descripción
Este proyecto ejemplifica un proceso integral de gestión de datos en la nube. Comienza con la ingesta de datos en un datalake mediante Azure Data Factory. Luego, se aplican transformaciones en Azure Databricks con PySpark y se almacenan los datos transformados. A continuación, se crean tablas en Azure Synapse Analytics (Database tipo serverless) desde estos datos transformados y se accede a ellos mediante Power BI Desktop para la creación de informes. 

## Arquitectura
![arquitectura](https://github.com/LorenzoG9917/azure_olympics_data_engineer/assets/121797266/f9ca6e25-9968-40c6-a389-e13124eaa2f3)

## Tecnologías usadas
- **Azure Data Lake Storage Gen2(ADLS2)**: Un sistema de almacenamiento en la nube altamente escalable y seguro para el almacenamiento y análisis de datos a gran escala.
- **Azure Data Factory**: Un servicio de orquestación de datos que permite crear, programar y orquestar flujos de trabajo de extracción, transformación y carga (ETL) de datos.
- **PySpark**: Una biblioteca de Python que facilita el procesamiento de datos distribuidos utilizando Apache Spark.
- **Synapse Analytics**: Una plataforma de análisis de datos unificada que combina el análisis de big data y el procesamiento de datos en un único servicio.
- **Power BI Desktop**: Una aplicación de visualización de datos que permite crear informes interactivos y paneles de control a partir de datos diversos para la toma de decisiones empresariales.

## Data usada
Estos archivos forman parte de un [conjunto de datos](https://github.com/LorenzoG9917/tokyo-olympic-azure-data-engineering-project/tree/main/data) relacionados con los Juegos Olímpicos y se utilizan para realizar análisis y generar informes sobre el rendimiento de atletas, entrenadores, equipos y disciplinas deportivas en dicho evento.
- Athletes.csv: Contiene información sobre los atletas que participan en los Juegos Olímpicos, incluyendo sus nombres, países y disciplinas deportivas.

- Coaches.csv: Este archivo registra datos sobre los entrenadores involucrados en los Juegos Olímpicos, incluyendo sus nombres, países, disciplinas deportivas y eventos específicos en los que están involucrados.

- EntriesGender.csv: Proporciona información sobre las disciplinas olímpicas, desglosando la cantidad de participantes masculinos, femeninos y el total de participantes en cada disciplina.

- Medals.csv: Registra el desempeño de los equipos en los Juegos Olímpicos, incluyendo su rango de clasificación, país o equipo, así como la cantidad de medallas de oro, plata y bronce ganadas.

- Teams.csv: Contiene datos sobre los equipos que compiten en los Juegos Olímpicos, incluyendo el nombre del equipo, la disciplina en la que compiten, el país al que pertenecen y el evento específico en el que participan.


## Paso a paso
### Paso 1: Crear un grupo de recursos general
Crea un grupo de recursos en Azure llamado "tokio-olympic-data" donde centralizarás todos los recursos relacionados con tu proyecto.
### Paso 2: Crear Azure Data Lake Storage Gen2 (ADLS2)
- Dentro del grupo de recursos, crea un servicio de Azure Data Lake Storage Gen2 (ADLS2).
- Crea un contenedor llamado "tokyo-olympic-data" dentro de ADLS2.
- Dentro del contenedor, crea dos carpetas llamadas "Raw" y "Transformed-data" para organizar los datos.
### Paso 3: Crear un servicio de Azure Data Factory (ADF)
- Crea un servicio de Azure Data Factory en tu grupo de recursos.
- Crea un nuevo pipeline llamado pl_copydata
### Paso 4: Crear actividad de copy data
- Elegir la actividad de copy data.Tener en cuenta que este paso debe repetirse para cada uno de los datasets.
### Paso 5: Crear Linked Services para el origen de los datos
- Crea Linked Services en ADF para el origen de los datos. Como tus datos están alojados en GitHub, estos Linked Services deben ser de tipo HTTP.
- Configura los Linked Services con las URL correspondientes para acceder a tus archivos.
### Paso 6: Crear Linked Services para el sink (destino)
- Crea Linked Services en ADF para el sink, que en este caso es Azure Data Lake Gen2. Debes especificar que deseas escribir en la carpeta "Raw" de tu Data Lake Gen2.
### Paso 7: Crear los respectivos Datasets
- Crea Datasets en ADF, uno de tipo HTTP y otro de tipo Data Lake Gen2.
- Configura los Datasets para que tengan el formato de texto delimitado por comas (CSV) ya que tus archivos son CSV.

### Paso 8: Ejecutar pipeline
- Se debe ejecutar el pipeline y verificar que la actividad de copy data resulte efectiva para cada uno de los datasets.
- Revisar que cada uno de los archivos resida en la capa Raw de tu Data Lake Gen2.
![data_factory1](https://github.com/LorenzoG9917/azure_olympics_data_engineer/assets/121797266/c07806df-042f-495b-a6cf-f9fa6ba222cb)
![data_factory2](https://github.com/LorenzoG9917/azure_olympics_data_engineer/assets/121797266/e4e8dac3-9f6d-43ce-bc6d-d0b6d16becb4)

### Paso 9: Configurar Azure Databricks
- Crear servicio tipo Azure Databricks dentro del grupo de recursos creado al inicio del proyecto.
- Accede a la interfaz gráfica de Azure Databricks.
- Crea un clúster que te permitirá ejecutar tus notebooks.
### Paso 10: Configurar acceso a Data Lake Gen2 desde Databricks
- Crea un servicio de Azure llamado "App registrations".
- Registra una nueva aplicación con un nombre como "app01".
- Esto generará un Application (client) ID y un Directory(tenant)ID que necesitarás para autenticarte desde Databricks.

### Paso 11: Crear un client secret
- En la aplicación "app01", crea un cliente secreto (client secret) y dale un nombre como "secretKey".
- Esto generara dos valores:  Secretkey(Value) y Secret ID
- El que se empleara es el Secretkey(Value)
### Paso 12: Configurar acceso desde el notebook de Databricks
En tu notebook de Databricks, incluye un código que te permita autenticarte y acceder a tu Data Lake Gen2 utilizando los datos de "app01" y el respectivo secretkey(value) creado en el paso anterior

```
configs = {"fs.azure.account.auth.type": "OAuth",
"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
"fs.azure.account.oauth2.client.id": "[Application(client)ID]" # ACTUALIZAR,
"fs.azure.account.oauth2.client.secret": '[Secretkey(Value)]' # ACTUALIZAR,
"fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/[Directory(tenant)ID]/oauth2/token" # ACTUALIZAR}

dbutils.fs.mount(
source = "abfss://[NombreContainer]@[NombreStorageAccount].dfs.core.windows.net", # contrainer@storageacc
mount_point = "/mnt/tokyoolymic",
extra_configs = configs)
```

### Paso 13: Asignar roles de Storage Contributor
- Asigna el rol de "Storage Contributor" a la aplicación "app01" que creaste en tu grupo de recursos. Esto garantiza que tenga los permisos necesarios para acceder y modificar los datos en Data Lake Gen2.

### Paso 14 Ejecutar el Notebook de Transformación: 
- Ejecuta el notebook en Azure Databricks donde realizas las transformaciones necesarias en los datos. Esto puede incluir cambios en el tipo de dato, limpieza y procesamiento adicional.
- Una vez que hayas completado las transformaciones, el código carga los datos resultantes en la carpeta "transformed-data" en tu Data Lake Gen2.

### Paso 15: Crear Azure Synapse Analytics
- Crea un servicio de Azure Synapse Analytics en tu grupo de recursos.
- Anotar el usuario y contraseña de la base de datos que se crea por defecto
- Dentro de Synapse Analytics, crea una SQL Pool Serverless que denominaremos "olympics-db". Esta base de datos será utilizada para consultar tus datos transformados.

### Paso 16: Generar  Shared access signature de nuestro Storage Account (ADLS2)
- Necesitamos hacer un puente entre Synapse y Data Lake Gen 2, por ende debemos generar un SAS el cual permita acceder al data lake y a todos sus recursos.
- Tener en cuenta que este SAS(Key) dura por defecto 8 horas por ende debe modificarse según su necesidad.

### Paso 16 : Crear tablas externas en base de datos "olympics-db"
- Para crear las tablas externas debemos antes realizar una serie de pasos (Crear  external data source y Crear formato)
- Data source se refiere a de donde proviene nuestra data en nuestro caso es la capa transformed-data ubicada en el Data Lake Gen2.
- Para crear el data source debemos crear un scope que nos permita acceder a nuestro Data Lake Gen2, el scope necesita el SAS creado en el paso anterior.
```
-- Create credentials
CREATE DATABASE SCOPED CREDENTIAL SasCredentialDemo
WITH IDENTITY = 'SHARED ACCESS SIGNATURE', 
SECRET = '[SASKeyGenerado]'
GO
```
- Crear formato tipo CSV
```
-- Create format
CREATE EXTERNAL FILE FORMAT CSV
WITH (FORMAT_TYPE = DELIMITEDTEXT,
      FORMAT_OPTIONS(
          FIELD_TERMINATOR = ',',
          USE_TYPE_DEFAULT = True,
          FIRST_ROW=2)
);
GO
```
- Crear external data source , donde hacemos referencia a nuestro Data Lake Storage Primary endpoint y usamos el scope previamente creado.
```
-- Creanos un external data
CREATE EXTERNAL DATA SOURCE olympicsdatalg17 WITH (
    LOCATION = 'https://tokyoolympicdatalg.dfs.core.windows.net/', CREDENTIAL = SasCredentialDemo
);
GO
```
- Crear external table (Este paso debe realizarse con todos los archivos). Usamos el data source previamente creado y procedemos a especificar la location de nuestra data (container/carpeta/nombre_archivo)
```
--Create table athletes
CREATE EXTERNAL TABLE athletes (
    PersonName VARCHAR(75),
    Country VARCHAR(75),
    Discipline VARCHAR(75)  
)
with (
LOCATION = 'tokyo-olympic-data/transformed-data/athletes',
DATA_SOURCE = olympicsdatalg17,
FILE_FORMAT = CSV
)
GO
```
### Paso 17: Conexión de Power BI Desktop a Synapse SQL Pool Serverless "olympics-db"
- Incializar el Power BI Desktop
- Seleccionar la opción obtener datos (Azure)
- Nos solicita poner la dirección del servidor y el puerto, en nuestro caso usaremos el Serverless SQL endpoint el cual podemos encontrar en la sección de propiedades de nuestro Synapse.
- Ejemplo de Serverless SQL endpoint: synapse-name-ondemand.sql.azuresynapse.net
- Posterior nos logeamos con el user y password creados en el paso 15.

### Paso 18: Crear dashboard final
- Crea un dashboard final que presente los datos de manera efectiva y genere los informes necesarios basados en tus datos transformados.
- Añade gráficos, tablas y filtros según sea necesario para crear un informe completo.

## Agradecimientos

- Agradecimientos especiales a [Darshil Parmar](https://www.linkedin.com/in/darshil-parmar/) por la creación de este proyecto con fines educativos.


## Autor

Este repositorio ha sido personalizado y adaptado por [Lorenzo Guerrero](https://www.linkedin.com/feed/) con fines educativos.









