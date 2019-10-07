# Importing the Keras libraries and packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator


import tensorflow as tf
tf.test.gpu_device_name()


# Initializing the CNN
model = Sequential()

# Convolution
model.add(Conv2D(32, (3, 3), input_shape = (256, 256, 3), activation = 'relu'))

# Pooling
model.add(MaxPooling2D(pool_size = (2, 2)))

# Second convolutional layer
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

# Third convolutional layer
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

# Flattening
model.add(Flatten())

# Full connection
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 128, activation = 'relu'))

model.add(Dense(units = 4, activation = 'softmax'))

# Compiling the CNN
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
model.summary()




TRAIN_DIR = './split_sets/train'
TEST_DIR = './split_sets/val'

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(TRAIN_DIR,
                                                 target_size = (256, 256),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

validation_generator = test_datagen.flow_from_directory(TEST_DIR,
                                            target_size = (256, 256),
                                            batch_size = 32,
                                            class_mode = 'categorical')



STEPS_PER_EPOCH = 100 # train_len/batch size
VALIDATION_STEPS = 25 # val_len/batch_size

MODEL_FILE = './ikea_model_CNN.hdf5'
mc = ModelCheckpoint(MODEL_FILE,monitor='val_acc',save_best_only=True, verbose=1)
callbacks_list = [mc]
history = model.fit_generator(train_generator,
                         steps_per_epoch = STEPS_PER_EPOCH,
                         epochs = 15,
                         validation_data = validation_generator,
                         validation_steps = VALIDATION_STEPS)


# ## Training Accuracy = 80.64, Val Accuracy = 73.49


import matplotlib.pyplot as plt
def plot_training(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(acc))
    
    plt.plot( acc)
    plt.plot( val_acc)
    plt.legend(['train','val'])
    plt.title('Training and validation accuracy')
  
    plt.figure()
    plt.plot(loss)
    plt.plot(val_loss)
    plt.legend(['train','val'])
    plt.title('Training and validation loss')
    
    plt.show()
  


plot_training(history)


