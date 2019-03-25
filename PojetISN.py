"""
@author: ykhima
"""
#A faire :

#-peut être une QDockWindow pour demander la taille de la fenêtre et le coefElement avant de lancer main() 
#vue que l'interface est en fonction de L et H

#un pushbutton pour mettre du texte pour les unitee et les valeurs

#utiliser un QDockWidget pour le texte de "besoin d'aide"

#un mode QCM ?

#un mode Leçon avec des animations ?

#creer peut être a la fin un mode save-load

#Faire une demande pour les XButton et quelle fonction ca va lancer

#Exo que des portes and et or

import sys, math
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QLine, QRect, QPoint


def main() :

#Taille de la fenètre MODIFIABLE dans le programme
#-et modifiable un jour par l'utilisateur 
#-toute taille disponible tant que c'est supperieur 250 et pair
    L  = 700
    H = 800
    
#Boolean du boutton de la souris pour la position des elements.
    clickCanvas = False
    
#l'utilisateur doit clicker une prmière fois pour appeler un element puis un second click pour le placer sur le canevas
    initClick = False

    rightClickCanvas = False
    
    isControlPressed = False
#initialisation des positions
    cursorPos = QPoint()
    clickPos = QPoint()
    startLinePos = QPoint()
    
#Taille des elements MODIFIABLE dans le programme
#-et modifiable un jour par l'utilisateur 
#-coefElement >= 2 et coefElement pair et c'est lisible quand c'est >=6
    coefElement = 10
    
#element choisit par l'utilisateur
    userElement = 0
    userRotation = math.pi*2
    
    intWindowMode = 0
    
    lineMode = False
    linearMode = True
    cadriageMode = False
    cursorLockMode = True
    
#taille du canevas en fonction de la taille de l'ecran non modifiable par l'utilisateur 
#-valeur pour intWindowMode = 0 servira pour afficher une image
    canvas = QRect(10, 10, L-20, (H*7/9)-20)
    
#Canvas Example est le canvas qui permet de changer d'element (theoriquement)    
    canvasExample = QRect((L/2)-(L/14), (H*8/9)-(H/14), L/7, H/7) 
  
#initialisation des Button du Home Menu et du mode de creation avec un tableau

    homeButton = []
    #init homeButton
    for n in range(4):
        homeButton.append(n)
    
    editorButton = []
    for n in range(7):
        editorButton.append(n)

    elementOnCanvas = [0]
    elementOnCanvasPos = [0]
    elementOnCanvasRotation = [0]
    
    lineOnCanvas = [0]
#-----------------------------------------------------------     
#-----------------------------------------------------------     
#class des differents evenement de mainWindow
    class windowEvent(QtWidgets.QMainWindow):
#-----------------------------------------------------------
         def __init__(self):
            super().__init__()
            self.setMouseTracking(True)
            self.setFocusPolicy(Qt.StrongFocus)
#-----------------------------------------------------------
         def mouseMoveEvent(self, event):
            nonlocal cursorPos, cursorLockMode, canvas
            
            cursorPos = event.pos()
            
            if cursorLockMode and canvas.contains(cursorPos):
                cursorPos = QPoint(round(cursorPos.x(), -1), round(cursorPos.y(), -1))
           
            self.update()
#-----------------------------------------------------------            
         def keyPressEvent(self, event):
            nonlocal isControlPressed
    
            if event.key() == Qt.Key_Control : 
                isControlPressed = True
            
            if event.key() == Qt.Key_Z and isControlPressed:
                deleteLastElement()
            

            self.update()
            
         def keyReleaseEvent(self, event):
            nonlocal isControlPressed
            
            if event.key() == Qt.Key_Control:
                isControlPressed = False
