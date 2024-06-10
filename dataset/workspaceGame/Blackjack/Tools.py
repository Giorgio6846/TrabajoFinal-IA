import os
from tensorflow.keras import layers, models, Input
import tensorflow as tf
import numpy as np
import random
import platform

VERBOSETRAIN = 0

class SaveModel:
    def __init__(self):
        self.checkpointPath = "./models/v{ver}/cp-{epoch:04d}.weights.h5"
        self.modelPath = "./models/v{ver}/finished_{comVer}.keras"
        if 'TERM_PROGRAM' in os.environ.keys() and os.environ['TERM_PROGRAM'] == 'vscode':
            self.checkpointPath = "./dataset/workspaceGame/models/v{ver}/cp-{epoch:04d}.weights.h5"
            self.modelPath = "./dataset/workspaceGame/models/v{ver}/finished_{comVer}.keras"


    def saveCheckpoint(self, model, VERSION, EPOCH):
        path_dir = os.path.dirname(self.checkpointPath)

        model.save_weights(self.checkpointPath.format(ver=VERSION, epoch=EPOCH))

    def loadCheckpoint(self, model, VERSION, EPOCH):
        path_dir = os.path.dirname(self.checkpointPath)
        return model.load_weights(self.checkpointPath.format(ver=VERSION, epoch=EPOCH))

    def saveModel(self, model, VERSION, COMPLETEDVERSION):
        path_dir = os.path.dirname(self.modelPath)

        model.save(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION))

    def loadModel(self, VERSION, COMPLETEDVERSION):
        path_dir = os.path.dirname(self.modelPath)

        return models.load_model(
            self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION)
        )
    
    def latestModel(self, VERSION):
        fileExist = True
        COMPLETEDVERSION = 1
        
        while fileExist:
            if os.path.exists(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION)):
                print(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION))
                COMPLETEDVERSION +=1
            else:
                fileExist = False

        return COMPLETEDVERSION
        
class Model:

    def _build_model(self, state_size, action_size):
        model = models.Sequential()
        model.add(Input(shape = [state_size], dtype = 'uint8'))
        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dense(action_size, activation="linear"))
        
        if platform.system() == "Darwin" and platform.processor() == "arm":
            opt = tf.keras.optimizers.legacy.Adam(learning_rate=0.01)
        else:
            opt = tf.keras.optimizers.Adam(learning_rate=0.01)

        model.compile(loss="mse", optimizer=opt, metrics =['accuracy'])
        model.summary()
    
        return model

    def act(self, state, epsilon, action_size, model):
        if np.random.rand() <= epsilon:
            return random.randrange(action_size)
        act_values = model.predict(state, verbose=VERBOSETRAIN)
        return np.argmax(act_values[0])

    def remember(self, state, action, reward, next_state, done, memory):
        memory.append((state, action, reward, next_state, done))
