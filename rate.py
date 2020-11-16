from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle 
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
import cv2
import numpy as np
import urllib 
from skimage import io

def draw_image_with_boxes(filename, result_list):
    # Load the image
    data = pyplot.imread(filename)

    # Plot the image
    pyplot.imshow(data)

    # Get the context for drawing boxes
    ax = pyplot.gca()

    # Plot each box
    for result in result_list:
        # Get coordinates
        x, y, width, height = result['box']

        # Create the shape
        rect = Rectangle((x, y), width, height, fill=False, color="red")

        # Draw the box
        ax.add_patch(rect)

        # Draw the dots
        for key, value in result['keypoints'].items():
            # Create and draw dot
            dot = Circle(value, radius=2, color="red")
            ax.add_patch(dot)

    # Show the plot
    pyplot.show()

def draw_faces(filename, result_list, array_of_faces):
    # Load the image
    data = io.imread(filename)

    # Plot each face as a subplot
    for i in range(len(result_list)):
        # Get coordinates
        x1, y1, width, height = result_list[i]['box'] 
        x2, y2 = x1 + width, y1 + height
        
        # Define subplot 
        pyplot.axis('off')

        # Plot face
        pyplot.imshow(data[y1:y2, x1:x2])

        array_of_faces.append(data[y1:y2, x1:x2])

        # Rate face
        print(give_rating(data[y1:y2, x1:x2]))

        # Show the plot
        pyplot.show()

def preprocess_image(image,target_size):
    return cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),target_size) / .255


def give_rating(image):
    model_path = 'models/attractiveness_classifier.h5'
    model = load_model(model_path)
    score = model.predict(np.expand_dims(preprocess_image(image, (350,350)), axis=0))
    return score