#-----------------------------------------------------------
         def mousePressEvent(self, event):
            nonlocal clickCanvas, initClick, cursorPos, clickPos, intWindowMode
            nonlocal startLinePos, lineMode, rightClickCanvas

            
            if event.button() == Qt.RightButton and canvas.contains(cursorPos) and not intWindowMode == 0:
                rightClickCanvas = True
                clickCanvas = False
                
                if not lineMode:
                    initClick = True
            
            if event.button() == Qt.XButton2 and not intWindowMode == 0:
                deleteLastElement()
                
            if event.button() == Qt.XButton1 and not intWindowMode == 0:
                addRotation()
            
            if initClick:
                clickPos = cursorPos
                if lineMode:    
                    startLinePos = clickPos
            
            if not intWindowMode == 0 and canvasExample.contains(cursorPos) and not lineMode:
                changeElement(event)
                
            elif not intWindowMode == 0 and canvas.contains(cursorPos) and not canvasExample.contains(clickPos):
                
               if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
                   clickCanvas = True
                   initClick = not initClick
                   
            elif not intWindowMode == 0 and (not canvas.contains(cursorPos) or canvasExample.contains(cursorPos)):
                print("vous n'êtes pas dans la zone de travail")
                
                if lineMode:
                    rightClickCanvas = True
                else:
                    clickCanvas = False
                    initClick = False                
            
            self.update()
