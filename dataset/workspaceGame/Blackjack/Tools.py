import os
from tensorflow.keras import layers, models, Input
from pathlib import Path
import tensorflow as tf
import numpy as np
import random
import platform

VERBOSETRAIN = 0


class Model:
    def __init__(self, state_size, action_size):
        self.checkpointPath = (
            "./models/v{ver}/checkpoint_{comVer}/cp-{epoch:04d}.weights.h5"
        )
        self.modelPath = "./models/v{ver}/finished_{comVer}.keras"
        self.checkpointDir = (
            "./models/v{ver}/checkpoint_{comVer}/"
        )
        self.modelDir = "./models/v{ver}/"

        if (
            "TERM_PROGRAM" in os.environ.keys()
            and os.environ["TERM_PROGRAM"] == "vscode"
        ):
            self.checkpointPath = "./dataset/workspaceGame/models/v{ver}/checkpoint_{comVer}/cp-{epoch:04d}.weights.h5"
            self.modelPath = (
                "./dataset/workspaceGame/models/v{ver}/finished_{comVer}.keras"
            )
            self.checkpointDir = "./dataset/workspaceGame/models/v{ver}/checkpoint_{comVer}/"
            self.modelDir = (
                "./dataset/workspaceGame/models/v{ver}/"
            )

        self.state_size = state_size
        self.action_size = action_size
        self.model = 0
        self._build_model()

    def _build_model(self):
        self.model = models.Sequential()
        self.model.add(Input(shape=[self.state_size], dtype="uint8"))
        self.model.add(layers.Dense(128, activation="relu"))
        self.model.add(layers.Dense(self.action_size, activation="linear"))

        if platform.system() == "Darwin" and platform.processor() == "arm":
            opt = tf.keras.optimizers.legacy.Adam(learning_rate=0.01)
        else:
            opt = tf.keras.optimizers.Adam(learning_rate=0.01)

        self.model.compile(loss="mse", optimizer=opt, metrics=["accuracy"])
        self.model.summary()

    def act(self, state, epsilon, action_size):
        if np.random.rand() <= epsilon:
            return random.randrange(action_size)
        return self.predict(state)

    def remember(self, state, action, reward, next_state, done, memory):
        memory.append((state, action, reward, next_state, done))

    def predict(self, state):
        return np.argmax(
            self.model.predict(state, verbose=VERBOSETRAIN, use_multiprocessing=True)[0]
        )

    def loadModel(self, VERSION, COMPLETEDVERSION):
        self.model = models.load_model(
            self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION)
        )

    def saveModel(self, VERSION, COMPLETEDVERSION):
        if not os.path.exists(
            os.path.dirname(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION))
        ):
            Path(
                    self.modelDir.format(ver=VERSION, comVer=COMPLETEDVERSION)
            ).parent.mkdir(exist_ok=True, parents=True)

        self.model.save(self.modelPath.format(ver=VERSION, comVer=COMPLETEDVERSION))

    def loadCheckpoint(self, VERSION, COMPLETEDVERSION, EPOCH):
        self.model.load_weights(
            self.checkpointPath.format(
                ver=VERSION, epoch=EPOCH, comVer=COMPLETEDVERSION
            )
        )

    def saveCheckpoint(self, VERSION, COMPLETEDVERSION, EPOCH):
        if not os.path.exists(
            os.path.dirname(
                self.checkpointPath.format(
                    ver=VERSION, epoch=EPOCH, comVer=COMPLETEDVERSION
                )
            )
        ):
            Path(
                self.checkpointDir.format(
                    ver=VERSION, epoch=EPOCH, comVer=COMPLETEDVERSION
                )
            ).parent.mkdir(exist_ok=True, parents=True)

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
        if not os.path.exists("./models/v{ver}/info.txt".format(ver=VERSION)):
            Path("./models/v{ver}/info.txt".format(ver=VERSION)).parent.mkdir(exist_ok=True, parents=True)
            f = open("./models/v{ver}/info.txt".format(ver=VERSION), "w")
            if fileVersion == 1:
                f.write("Train based on SingleTraining")
            else:
                f.write("Train based on WorkerPC")
            f.close()
