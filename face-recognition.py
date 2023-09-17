import os
import face_recognition
import cv2
import numpy as np

def load_images_and_store_face_vectors(image_folder_path):

    known_faces = []

    # Iterate over the images in the folder
    for image_file in os.listdir(image_folder_path):

        # Load the image
        #print(image_file)
        image = face_recognition.load_image_file(os.path.join(image_folder_path, image_file))

        # Find the face in the image
        face_locations = face_recognition.face_locations(image)

        # If there is a face in the image, add it to the list of known faces
        if face_locations:
            face_encoding = face_recognition.face_encodings(image, face_locations)[0]
            known_faces.append((image_file, face_encoding))
    #print(known_faces[0][1])    
    #print(known_faces[:,1])    
    return known_faces


def stream_video_and_display_rectangle_box(known_faces):

    # Start the webcam
    cap = cv2.VideoCapture(0)

    while True:

        # Capture a frame from the webcam
        ret, frame = cap.read()

        # Find the faces in the frame
        face_locations = face_recognition.face_locations(frame)

        # For each face in the frame, check if it is registered in the database
        for face_location in face_locations:

            # Get the face encoding for the face
            face_encoding = face_recognition.face_encodings(frame, [face_location])[0]

            # Find the closest match to the known faces in the database
            distances = face_recognition.face_distance([face[1] for face in known_faces], face_encoding)
            best_match_index = np.argmin(distances)
            print(distances[best_match_index])
            # If the distance to the best match is less than a certain threshold, then the face is registered in the database
            if distances[best_match_index] < 0.5:

                # Display a rectangle box around the face
                cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 255, 0), 2)

                # Display the name of the person
                cv2.putText(frame, known_faces[best_match_index][0], (face_location[3], face_location[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Face Recognition', frame)

        # If the user presses the 'q' key, quit the script
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()

    # Destroy all windows
    cv2.destroyAllWindows()

def main():

    # Load the known faces
    known_faces = load_images_and_store_face_vectors('C:/Users/Shivesh/Desktop/repo/image_detection/images')

    # Stream video and display a rectangle box if the face is registered or not
    stream_video_and_display_rectangle_box(known_faces)


if __name__ == '__main__':
    main()