#-----------------------------------------------------------
         def paintEvent(self, event):
            nonlocal clickCanvas, initClick, clickPos, cursorPos, startLinePos, userRotation, rightClickCanvas
            nonlocal canvas, dictElementElec, canvasExample, lineMode, linearMode, cadriageMode
            nonlocal elementOnCanvas, elementOnCanvasPos, elementOnCanvasRotation, lineOnCanvas
            
            #initialisation du QPainter
            painter = QPainter(self)
            brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
            pen = QtGui.QPen(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)
            
            #dessin des canvas
            if not intWindowMode == 0 :
                painter.setBrush(brush)
                painter.drawRect(canvas)
                painter.drawRect(canvasExample)    
                painter.setBrush(Qt.NoBrush)
                #dessin du canvas Example
                temp = clickPos
                
                clickPos = canvasExample.center()
                
                if intWindowMode == 1:
                    dictElementElec[userElement](painter)
                elif intWindowMode == 2:
                    dictElementLogic[userElement](painter)
                    
                clickPos = temp
                
            painter.setClipRect(canvas)
            
            if cadriageMode:
                
               pen.setWidth(1) 
               painter.setPen(pen)
               
               for n in range(int(L/20)):
                   painter.drawLine((L*n)/(L/20), 0, (L*n)/(L/20), H)
                   
               for n in range(int(H/20)):
                   painter.drawLine(0, (H*n)/(H/20), L, (H*n)/(H/20))
                 
               pen.setWidth(2) 
               painter.setPen(pen) 
               
            if initClick:
                clickPos = cursorPos

            if clickCanvas and not intWindowMode == 0 and canvas.contains(clickPos) and not canvasExample.contains(cursorPos) and not lineMode :
                
                if intWindowMode == 1:
                    dictElementElec[userElement](painter)
                elif intWindowMode == 2:
                    dictElementLogic[userElement](painter)
                
                if not initClick and not rightClickCanvas:
                    
                    if elementOnCanvasPos[0] == 0:
                        elementOnCanvas[0] = userElement
                        elementOnCanvasPos[0] = clickPos
                        elementOnCanvasRotation[0] = userRotation
                        clickCanvas = False
                    
                    else :
                        
                        elementOnCanvas.append(len(elementOnCanvas))
                        elementOnCanvas[len(elementOnCanvas)-1] = userElement
                                        
                        elementOnCanvasPos.append(len(elementOnCanvasPos))
                        elementOnCanvasPos[len(elementOnCanvasPos)-1] = clickPos
                                  
                        elementOnCanvasRotation.append(len(elementOnCanvasRotation))
                        elementOnCanvasRotation[len(elementOnCanvasRotation)-1] = userRotation
                                                
                        clickCanvas = False
                        
                elif rightClickCanvas:
                    clickCanvas = False
                    rightClickCanvas = False
                    
            if not elementOnCanvasPos[0] == 0  :
                
                for n in range(len(elementOnCanvas)):
                    temp = userRotation
                    temp2 = clickPos
                    
                    
                    clickPos = elementOnCanvasPos[n]
                    userRotation = elementOnCanvasRotation[n]
                    if intWindowMode == 1:
                        dictElementElec[elementOnCanvas[n]](painter)
                    elif intWindowMode == 2:
                        dictElementLogic[elementOnCanvas[n]](painter)
                    
                    userRotation= temp
                    clickPos = temp2
                
            if not lineOnCanvas[0] == 0:
                for n in range(len(lineOnCanvas)):
                    painter.drawLine(lineOnCanvas[n])
            
            
            if lineMode and clickCanvas and canvas.contains(clickPos) and not intWindowMode == 0 :
                
                if linearMode:
                    
                    temp = cursorPos-startLinePos
                    temp1 = temp.x()
                    temp2 = temp.y()
                
                    if abs(temp1) <= abs(temp2):
                        cursorPos.setX(startLinePos.x())

                    elif abs(temp2) <= abs(temp1) :
                        cursorPos.setY(startLinePos.y())
                    
                painter.drawLine(startLinePos.x(), startLinePos.y(), cursorPos.x(), cursorPos.y())
                
                if initClick and not rightClickCanvas:
                    
                    if lineOnCanvas[0] == 0:
                        lineOnCanvas[0] = QLine(startLinePos.x(), startLinePos.y(), cursorPos.x(), cursorPos.y())
                        clickCanvas = True
                        initClick = False
                        startLinePos = cursorPos

                    else :
                        lineOnCanvas.append(len(lineOnCanvas))
                        lineOnCanvas[len(lineOnCanvas)-1] = QLine(startLinePos.x(), startLinePos.y(), cursorPos.x(), cursorPos.y())
                        clickCanvas = True
                        initClick = False
                        startLinePos = cursorPos

                elif rightClickCanvas:
                    clickCanvas = False
                    initClick = True
                    rightClickCanvas = False
                    startLinePos = cursorPos
                    
            self.update()
        
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
    def deleteLastElement():
        nonlocal  lineMode, lineOnCanvas, elementOnCanvasRotation, elementOnCanvasPos, elementOnCanvas
        
        if lineMode:
            del lineOnCanvas[len(lineOnCanvas)-1]
                     
            if len(lineOnCanvas) == 0:
                
                lineOnCanvas.append(len(lineOnCanvas))
                lineOnCanvas[0] = 0
        else:
            del elementOnCanvasRotation[len(elementOnCanvasRotation)-1]
            del elementOnCanvasPos[len(elementOnCanvasPos)-1]
            del elementOnCanvas[len(elementOnCanvas)-1]
                     
            if len(elementOnCanvas) == 0:
                elementOnCanvas.append(0)
                elementOnCanvas[0] = 0

                elementOnCanvasPos.append(0)
                elementOnCanvasPos[0] = 0
                
                elementOnCanvasRotation.append(0)
                elementOnCanvasRotation[0] = 0
#-----------------------------------------------------------                
    def changeElement(event):
        nonlocal userElement, dictElementElec, dictElementLogic,  intWindowMode
        
        if event.button() == Qt.LeftButton:
            userElement = userElement + 1
            
            if userElement == len(dictElementElec) and intWindowMode == 1 or userElement == len(dictElementLogic) and intWindowMode == 2:
                userElement = 0
                        
        elif event.button() == Qt.RightButton:
            if userElement == 0 and intWindowMode == 1:
                userElement = len(dictElementElec) -1
                
            elif userElement == 0 and intWindowMode == 2:
                userElement = len(dictElementLogic) -1
                
            else: 
                userElement = userElement -1  
                
        elif event.button() == Qt.MidButton:
            userElement = 0
         
#-----------------------------------------------------------
#-----------------------------------------------------------   
#Les class des elements a pour but de dessiner les elements en fonction d'un repère
    class elementElec(QPainter):        
