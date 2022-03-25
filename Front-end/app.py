import cv2


from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2


# On accède à la webcam
cam = cv2.VideoCapture(0)



# Paramètres pour définir la fenêtre
nom_fenetre = "video_cam"
largeur_image = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
hauteur_image = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        #Connectez-vous à la 0ème caméra
        self.capture = cv2.VideoCapture(0)
        #Définir l'intervalle de dessin
        Clock.schedule_interval(self.update, 1.0 / 30)
    
    def update(self, dt):
        #Cadre de charge
        ret, self.frame = self.capture.read()
        #Convertir en texture Kivy
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr') 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        #Changer la texture de l'instance
        self.texture = texture

class SelfieCameraApp(App):

    def build(self):

        '''
        return
        
        '''

        
        
        #Button
        button_obj = Button(text="Prendre une Photo")
        
        
        button_obj.bind(on_press=self.take_selfie)



        #Layout
      
        layout = BoxLayout()
        
        layout.add_widget(button_obj)
        return layout
    


    def take_selfie(self, *args):

        
        
        print("...Photo en cours...")
        # On prend une photo
        nouvelle_image=[]
        ret, image = cam.read()#prend la photo
        if ret:

        # On affiche la fenêtre avec notre image
            cv2.imshow(nom_fenetre, image)    
            nouvelle_image.append(image)
            cv2.imwrite('./image.png',image)

            
            
            

       
        
            


if __name__=='__main__':
    SelfieCameraApp().run()
    
