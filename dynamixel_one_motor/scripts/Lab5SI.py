import rospy
import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

#creación del robot con roboticstoolbox
robot= rtb.DHRobot([
    rtb.RevoluteDH(d=0.045, alpha= -np.pi/2),
    rtb.RevoluteDH(a= 0.105),
    rtb.RevoluteDH(a=0.105),
    rtb.RevoluteDH(a=0.110)
], name= "Pincher")


#Cálculo de la cinamática inversa del robot
def cinemInversa(x,y,z):
    l0=0.04
    l1=0.110
    l2=0.110
    l3=0.09
    xaux=np.sqrt(x**2+y**2)-l2
    zaux=-0.06+z
    costheta3=(xaux**2+zaux**2-l1**2-l2**2)/(2*l1*l2)
    sentheta3=np.sqrt(1-costheta3**2)
    theta1=np.arctan2(y,x)
    theta2=(np.arctan2(zaux,xaux)+np.arctan2(l2*sentheta3, l1+l2*costheta3))
    theta3=np.arctan2(sentheta3, costheta3)
    theta4=(-theta2+theta3)
    angulos=[theta1, -(np.pi/2-theta2), -(theta3), (theta4), 0]

    return angulos

#Publicador de las posiciones
def enviarPosicion(puntos,flag):
    global posActual
    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
    rospy.init_node('joint_publisher', anonymous=False)
    print(" ")
    print(" ")
    for i in range(len(puntos)):
        puntoActual=puntos[i]
        x=puntoActual[0]
        y=puntoActual[1]
        z=puntoActual[2]
        print('Posición actual: x->',x*1000,'mm, y->',y*1000,'mm, z->',z*1000,'mm')
        state = JointTrajectory()
        state.header.stamp = rospy.Time.now()
        state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
        point = JointTrajectoryPoint()
        posActual=cinemInversa(x,y,z)
        if flag==True: posActual[4]=-2
        else: posActual[4]=0
        point.positions = posActual
        point.time_from_start = rospy.Duration(0.5)
        state.points.append(point)
        pub.publish(state)
        rospy.sleep(3)

#Publicador de los ángulos
def enviarAngulos(angulos):
    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
    rospy.init_node('joint_publisher', anonymous=False)
    state = JointTrajectory()
    state.header.stamp = rospy.Time.now()
    state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
    point = JointTrajectoryPoint()
    point.positions = angulos
    point.time_from_start = rospy.Duration(0.5)
    state.points.append(point)
    pub.publish(state)
    rospy.sleep(3)