#-----------------------------------------------------------     
        def resistance(self):
            #base
            self.drawLine(createLine(-1, -2, 1, -2))
            self.drawLine(createLine(1, -2, 1, 2))
            self.drawLine(createLine(1, 2, -1, 2))
            self.drawLine(createLine(-1, 2, -1, -2))
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
#-----------------------------------------------------------
        def generator(self):
            #base
            self.drawEllipse(createEllipse(0, 0, 4, 4))
            #cables
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
            #"+"
            self.drawLine(createLine(-2, -3, -2, -2))
            self.drawLine(createLine(-2.5, -2.5, -1.5, -2.5))
            #"-"
            self.drawLine(createLine(-2.5, 2.5, -1.5, 2.5))
#-----------------------------------------------------------
        def ground(self):
            #base
            self.drawLine(createLine(-2, -0.5, 2, -0.5))
            self.drawLine(createLine(-1.5, 0, 1.5, 0))
            self.drawLine(createLine(-1, 0.5, 1, 0.5))
            #cable
            self.drawLine(createLine(0, -0.5, 0, -2))
#----------------------------------------------------------
        def diode(self):
            #triangle
            self.drawLine(createLine(-2, 2, 2, 2))
            self.drawLine(createLine(2, 2, 0,-2))
            self.drawLine(createLine(0, -2, -2, 2))
            #trait de la katode
            self.drawLine(createLine(-2, -2, 2, -2))
            #cables
            self.drawLine(createLine(0, -4, 0, 4))
            
        def diodeZener(self):
            elementElec.diode(self)
            self.drawLine(createLine(2, -2, 2, -1.5))
#-----------------------------------------------------------
        def transistor(self):
            #base
            self.drawLine(createLine(-2, -2, -2, 2))
            self.drawLine(createLine(-2, -1, 0, -2))
            self.drawLine(createLine(-2, 1, 0, 2))
            #cable
            self.drawLine(createLine(-2, 0, -4, 0))
            self.drawLine(createLine(0, -2, 0, -4))
            self.drawLine(createLine(0, 2, 0, 4))
#-----------------------------------------------------------
        def coil(self):
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
            #base 
            for n in range(0,4):
                self.drawArc(createEllipse(0, -1.5 + n, 1, 1), createHalfAngle(math.pi*3/2), createHalfAngle(0))
#-----------------------------------------------------------
        def capacitor(self):
            #base
            self.drawLine(createLine(-1.5, -0.5, 1.5, -0.5))
            self.drawLine(createLine(-1.5, 0.5, 1.5, 0.5))
            #cable
            self.drawLine(createLine(0, -0.5, 0, -2.5))
            self.drawLine(createLine(0, 0.5, 0, 2.5))
#-----------------------------------------------------------
        def AOP(self):
            #triangle
            self.drawLine(createLine(-3, 3, 3, 3))
            self.drawLine(createLine(3, 3, 0,-3))
            self.drawLine(createLine(0, -3, -3, 3))
            #"+"
            self.drawLine(createLine(-2, 3, -2, 4))
            self.drawLine(createLine(-2.5, 3.5, -1.5, 3.5))
            #"-"
            self.drawLine(createLine(1.5, 3.5, 2.5, 3.5))
            #cable
            self.drawLine(createLine(0, -3, 0, -5))
            self.drawLine(createLine(-1, 3, -1, 5))
            self.drawLine(createLine(1, 3, 1, 5))
#-----------------------------------------------------------             
        def arrowVoltage(self):
            self.drawLine(createLine(0, -3, 0, 3))
            self.drawLine(createLine(-0.5, -2.5, 0, -3))
            self.drawLine(createLine(0, -3, 0.5, -2.5))
#-----------------------------------------------------------             
        def arrowCurrent(self):
            self.drawLine(createLine(-0.5, 0, 0, -1))
            self.drawLine(createLine(0, -1, 0.5, 0))
