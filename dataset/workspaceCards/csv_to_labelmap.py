"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python csv_to_labelmap.py --csv_input=data/train_labels.csv  --output_path=data/train.pbtxt
  # Create test data:
  python csv_to_labelmap.py --csv_input=data/test_labels.csv  --output_path=data/test.pbtxt
"""


import tensorflow.compat.v1 as tf
import pandas as pd

flags = tf.app.flags
flags.DEFINE_string('csv_input', './Playing Cards.v4-yolov8n.tensorflow/train/_annotations.csv', 'Path to the CSV input')
flags.DEFINE_string('output_path', './label_map.pbtxt', 'Path to output pbtxt file')

FLAGS = flags.FLAGS


def main(_):
    df = pd.read_csv(FLAGS.csv_input)
    label_maps = ""
    it = 1
    for i in df['class'].unique():
        label_maps += """
item {
    name: '"""+str(i)+"""'
    id: """+str(it)+"""
}
        """
        it+=1
    it=1
    with open(FLAGS.output_path, "w") as pbfile:
        pbfile.write(label_maps)

    label_maps = ""
    for i in df['class'].unique():
            label_maps += """
    """+str(it)+""": {
        'name': '"""+str(i)+"""'
        'id': """+str(it)+"""
    }
            """
            it+=1

    file = "test.txt"
    with open(file, "w") as pbfile:
        pbfile.write(label_maps)
        
        print('Labelmaps generated!')
    
if __name__ == '__main__':
    tf.app.run()