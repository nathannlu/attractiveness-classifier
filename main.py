
from tinder_api import tinderAPI
from mtcnn.mtcnn import MTCNN
import rate
from skimage import io

s = tinderAPI(process.env.X_AUTH_TOKEN)
list_of_nearby = s.nearby_persons()[0].download_images()

# Create detector with default weights
detector = MTCNN()

# Counter
i = 0

all_faces = []

for img_url in list_of_nearby:
    i = i + 1
    print(f"Loading image {i}")
    filename = img_url 

    # Load url
    pixels = io.imread(filename)

    # Detect faces in the image
    faces = detector.detect_faces(pixels)

    # Display faces on the original image
    rate.draw_faces(filename, faces, all_faces)


    input("Press Enter to continue to rate next image")

print(all_faces)