#----------------------------------------------------------     
#----------------------------------------------------------     
#"dicitonaire" faisant l'office d'un "Switch Case" et regroupe toutes les fonctions de la class element dans un tableau, il ne reste plus qu'a faire dictElementElec[int](painter)
    dictElementElec = {
           0 : elementElec.resistance,
           1 : elementElec.generator,
           2 : elementElec.ground,
           3 : elementElec.diode,
           4 : elementElec.diodeZener,
           5 : elementElec.transistor,
           6 : elementElec.coil,
           7 : elementElec.capacitor,
           8 : elementElec.AOP,
           9 : elementElec.arrowVoltage,
           10 : elementElec.arrowCurrent, }
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------     
    class elementLogic(QPainter):  
#-----------------------------------------------------------         
        def bufferGate(self):
            #triangle
            self.drawLine(createLine(-2, 2, 2, 2))
            self.drawLine(createLine(2, 2, 0,-2))
            self.drawLine(createLine(0, -2, -2, 2))
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
#-----------------------------------------------------------             
        def notGate(self):
            elementLogic.bufferGate(self)
            self.drawEllipse(createEllipse(0, -2, 1, 1))
#-----------------------------------------------------------             
        def orGate(self):
            #cable
            self.drawLine(createLine(0, -2, 0, -4))
            self.drawLine(createLine(-1, 1.5, -1, 4))
            self.drawLine(createLine(1, 1.5, 1, 4))
            #base
            self.drawArc(createEllipse(0, 2, 4, 8), createHalfAngle(math.pi*2), createHalfAngle(0))
            self.drawArc(createEllipse(0, 2.5, 4, 2), createHalfAngle(math.pi*2), createHalfAngle(0))
#-----------------------------------------------------------             
        def norGate(self):
            elementLogic.orGate(self)
            self.drawEllipse(createEllipse(0, -2.5, 1, 1))
#-----------------------------------------------------------         
        def xorGate(self):
            elementLogic.orGate(self)
            self.drawArc(createEllipse(0, 3, 4, 1), createHalfAngle(math.pi*22), createHalfAngle(0))
#-----------------------------------------------------------             
        def nxorGate(self):
            elementLogic.norGate(self)
            elementLogic.xorGate(self)
#-----------------------------------------------------------                         
        def andGate(self):
            #cable
            self.drawLine(createLine(-1, 2, -1, 4))
            self.drawLine(createLine(1, 2, 1, 4))
            self.drawLine(createLine(0, -1, 0, -4))
            #base
            self.drawArc(createEllipse(0, 0, 4, 2), createHalfAngle(math.pi*2), createHalfAngle(0))
            self.drawLine(createLine(-2, 0, -2, 2))
            self.drawLine(createLine(-2, 2, 2, 2))
            self.drawLine(createLine(2, 2, 2, 0))
#-----------------------------------------------------------             
        def nandGate(self):
            elementLogic.andGate(self)
            self.drawEllipse(createEllipse(0, -1.5, 1, 1))
            
        def bridge(self):
            self.drawArc(createEllipse(0, 0, 1, 1), createHalfAngle(math.pi*2), createHalfAngle(0))

#-----------------------------------------------------------     
#-----------------------------------------------------------
#-----------------------------------------------------------   
    dictElementLogic = {
           0 : elementLogic.bufferGate,
           1 : elementLogic.notGate,
           2 : elementLogic.andGate,
           3 : elementLogic.nandGate,
           4 : elementLogic.orGate,
           5 : elementLogic.norGate,
           6 : elementLogic.xorGate,
           7 : elementLogic.nxorGate,
           8 : elementLogic.bridge,
           }
    
