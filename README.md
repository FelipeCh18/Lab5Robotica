# Laboratorio 5 - Cinemática Inversa - Phantom X - ROS

***INTEGRANTES***

* Marco Antonio Quimbay Dueñas
* Felipe Chaves Delgadillo

Para llevar a cabo la práctica, el primer paso consistió en hacer la Cinemática Directa del Robot en la posición de Home y así obtener los parámetros de DH. En la figura pueden observarse las distintas distancias que existen entre los eslabones del robot, y sus respectivas magnitudes, adquiridas mediante el uso de un calibrador.

![modelo_directo](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/83827043-6be3-48f2-85b6-bc4c53030b74)


Obteniendo la siguiente DH:

![DHstd](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/4e220a19-04ba-4b2e-8b4f-fef564e8117b)

## Implementación en ROS

Después de sacar el modelo geométrico inverso, se procedió a implementar la solución en ROS teniendo en cuenta las recomendaciones de la guía, por lo que para realizar dichos puntos, se hizo un solo programa en la cual se integra todos los puntos, primero importamos las librerias necesarias para el funcionamiento del programa:

![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/f9cdaa56-9e62-4e63-905a-9e8296c0c502)


Después programamos lo que es la cadena cinemática del robot con los parámetros DH encontrados al principio, con la ayuda de la libreria de Peter Corke:

![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/857bbfbc-1dae-4198-b9cc-87978045ef0a)



Ahora debemos programar el modelo cinemático inverso teniendo en cuenta que el piso está mucho más abajo de la base del robot por lo que se deben programar unas coordenadas auxiliares y esta función nos devuelve los ángulos respectivos de cada unión:

![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/84db8f81-9d9d-49d2-a175-e80c85fc628d)



Ahora programamos la función del publicador de posición en el cual mostramos la posición espacial del TCP, y se realiza la cinemática inversa del punto actual para luego enviarlos al tópico respectivo:

![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/f7941caa-d32e-47f7-8086-0bcc7235efce)



Ahora programamos lo que es el publicador de los ángulos de las uniones, la idea es complementar el publicador anterior: 

![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/917f89f6-2264-4d68-abf4-99d6cc1f2a7d)

Por último programamos lo que es el programa principal en forma de función, aquí vamos a utilizar las funciones anteriores para realizar las rutinas de dibujo las cuales corresponden al dibujo del área máxima y mínima de dibujo, las iniciales de los nombres de los integrantes del grupo, un circulo y por último, triangulo con una x dibujada en el medio, para cada rutina se importa la imagen con CV2 y se muetsra, una vez cerrada la imagen, el robot comienza la rutina elegida y cada una tiene una lista de puntos, los cuales indican las posiciones de todos los lugares en donde se dibuja y el tiempo de ejecución de cada rutina: 

![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/9b09c2b6-3253-4b0b-8510-6bf3002f1977)
![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/bc30d475-f6da-4cd5-96e3-23ca6dbe82bd)
![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/70da213a-c897-41b5-8b94-68d3c92aaa92)
![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/a707b723-9590-43cf-aab8-c63b20b58309)
![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/ef1ab418-fbf5-4312-809e-496bbda2bd8f)
![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/c727ac7a-5909-4a19-a791-035a43854d2e)
![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/37d2d17b-1e99-4956-bc79-8edcbc084fb3)





Finalmente, tenemos el código principal en el cual se llama la función principal y se da un tiempo de espera entre llamadas: 
![image](https://github.com/FelipeCh18/Lab5Robotica/assets/95656388/fed3ff52-42d9-4090-a5d8-c7925448deb3)


Cabe aclarar que la interfaz HMI se programó para la consola de linux.

**Resultados**
<p style = 'text-align:center;' align="center">
<img src="images/1717384619455.jpg" width="500px" >
</p>
<p style = 'text-align:center;' align="center">
<img src="images/1717384619483.jpg" width="500px" >
</p>
Los trazos que funcionan con el giro de una sola unión, se denotan muy claros y limpios, sin embargo, cuando son movimientos lentos y cortos, al robot le cuesta seguir una trayectoria limpia.
