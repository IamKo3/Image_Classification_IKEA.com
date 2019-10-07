import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

#load model
model = load_model('./ikea_model_CNN.h5')

def predict(model, img):
    
    x = image.img_to_array(img)/255.0
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    
    return preds[0]

#classes = train_generator.class_indices
#labels = dict([(value,key) for (key,value) in classes.items()])
labels = {0:'Chair',1:'Couch',2:'Table',3:'Wardrobe'}

import matplotlib.pyplot as plt
import keras.preprocessing.image

images = ['test1.jpg', 'test2.jpg', 'test3.jpg', 'test4.jpg']
for i in images: 
    img = image.load_img('pepperfry_test/'+i,target_size=(256,256))

    pred = predict(model,img)
    print('Probabilities:',pred)
    t = '{:.2f}'.format(pred.max()*100)+'% '+labels[pred.argmax()]
    
    plt.title(t)
    plt.imshow(np.asarray(img))
    plt.show()
