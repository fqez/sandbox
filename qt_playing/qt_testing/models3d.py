from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.Qt3DCore import *
from PyQt5.Qt3DRender import *
from PyQt5.Qt3DInput import *
from PyQt5.Qt3DExtras import *
import resources
import sys, time
import threading


def fuzzyCompareDouble(p1, p2):
    """
    compares 2 double as points
    """
    return abs(p1 - p2) * 100000. <= min(abs(p1), abs(p2))

class OrbitTransformController(QTransform):
    targetChanged = pyqtSignal()
    angleChanged = pyqtSignal()
    radiusChanged = pyqtSignal()

    def __init__(self, parent):
        QTransform.__init__(self, parent)
        self.m_target = QTransform()
        self.m_matrix = QMatrix4x4()
        self.m_radius = 1.0
        self.m_angle = 0.0

    def target(self):
        return self.m_target

    def setTarget(self, target):
        if self.m_target == target:
            return
        self.m_target = target
        self.targetChanged.emit()

    def setRadius(self, radius):
        if fuzzyCompareDouble(radius, self.m_radius):
            return
        self.m_radius = radius
        self.radiusChanged.emit()

    def radius(self, ): #  : # method of "", returning float OrbitTransformController (const)
        return self.m_radius

    def setAngle(self, angle): #  : # method of "", returning void OrbitTransformController ()
        if fuzzyCompareDouble(angle, self.m_angle):
            return
        self.m_angle = angle
        self.updateMatrix()
        self.angleChanged.emit()

    def angle(self): #  : # method of "", returning float OrbitTransformController (const)
        return self.m_angle

    def updateMatrix(self, ): #  : # method of "", returning void OrbitTransformController ()
        self.m_matrix.setToIdentity()
        self.m_matrix.rotate(self.m_angle, QVector3D(0.0, 1.0, 0.0))
        self.m_matrix.translate(self.m_radius, 0.0, 0.0)
        self.m_target.setMatrix(self.m_matrix)

    angle = pyqtProperty(float, fget=angle, fset=setAngle, notify=angleChanged)
    radius = pyqtProperty(float, fget=radius, fset=setRadius, notify=radiusChanged)
    target = pyqtProperty(QTransform, fget=target, fset=setTarget, notify=angleChanged)


