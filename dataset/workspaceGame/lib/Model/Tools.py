import os
from pytz import VERSION
from tensorflow.keras import layers, models, Input
import tensorflow as tf
import numpy as np
import random
import platform

VERBOSETRAIN = 0
LAYERS = 256
LOGSPATH = "./models/v{VERSION}/logs"

class Tools:
    def __init__(self):
        self.checkpointPath = (
            "./../GameModels/v{ver}/checkpoint_{comVer}/cp-{epoch:04d}.weights.h5"
        )
        self.modelPath = "./../GameModels/v{ver}/finished_{comVer}.keras"
        self.checkpointDir = "./../GameModels/v{ver}/checkpoint_{comVer}/"
        self.modelDir = "./../GameModels/v{ver}/"

        if (
            "TERM_PROGRAM" in os.environ.keys()
            and os.environ["TERM_PROGRAM"] == "vscode"
        ):
            self.checkpointPath = "./dataset/workspaceGame/GameModels/v{ver}/checkpoint_{comVer}/cp-{epoch:04d}.weights.h5"
            self.checkpointDir = (
                "./dataset/workspaceGame/GameModels/v{ver}/checkpoint_{comVer}/"
            )
            self.modelPath = (
                "./dataset/workspaceGame/GameModels/v{ver}/finished_{comVer}.keras"
            )
            self.modelDir = "./dataset/workspaceGame/GameModels/v{ver}/"

    def loadModel(self, VERSION, COMPLETEDVERSION):
        self.model = models.load_model(
            self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION)
        )

    def saveModel(self, VERSION, COMPLETEDVERSION):
        self.checkFolder(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION))
        self.model.save(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION))

    def loadCheckpoint(self, VERSION, COMPLETEDVERSION, EPOCH):
        self.model.load_weights(
            self.checkpointPath.format(
                ver=VERSION, epoch=EPOCH, comVer=COMPLETEDVERSION
            )
        )

    def saveCheckpoint(self, VERSION, COMPLETEDVERSION, EPOCH):
        self.checkFolder(
            self.checkpointPath.format(
                ver=VERSION, epoch=EPOCH, comVer=COMPLETEDVERSION
            )
        )

        self.model.save_weights(
            self.checkpointPath.format(
                ver=VERSION, epoch=EPOCH, comVer=COMPLETEDVERSION
            )
        )

    def getFinalLatestVersion(self, VERSION):
        fileExist = True
        COMPLETEDVERSION = 1

        while fileExist:
            if os.path.exists(
                self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION)
            ):
                print(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION))
                COMPLETEDVERSION += 1
            else:
                fileExist = False

        return COMPLETEDVERSION

    def getCheckpointLatestVersion(self, VERSION, COMPLETEDVERSION):
        fileExist = True
        EPOCH = 1

        while fileExist:
            if os.path.exists(
                self.checkpointPath.format(
                    ver=VERSION, comVer=COMPLETEDVERSION, epoch=EPOCH
                )
            ):
                print(
                    self.checkpointPath.format(
                        ver=VERSION, comVer=COMPLETEDVERSION, epoch=EPOCH
                    )
                )
                EPOCH += 1
            else:
                fileExist = False

        return EPOCH

    def saveStatus(self, fileVersion, VERSION):
        self.checkFolder(
            self.modelDir.format(ver=VERSION) + "config.txt".format(ver=VERSION)
        )
        f = open(
            self.modelDir.format(ver=VERSION) + "config.txt".format(ver=VERSION), "w"
        )
        if fileVersion == 1:
            f.write("Train based on SingleTraining")
        else:
            f.write("Train based on WorkerPC")
        f.close()

    def saveConfigModel(self, dict, VERSION):
        self.checkFolder(self.modelDir.format(ver=VERSION)+"info.txt")
        f = open(self.modelDir.format(ver=VERSION) + "info.txt", "w")
        for key, value in dict.items():
            f.write(f"{key}: {value} \n")
        f.close()

    def saveConfigModelComVer(self, dict, VERSION, comVer):
        self.checkFolder(self.modelDir.format(ver=VERSION)+f"info{comVer}.txt")
        f = open(self.modelDir.format(ver=VERSION) + f"info{comVer}.txt", "w")
        for key, value in dict.items():
            f.write(f"{key}: {value} \n")
        f.close()

    def checkFolder(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))


class ModelA3C(Tools):
    def __init__(self, state_size, action_size):
        super().__init__()

        self.state_size = state_size
        self.action_size = action_size

    def _build_modelCritic(self):
        self.model = models.Sequential()
        self.model.add(Input(shape=[self.state_size], dtype="uint8"))
        self.model.add(layers.Dense(LAYERS, activation="relu"))
        self.model.add(layers.Dense(LAYERS/2, activation="relu"))
        self.model.add(layers.Dense(self.action_size, activation="linear"))

        #self.model.compile(loss="mse", optimizer=opt, metrics=["accuracy"])
        #self.model.summary()

    def _build_modelActor(self):
        self.model = models.Sequential()
        self.model.add(Input(shape=[self.state_size], dtype="uint8"))
        self.model.add(layers.Dense(LAYERS, activation="relu"))
        self.model.add(layers.Dense(self.action_size, activation="softmax"))

        #self.model.compile(loss="mse", optimizer=opt, metrics=["accuracy"])
        #self.model.summary()

class ModelDQN(Tools):
    def __init__(self, state_size, action_size, learning_rate):
        super().__init__()

        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self._build_model()

    def _build_model(self):
        self.model = models.Sequential()
        self.model.add(Input(shape=[self.state_size], dtype="uint8"))
        self.model.add(layers.Dense(LAYERS, activation="relu"))
        self.model.add(layers.Dense(self.action_size, activation="linear"))

        if platform.system() == "Darwin" and platform.processor() == "arm":
            opt = tf.keras.optimizers.legacy.Adam(learning_rate=self.learning_rate)
        else:
            opt = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

        self.model.compile(loss="mse", optimizer=opt, metrics=["accuracy"])
        self.model.summary()

    def act(self, state, epsilon, action_size):
        if np.random.rand() <= epsilon:
            return random.randrange(action_size)
        return self.predict(state)

    def predict(self, state):
        return np.argmax(
            self.model.predict(state, verbose=VERBOSETRAIN, use_multiprocessing=True)[0]
        )

    def modelFit(self, state, target_f, VERBOSE, STT, version):
        callbacks = tf.keras.callbacks.TensorBoard(
            log_dir=LOGSPATH.format(VERSION=version),
            histogram_freq=0,
            write_graph=True,
        )

        if STT:       
            self.model.fit(state, target_f, epochs = 1, verbose=VERBOSE, use_multiprocessing = True, callbacks=callbacks)
        else:
            self.model.fit(
                state, target_f, epochs=1, verbose=VERBOSE, use_multiprocessing=True
            )
