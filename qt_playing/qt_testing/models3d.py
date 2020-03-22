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
    def __init__(self, robot_type):
        super(View3D, self).__init__()
        self.view = Qt3DWindow()
        self.container = self.createWindowContainer(self.view)
        self.setStyleSheet('background-color: white')
        self.robot_type = robot_type

        vboxlayout = QHBoxLayout()
        vboxlayout.addWidget(self.container)
        self.setLayout(vboxlayout)

        self.scene = self.createScene()

        # Camera.
        self.initialiseCamera(self.scene)

        self.view.setRootEntity(self.scene)

        t1 = threading.Thread(target=self.print_campos)
        t1.start()

    def print_campos(self):
        while True:
            print('camera position', self.camera.position())
            time.sleep(0.5)
        

    def initialiseCamera(self, scene):
        # Camera.
        self.camera = self.view.camera()
        self.camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        if self.robot_type == 'car':
            self.camera.setPosition(QVector3D(0.5, 2.0, 10.0))
        elif self.robot_type == 'drone':
            self.camera.setPosition(QVector3D(0.5, 0.3, 1.5))
        self.camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))

        # # For camera controls.
        # camController = QOrbitCameraController(scene)
        # camController.setLinearSpeed(500.0)
        # camController.setLookSpeed(500.0)
        # camController.setCamera(self.camera)

    def createScene(self):
        # Root entity
        rootEntity = QEntity()

        # Material
        material = QPhongMaterial(rootEntity)
        
        ent = QEntity(rootEntity)
        f1_mesh = QMesh()
        f1_mesh.setSource(QUrl('qrc:/assets/'+self.robot_type+'.obj'))

         # Qt3DCore.QTransform *
        sphereTransform = QTransform()
        #OrbitTransformController *
        controller = OrbitTransformController(sphereTransform)
        controller.setTarget(sphereTransform)
        controller.setRadius(0.0)
        # QPropertyAnimation *
        sphereRotateTransformAnimation = QPropertyAnimation(sphereTransform)
        sphereRotateTransformAnimation.setTargetObject(controller)
        sphereRotateTransformAnimation.setPropertyName(b"angle")
        sphereRotateTransformAnimation.setStartValue(0)
        sphereRotateTransformAnimation.setEndValue(360)
        sphereRotateTransformAnimation.setDuration(10000)
        sphereRotateTransformAnimation.setLoopCount(-1)
        sphereRotateTransformAnimation.start()
    
        ent.addComponent(f1_mesh)
        ent.addComponent(sphereTransform)
        ent.addComponent(material)

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


class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        #
        view3d = View3D()
        self.setCentralWidget(view3d)
        self.show()

# Approach 1 - Integrate Qt3DWindow into a QMainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())