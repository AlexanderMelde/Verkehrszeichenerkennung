import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # disable TF warning about cpu instructions
import tensorflow as tf
import cv2
import numpy as np
import os

#this function classifies an opencv image
def analyse_frame(opencv_image):
    # Format for the Mul:0 Tensor
    # img2 = cv2.resize(opencv_image, dsize=(299, 299), interpolation=cv2.INTER_CUBIC)
    # Numpy array
    # np_image_data = np.asarray(opencv_image)
    # maybe insert float convertion here - np_image_data=cv2.normalize(np_image_data.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)
    # np_final = np.expand_dims(np_image_data, axis=0)
    # image_data = np_final  # Read in the image_data
    with tf.device('/device:GPU:0'): # use gpu instead of cpu ("/cpu:0")
        image_data = np.array(opencv_image)[:, :, 0:3]      #convert opencv image to a numpy array that can be processed by the DecodeJpeg tensor
        # Reset Graph
        tf.reset_default_graph()
        # Loads label file, strips off carriage return
        label_lines = [line.rstrip() for line
                       in tf.gfile.GFile(os.path.join(os.path.dirname(__file__),"..","tf_files/retrained_labels.txt"))]

        # Unpersists graph from file
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(tf.gfile.FastGFile(os.path.join(os.path.dirname(__file__),"..","tf_files/retrained_graph.pb"), 'rb').read())
        _ = tf.import_graph_def(graph_def, name='')
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = tf.Session().graph.get_tensor_by_name('final_result:0')
        predictions = tf.Session().run(softmax_tensor, {'DecodeJpeg:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        results = []
        results_readable = []
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            results_readable.append('%s (score = %.5f)' % (human_string, score))
            results.append((human_string,score))

        # print("tf: "+str(results_readable))
        return results   # array of (label,score) [(00014,0.03),(00025,0.006)]
