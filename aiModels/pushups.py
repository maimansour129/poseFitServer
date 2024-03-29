import cv2 as cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Setup mediapipe instance
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Curl counter variables
counter = 0
stage = 'Down'
instructions = "Start Taining"
landmarksList = []
poseIsCorrect = False


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


def receive_frame(frame):

    global counter
    global instructions
    global stage
    global landmarksList
    global poseIsCorrect

    rotatedImage = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # (1) => flip on x-axis (skeleton flipped while drawing)
    flippedImage = cv2.flip(rotatedImage, 1)

    image = cv2.cvtColor(flippedImage, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        left_knee = [0, 0]

        right_knee = [0, 0]

        # List to Draw Skeleton
        landmarksList = [left_wrist, left_elbow, left_shoulder, left_hip,
                         left_knee, left_ankle, right_ankle, right_knee,
                         right_hip, right_shoulder, right_elbow, right_wrist]

        # Calculate angle
        left_torso_angle = calculate_angle(left_wrist, left_hip, left_shoulder)

        left_elbow_angle = calculate_angle(
            left_shoulder, left_elbow, left_wrist)

        right_torso_angle = calculate_angle(
            right_wrist, right_shoulder, right_hip)

        right_elbow_angle = calculate_angle(
            right_shoulder, right_elbow, right_wrist)


        # Curl counter logic
        if ((left_torso_angle > 100) or (right_torso_angle > 100)):

            poseIsCorrect = False
            instructions = "Fix your Posture"

        if ((left_torso_angle < 100) and (right_torso_angle < 100)):

            poseIsCorrect = True

            if (left_elbow_angle < 45 and right_elbow_angle < 45) and stage == 'Down':
                stage = "Up"
                counter += 1
                instructions = "Go Down"

            elif ((left_elbow_angle < 160 and left_elbow_angle > 30) and (right_elbow_angle < 160 and right_elbow_angle > 30)) and stage == 'Up':
                instructions = "Go Down more"

            elif left_elbow_angle >= 160 and right_elbow_angle >= 160 and stage == 'Up':
                stage = "Down"
                instructions = "Go Up"

            elif ((left_elbow_angle > 30 and left_elbow_angle < 160) and (right_elbow_angle > 30 and right_elbow_angle < 160)) and stage == 'Down':
                instructions = "Go Up more"
            
            elif counter and counter % 5 == 0:
                instructions = 'Keep Going'
    except:
        pass

    return image, counter, instructions, landmarksList, poseIsCorrect