#Les fonctions suivantes ont pour but de creer les elements en fonction du coef et de la souris (repère : clickPos, coefElement* x->, coefElement* y->)
    def createPointX(X):
        nonlocal clickPos, coefElement
        return clickPos.x()+X*coefElement
  
    def createPointY(Y):
        nonlocal clickPos, coefElement
        return clickPos.y()+Y*coefElement
  
    def createLine(x1, y1, x2, y2):
        nonlocal clickPos, coefElement, userRotation
        
        cosPhi = round(math.cos(userRotation))
        sinPhi = round(math.sin(userRotation))
        
        newX1 = clickPos.x() + x1*cosPhi*coefElement - y1*sinPhi*coefElement
        newY1 = clickPos.y() + x1*sinPhi*coefElement + y1*cosPhi*coefElement
        
        newX2 = clickPos.x() + x2*cosPhi*coefElement - y2*sinPhi*coefElement
        newY2 = clickPos.y() + x2*sinPhi*coefElement + y2*cosPhi*coefElement
        
        return QLine(newX1, newY1, newX2, newY2)
    
    def createHalfAngle(startAngle):
        nonlocal userRotation
        if startAngle == 0:
            return math.degrees(math.pi)*16
        else :
            return math.degrees(startAngle-userRotation)*16
        
    def createEllipse(x, y, largeur, hauteur):
        nonlocal clickPos, coefElement, userRotation
        
        cosPhi = round(math.cos(userRotation))
        sinPhi = round(math.sin(userRotation))

        
        newX1 = clickPos.x() + (x-largeur/2)*cosPhi*coefElement - (y-hauteur/2)*sinPhi*coefElement
        newY1 = clickPos.y() + (x-largeur/2)*sinPhi*coefElement + (y-hauteur/2)*cosPhi*coefElement

        newX2 = largeur*cosPhi*coefElement - hauteur*sinPhi*coefElement
        newY2 = largeur*sinPhi*coefElement + hauteur*cosPhi*coefElement

        return QRect(newX1, newY1, newX2, newY2)
#-----------------------------------------------------------           
    def createButton(posX, posY, sizeX, sizeY, texte, widget, callBack) :
        
        button = QtWidgets.QPushButton(texte, widget)
        button.move(posX, posY)
        button.resize(sizeX, sizeY)
        button.clicked.connect(callBack)
        return button
    
#Differents callBacks
    def elecMode():
        windowMode(1)

    def logicMode():
        windowMode(2)
        
    def closeProg():
        mainWindow.close()
        
    def clearAll():
        nonlocal elementOnCanvas, elementOnCanvasPos, elementOnCanvasRotation
        nonlocal userRotation, cursorPos, clickPos, lineOnCanvas, lineMode, initClick
        nonlocal startLinePos, clickCanvas, rightClickCanvas
        
        userRotation = math.pi*2
        
        elementOnCanvas = [0]
        elementOnCanvasPos = [0]
        elementOnCanvasRotation = [0]
        
        cursorPos = QPoint()
        clickPos = QPoint()
        startLinePos = QPoint()
        
        lineOnCanvas = [0]
        
        rightClickCanvas = False
        clickCanvas = False
        
        if lineMode:
            initClick = True
            
        else:
            initClick = False
        
    def returnHomeMenu():
        nonlocal userElement, lineMode
        nonlocal linearMode, cadriageMode, cursorLockMode
        userElement = 0
        
        lineMode = False
        cadriageMode = False
        linearMode = True
        cursorLockMode = True
        
        clearAll()
        windowMode(0)
        
    def addRotation():
        nonlocal userRotation
        userRotation = userRotation + math.pi/2
        if userRotation == math.pi*4:
            userRotation = 2*math.pi
        
    def changeLineMode():
        nonlocal lineMode, initClick, editorButton, clickCanvas

        clickCanvas = False
        if editorButton[0].isChecked():
            lineMode = True
            initClick = True
            
        else :
            lineMode = False
            initClick = False
            
    def changeLinearMode():
        nonlocal linearMode, editorButton
       
        if editorButton[1].isChecked() :
            linearMode = False            
        else :
            linearMode = True
            
    def changeCadriageMode():
        nonlocal editorButton, cadriageMode
       
        if editorButton[4].isChecked() :
            cadriageMode = True            
        else :
            cadriageMode = False
            
            
    def changeCursorLock():
        nonlocal cursorLockMode, editorButton
       
        if editorButton[6].isChecked() :
            cursorLockMode = False            
        else :
            cursorLockMode = True
            
                 
    def null():
        print("null")
        