def joint_publisher():
    
    posicionHome=[0, 0, -np.pi/2, 0, 0]
    enviarAngulos(posicionHome)
    puntos=[[0.020,-0.260,0.12],[0.020,-0.260,0.028]]
    enviarPosicion(puntos,False)
    puntos=[[0.020,-0.260,0.028],[0.020,-0.260,0.12]]
    enviarPosicion(puntos,True)
    posicionHome=[0, 0, -np.pi/2, 0, -2]
    enviarAngulos(posicionHome)
    print("")
    print("")
    print("Marcador en el porta herramientas")
    while not rospy.is_shutdown():
        print("")
        print("Seleccione la tarea a realizar, digitando el número: ")
        print("1. Dibujar espacio de trabajo max.")
        print("2. Dibujar espacio de trabajo min.")
        print("3. Dibujar las iniciales de los nombres.")
        print("4. Dibujar un circulo.")
        print("5. Dibujar una x sobre un triangulo.")
        print("6. Salir.")

        tarea=int(input())  
        #Casos de trabajo
        if tarea==1:
            img1BGR= cv2.imread('/home/felipech18/catkin_ws/src/dynamixel_one_motor/scripts/Imagenes/circmax.png')
            img1RGB=cv2.cvtColor(img1BGR, cv2.COLOR_BGR2RGB)
            plt.imshow(img1RGB)
            plt.show()
            start_time = time.time()
            puntos=[[0,-0.320,0.06],[0,-0.320,0.0],[0,0.320,0.0],[0,0.320,0.06]]
            enviarPosicion(puntos,True)
            print("\nRutina terminada, volviendo a home.")
            enviarAngulos(posicionHome)
            print(" ")
            end_time = time.time()
            Tiempo=end_time-start_time
            print("\nTiempo de ejecución: %.2f s" % Tiempo)
            print("")
        elif tarea==2:
            img1BGR= cv2.imread('/home/felipech18/catkin_ws/src/dynamixel_one_motor/scripts/Imagenes/circmin.png')
            img1RGB=cv2.cvtColor(img1BGR, cv2.COLOR_BGR2RGB)
            plt.imshow(img1RGB)
            plt.show()
            start_time = time.time()
            puntos=[[0,-0.200,0.06],[0,-0.190,0.0],[0,0.190,0.0],[0,0.190,0.06]]
            enviarPosicion(puntos,True)
            print("\nRutina terminada, volviendo a home.")
            enviarAngulos(posicionHome)
            end_time = time.time()
            Tiempo=end_time-start_time
            print("\nTiempo de ejecución: %.2f s" % Tiempo)
            print("")
        elif tarea==3:
            img1BGR= cv2.imread('/home/felipech18/catkin_ws/src/dynamixel_one_motor/scripts/Imagenes/FM.png')
            img1RGB=cv2.cvtColor(img1BGR, cv2.COLOR_BGR2RGB)
            plt.imshow(img1RGB)
            plt.show()
            start_time = time.time()
            puntos=[[0.118,-0.164,0.06],[0.118,-0.164,0.0],[0.067,-0.184,0.0],[0.100,-0.269,0.0],[0.100,-0.269,0.06],[0.082,-0.223,0.06],[0.082,-0.223,0.0],[0.118,-0.208,0.0],[0.118,-0.208,0.06],[0.163,-0.240,0.06],[0.163,-0.240,0.0],[0.130,-0.160,0.0],[0.176,-0.177,0.0],[0.200,-0.132,0.0],[0.234,-0.207,0.0],[0.234,-0.207,0.06]]
            enviarPosicion(puntos,True)
            print("\nRutina terminada, volviendo a home.")
            enviarAngulos(posicionHome)
            end_time = time.time()
            Tiempo=end_time-start_time
            print("\nTiempo de ejecución: %.2f s" % Tiempo)
            print("")
        elif tarea==4:
            img1BGR= cv2.imread('/home/felipech18/catkin_ws/src/dynamixel_one_motor/scripts/Imagenes/circulo.png')
            img1RGB=cv2.cvtColor(img1BGR, cv2.COLOR_BGR2RGB)
            plt.imshow(img1RGB)
            plt.show()
            start_time = time.time()
            angulo=0
            puntos=[]
            puntos.append([0.229+0.04*np.cos(np.deg2rad(24)),-0.0008+0.04*np.sin(np.deg2rad(24)),0.06])
            for o in range(0,17):
                angulo=angulo+24
                puntos.append([0.229+0.04*np.cos(np.deg2rad(angulo)),-0.0008+0.04*np.sin(np.deg2rad(angulo)),0.0])
            puntos.append([0.229+0.04*np.cos(np.deg2rad(o)),-0.0008+0.04*np.sin(np.deg2rad(o)),0.06])
            enviarPosicion(puntos,True)
            print("\nRutina terminada, volviendo a home.")
            enviarAngulos(posicionHome)
            end_time = time.time()
            Tiempo=end_time-start_time
            print("\nTiempo de ejecución: %.2f s" % Tiempo)
            print("")
        elif tarea==5:
            img1BGR= cv2.imread('/home/felipech18/catkin_ws/src/dynamixel_one_motor/scripts/Imagenes/trix.png')
            img1RGB=cv2.cvtColor(img1BGR, cv2.COLOR_BGR2RGB)
            plt.imshow(img1RGB)
            plt.show()
            start_time = time.time()
            puntos=[[0.115, 0.191, 0.06],[0.115, 0.191, 0.0],[0.204, 0.220, 0.0],[0.244, 0.109, 0.0],[0.115, 0.191, 0.0],[0.115, 0.191, 0.06],[0.154, 0.236, 0.06],[0.154, 0.236, 0.0],[0.212, 0.098, 0.0],[0.212, 0.098, 0.06],[0.262, 0.181, 0.06],[0.262, 0.181, 0.0],[0.111, 0.167, 0.0],[0.111, 0.167, 0.06]]
            enviarPosicion(puntos,True)
            print("\nRutina terminada, volviendo a home.")
            enviarAngulos(posicionHome)
            end_time = time.time()
            Tiempo=end_time-start_time
            print("\nTiempo de ejecución: %.2f s" % Tiempo)
            print("")
        else : 
            print("\nRegresando el marcador y saliendo del programa.")
            enviarAngulos(posicionHome)
            puntos=[[0.02,-0.25,0.12],[0.02,-0.25,0.025]]
            enviarPosicion(puntos,True)
            puntos=[[0.02,-0.25,0.025],[0.02,-0.25,0.12]]
            enviarPosicion(puntos,False)
            posicionHome=[0, 0, -np.pi/2, 0, -2]
            enviarAngulos(posicionHome)
            posicionHome=[0, 0, -np.pi/2, 0, 0]
            enviarAngulos(posicionHome)
            break




if __name__ == '__main__':
    try:
        time.sleep(1)
        joint_publisher()
    except rospy.ROSInterruptException:
        pass