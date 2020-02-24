# Sentiment Analysis

![Portada](images/sentimentanalysis.jpg)

> Análisis de sentimiento (también conocido como minería de opinión) se refiere al uso de procesamiento de lenguaje natural, análisis de texto y lingüística computacional para identificar y extraer información subjetiva de los recursos. Desde el punto de vista de la minería de textos, el análisis de sentimientos es una tarea de clasificación masiva de documentos de manera automática, en función de la connotación positiva o negativa del lenguaje ocupado en el documento.  — (Wikipedia)

Con esta premisa en este repositorio tenemos una API que podemos utilizar para introducir usuarios, chats y mensajes en nuestra BBDD con MongoDB. Ademas podemos analizar los datos introducidos a la BBDD para analizar el sentimiento de los mensajes y los usuarios e incluso recomendar otros usuarios que se le parezcan.

# Uso de la API:

+ Añadir un usuario:

```/user/create/<name>```
 
+ Añadir un chat:

```/chat/create/<name>```

+ Añadir un usuario al chat:

```/chat/<chat_id>/adduser/<user_id>```

+ Añadir mensajes al chat:

```/messages/<chat_id>/addmessage/<user_id>/<text>```

+ Listar todos los mensajes de un chat:

```/chat/list/<chat_id>'```

+ Listar todos los mensajes de un determinado usuario en un chat:

```/chat/list/user/messages/<chat_id>/<user_id>```

+ Listar todos los usuarios de un chat:

```/chat/list/users/<chat_id>```

+ Analizar cada mensaje de manera independiente con 'NLTK' de un chat:

```/chat/analyze/each/<chat_id>```

+ Analizar todos los mensajes de un chat con 'NLTK':

```/chat/analyze/all/<chat_id>```

+ Analizar todos los mensajes de un chat con 'NLTK' solo para un usuario especifico:

```/chat/analyze/all/user/<chat_id>/<user_id>```

+ Analizar todos los mensajes de un chat con 'NLTK' dividido por usuario:

```/chat/analyze/all/each_user/<chat_id>```

+ Recomendacion de los 3 usuarios mas cercanos al usuario indicado:

```/user/<user_id>/recommend/<chat_id>```



# Recursos:
* [Flask](https://palletsprojects.com/p/flask/)
* [NLTK](https://www.nltk.org/)
* [Docker](https://www.docker.com/)
* [Heroku](https://www.heroku.com/)
* [Jupyter](https://jupyter.org/)
* [Python 3](https://www.python.org/)
* [MongoDB](https://www.mongodb.com/es)
