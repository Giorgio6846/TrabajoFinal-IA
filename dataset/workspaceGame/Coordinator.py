import tensorflow as tf
from Tools import SaveModel, Model
import socket

class Coordinator:
    def __init__(self, state_size, action_size, episodes, batch_size):
        self.ModelCreate = Model()
        self.episodes = episodes
        self.batch_size = batch_size

        self.model = self.ModelCreate.build_model(state_size, action_size)
        self.dictPC = {}

    def merge_networks(self, newModel):
        # Assuming net1 and net2 have the same architecture
        new_net = tf.keras.models.clone_model(self.model)
        new_net.build(
            self.model.input_shape
        )  # Build the model with the correct input shape

        weights1 = self.model.get_weights()
        weights2 = newModel.get_weights()

        new_weights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]
        new_net.set_weights(new_weights)

        self.model = new_net

    def Network():
        print()


if __name__ == "__main__":
    print()