class View3D(QWidget):
    def __init__(self, robot_type, parent = None):
        super(View3D, self).__init__(parent)
        self.view = Qt3DWindow()
        self.parent = parent
        self.view.defaultFrameGraph().setClearColor(QColor(51,51,51))
        self.container = self.createWindowContainer(self.view)
        self.setStyleSheet('background-color: white')
        self.robot_type = robot_type
        self.robot_entity = None
        self.setMouseTracking(True)

        vboxlayout = QHBoxLayout()
        vboxlayout.addWidget(self.container)
        self.setLayout(vboxlayout)

        self.scene = self.createScene()

        # Camera.
        self.initialiseCamera(self.scene)

        self.view.setRootEntity(self.scene)

    #     t1 = threading.Thread(target=self.print_campos)
    #     t1.start()

    # def print_campos(self):
    #     while True:
    #         print(self.robot_type, self.camera.position())
    #         time.sleep(0.5)


    def initialiseCamera(self, scene):
        # Camera.
        self.camera = self.view.camera()
        self.camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        if self.robot_type == 'car':
            self.camera.setPosition(QVector3D(0.3, 1.5, 4.0))
        elif self.robot_type == 'f1':
            self.camera.setPosition(QVector3D(0.3, 1.7, 4.5))
        elif self.robot_type == 'drone' or self.robot_type == 'drone_l':
            self.camera.setPosition(QVector3D(0.2, 0.1, 0.5))
        elif self.robot_type == 'roomba':
            self.camera.setPosition(QVector3D(0.0, 0.2, 0.6))
        elif self.robot_type == 'turtlebot':
            self.camera.setPosition(QVector3D(0.0, 0.4, 0.8))
        elif self.robot_type == 'pepper':
            self.camera.setPosition(QVector3D(0.17, 1.3, 1.6))
        
        if self.robot_type == 'pepper':
            self.camera.setViewCenter(QVector3D(0.0, 0.6, 0.0))
        elif self.robot_type == 'turtlebot':
            self.camera.setViewCenter(QVector3D(0.0, 0.1, 0.0))
        else:
            self.camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))


        # # For camera controls.
        # camController = QOrbitCameraController(scene)
        # camController.setLinearSpeed(250.0)
        # camController.setLookSpeed(250.0)
        # camController.setCamera(self.camera)

    def change_window(self):
        self.parent.emit_and_destroy()
    
    def start_animation(self):
        self.stop_animation()
        self.sphereRotateTransformAnimation.start()

    def start_animation_with_duration(self, duration):
        self.stop_animation()
        self.sphereRotateTransformAnimation.setDuration(duration)
        self.sphereRotateTransformAnimation.setLoopCount(1)
        self.start_animation()
        self.sphereRotateTransformAnimation.finished.connect(self.change_window)


    def stop_animation(self):
        self.sphereRotateTransformAnimation.stop()

    def set_animation_speed(self, speed):
        """ speed of a 360deg rotation in seconds """
        self.sphereRotateTransformAnimation.setDuration(speed)

    def createScene(self):
        # Root entity
        rootEntity = QEntity()

        light_entity = QEntity(rootEntity)
        light = QPointLight(light_entity)
        light.setColor(QColor(255,255,255))
        light.setIntensity(0.6)
        trans = QTransform()
        trans.setTranslation(QVector3D(0,0,2))
        
        light_entity.addComponent(trans)
        light_entity.addComponent(light)

        # Material
        # material = QTextureMaterial(rootEntity)
        # material.setTexture(QTextureImage().setSource(QUrl('qrc:/assets/blue.jpg')))
        material = QPhongMaterial(rootEntity)
        material.setAmbient(QColor(100,100,100))
        # material.setShininess(0)
        
        self.robot_entity  = QEntity(rootEntity)
        f1_mesh = QMesh()
        f1_mesh.setSource(QUrl('qrc:/assets/'+self.robot_type+'.obj'))

       
    
        self.robot_entity .addComponent(f1_mesh)
        
        self.robot_entity .addComponent(material)

        # Qt3DCore.QTransform *
        sphereTransform = QTransform()
        #OrbitTransformController *
        controller = OrbitTransformController(sphereTransform)
        controller.setTarget(sphereTransform)
        controller.setRadius(0.0)
        # QPropertyAnimation *
        self.sphereRotateTransformAnimation = QPropertyAnimation(sphereTransform)
        self.sphereRotateTransformAnimation.setTargetObject(controller)
        self.sphereRotateTransformAnimation.setPropertyName(b"angle")
        self.sphereRotateTransformAnimation.setStartValue(0)
        self.sphereRotateTransformAnimation.setEndValue(360)
        self.sphereRotateTransformAnimation.setDuration(10000)
        self.sphereRotateTransformAnimation.setLoopCount(-1)
        self.robot_entity.addComponent(sphereTransform)
        self.start_animation()

        # # Torus
        # torusEntity = QEntity(rootEntity)
        # # Qt3DExtras.QTorusMesh *
        # torusMesh = QTorusMesh()
        # torusMesh.setRadius(5)
        # torusMesh.setMinorRadius(1)
        # torusMesh.setRings(100)
        # torusMesh.setSlices(20)

        # #Qt3DCore.QTransform *
        # torusTransform = QTransform()
        # torusTransform.setScale3D(QVector3D(1.5, 1, 0.5))
        # torusTransform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(1, 0, 0), 45.0))

        # torusEntity.addComponent(torusMesh)
        # torusEntity.addComponent(torusTransform)
        # torusEntity.addComponent(material)

        # # Sphere
        # sphereEntity = QEntity(rootEntity)
        # sphereMesh = QSphereMesh()
        # sphereMesh.setRadius(3)

        # # Qt3DCore.QTransform *
        # sphereTransform = QTransform()
        # #OrbitTransformController *
        # controller = OrbitTransformController(sphereTransform)
        # controller.setTarget(sphereTransform)
        # controller.setRadius(20.0)
        # # QPropertyAnimation *
        # sphereRotateTransformAnimation = QPropertyAnimation(sphereTransform)
        # sphereRotateTransformAnimation.setTargetObject(controller)
        # sphereRotateTransformAnimation.setPropertyName(b"angle")
        # sphereRotateTransformAnimation.setStartValue(0)
        # sphereRotateTransformAnimation.setEndValue(360)
        # sphereRotateTransformAnimation.setDuration(10000)
        # sphereRotateTransformAnimation.setLoopCount(-1)
        # sphereRotateTransformAnimation.start()

        # sphereEntity.addComponent(sphereMesh)
        # sphereEntity.addComponent(sphereTransform)
        # sphereEntity.addComponent(material)

        return rootEntity

def delete_widgets_from(layout):
    """ memory secure. """
    for i in reversed(range(layout.count())): 
        widgetToRemove = layout.itemAt(i).widget()
        # remove it from the layout list
        layout.removeWidget(widgetToRemove)
        # remove it from the gui
        widgetToRemove.setParent(None)

# class Application(QMainWindow):
#     def __init__(self):
#         super(Application, self).__init__()
#         #
#         view3d = View3D()
#         self.setCentralWidget(view3d)
#         self.show()

# # Approach 1 - Integrate Qt3DWindow into a QMainWindow
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Application()
#     sys.exit(app.exec_())