#cette fonction a pour but de regler les bouttons des deux modes (home et creation)
    def windowMode(state):
        nonlocal H, L, mainWindow, canvas, homeButton, editorButton, intWindowMode, logoHomeMenu
        intWindowMode = state 
        
        if state == 0 :
            mainWindow.close()
            logoHomeMenu.show()
            
            for n in range(len(homeButton)):
                homeButton[n].show()
            for n in range(len(editorButton)):
                editorButton[n].close()
                
        else :
            mainWindow.close()
            logoHomeMenu.close()
            
            for n in range(len(editorButton)):
                editorButton[n].show()
            
            for n in range(len(homeButton)) :
                homeButton[n].close()
                
        mainWindow.show()
    
    def initButtons():
        nonlocal L, H, homeButton, editorButton, mainWindow
        
        homeButton[0] = createButton(10, (H*3/6), L-20, (H/6)-10, "Creation de schemas electriques", mainWindow, elecMode)
        homeButton[1] = createButton(10, (H*4/6), L-20, (H/6)-10, "Creation de schemas logiques", mainWindow, logicMode)
        homeButton[2] = createButton(10, (H*5/6), (L/2)-20, (H/6)-10, "Besoin d'aide ?", mainWindow, null)
        homeButton[3] = createButton((L/2)+10, (H*5/6), (L/2)-20, (H/6)-10, "Fermer l'application", mainWindow, closeProg)
        
        editorButton[0] = createButton(10, (H*7/9), (L/4)-20, (H/8)-20, "Cable", mainWindow, changeLineMode)
        editorButton[0].setCheckable(True)
            
        editorButton[1] = createButton((L*3/12), (H*7/9), (L/8)-20, (H/8)-20, "All angle", mainWindow, changeLinearMode)
        editorButton[1].setCheckable(True)
            
        editorButton[2] = createButton(10, (H*8/9), (L/4)-20, (H/8)-20, "Tout suppimer", mainWindow, clearAll)
            
        editorButton[3] = createButton((L*3/4)+10, (H*8/9), (L/4)-20, (H/8)-20, "Retour", mainWindow, returnHomeMenu)
            
        editorButton[4] = createButton((L*8/12)-10, (H*7/9), (L/8)-20, (H/8)-20, "cadriage", mainWindow,  changeCadriageMode) 
        editorButton[4].setCheckable(True)
            
        editorButton[5] = createButton((L*3/4)+10, (H*7/9), (L/4)-20, (H/8)-20, "Rotation", mainWindow, addRotation)
 
        editorButton[6] = createButton((L*8/12)-10, (H*8/9), (L/8)-20, (H/8)-20, "All Position", mainWindow, changeCursorLock)
        editorButton[6].setCheckable(True)
        
#Initialisation du mainWindow et le place theoriquement en fonciton de de la resolution de l'ecran 

    app = QtWidgets.QApplication(sys.argv)    

    mainWindow = QtWidgets.QMainWindow()
    
    resolution = QtWidgets.QApplication.desktop().screenGeometry()
    mainWindow.move((resolution.width()/2)-(L/2), (resolution.height()/2)-(H/2))
    
    mainWindow.setFixedSize(L, H)
    
    mainWindow.setWindowIcon(QtGui.QIcon("images/icon.png"))
    
    logoHomeMenu = QtWidgets.QLabel(mainWindow)
    logoHomeMenu.setPixmap(QtGui.QPixmap("images/imageHomeMenu.png"))
    logoHomeMenu.move(10, 10)
    logoHomeMenu.setScaledContents(True)
    logoHomeMenu.resize(L-20, (H/2)-20)
    mainWindow.setWindowTitle("G.E Schematronique")
    
    mainWindow.setCentralWidget(windowEvent())
    
    initButtons()
    windowMode(0)
#-----------------------------------------------------------   
    mainWindow.show()
    sys.exit(app.exec_())
#-----------------------------------------------------------   

main() 
