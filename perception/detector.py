import cv2
import numpy as np
import pybullet as p


def get_rover_camera_image(rover, width=640, height=480):
    """
    Simulates a camera mounted on the rover.
    Gets an image from the rover's perspective in PyBullet.

    Returns the image as a numpy array (like a real camera would)
    """

    # --- STEP 1: Get rover's current position and orientation ---
    # We need to know where the rover is to place the camera there
    rover_position, rover_orientation = p.getBasePositionAndOrientation(rover)

    # --- STEP 2: Calculate camera position ---
    # We mount the camera slightly above and in front of the rover
    # rover_position is (x, y, z) so we add a small offset
    cam_x = rover_position[0]
    cam_y = rover_position[1]
    cam_z = rover_position[2] + 0.5  # 0.5 meters above rover center

    # --- STEP 3: Define where the camera looks ---
    # The camera looks forward from the rover's position
    # We look slightly downward to see the ground ahead
    target_x = rover_position[0] + 1.0  # look 1 meter ahead
    target_y = rover_position[1]
    target_z = rover_position[2]        # at rover's height

    # --- STEP 4: Build the view matrix ---
    # This tells PyBullet the camera position and direction
    # Think of it like placing a real camera in the world
    view_matrix = p.computeViewMatrix(
        cameraEyePosition=[cam_x, cam_y, cam_z],
        cameraTargetPosition=[target_x, target_y, target_z],
        cameraUpVector=[0, 0, 1]  # Z axis is "up"
    )

    # --- STEP 5: Build the projection matrix ---
    # This defines the camera's lens properties
    # fov = field of view (how wide the camera sees, in degrees)
    # aspectRatio = width/height ratio of the image
    # nearVal/farVal = how close/far the camera can see
    projection_matrix = p.computeProjectionMatrixFOV(
        fov=60,
        aspect=width/height,
        nearVal=0.1,
        farVal=100
    )

    # --- STEP 6: Capture the image ---
    # getCameraImage returns several things:
    # width, height, rgba_pixels, depth_pixels, segmentation_mask
    # We mainly care about rgba_pixels (the actual image)
    _, _, rgba_image, depth_image, _ = p.getCameraImage(
        width=width,
        height=height,
        viewMatrix=view_matrix,
        projectionMatrix=projection_matrix
    )

    # --- STEP 7: Convert to OpenCV format ---
    # PyBullet gives us RGBA (4 channels including alpha/transparency)
    # OpenCV uses BGR (3 channels) so we need to convert
    rgba_array = np.array(rgba_image, dtype=np.uint8)
    # reshape to image dimensions
    rgba_array = rgba_array.reshape(height, width, 4)
    bgr_image = cv2.cvtColor(rgba_array, cv2.COLOR_RGBA2BGR)  # RGBA → BGR

    return bgr_image, depth_image


def detect_obstacles(image):
    """
    Detects red obstacles in the image using HSV color detection.

    Returns:
        detections: list of detected obstacle locations in the image
        annotated_image: the image with detection boxes drawn on it
    """

    # --- STEP 1: Convert BGR to HSV ---
    # As we discussed HSV is better for color detection
    # because it separates color from brightness
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # --- STEP 2: Define the red color range in HSV ---
    # Red is tricky in HSV — it wraps around at both ends of the hue spectrum
    # So we need TWO ranges and combine them
    # Range 1: lower red (hue 0-10)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

    # Range 2: upper red (hue 160-180)
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # --- STEP 3: Create masks ---
    # A mask is a black and white image
    # White pixels = matches our color range
    # Black pixels = doesn't match
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine both masks into one
    red_mask = cv2.bitwise_or(mask1, mask2)

    # --- STEP 4: Clean up the mask ---
    # Sometimes the mask has small noisy spots
    # We use morphological operations to clean it up
    # MORPH_OPEN removes small noise
    # MORPH_CLOSE fills small holes
    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    # --- STEP 5: Find contours ---
    # Contours are the outlines of the white regions in our mask
    # Each contour = one detected obstacle
    contours, _ = cv2.findContours(
        red_mask,
        cv2.RETR_EXTERNAL,      # only outer contours
        cv2.CHAIN_APPROX_SIMPLE  # compress contour points
    )

    # --- STEP 6: Process each detected obstacle ---
    detections = []
    annotated_image = image.copy()  # copy so we don't modify original

    for contour in contours:
        # Filter out very small detections (noise)
        area = cv2.contourArea(contour)
        if area < 500:  # ignore anything smaller than 500 pixels
            continue

        # Get bounding box around the contour
        # x, y = top left corner of box
        # w, h = width and height of box
        x, y, w, h = cv2.boundingRect(contour)

        # Calculate center of the detection
        center_x = x + w // 2
        center_y = y + h // 2

        # Store the detection
        detections.append({
            "center": (center_x, center_y),
            "bbox": (x, y, w, h),
            "area": area
        })

        # --- STEP 7: Draw on the annotated image ---
        # Draw green bounding box
        cv2.rectangle(annotated_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Draw red dot at center
        cv2.circle(annotated_image, (center_x, center_y), 5, (0, 0, 255), -1)

        # Add label
        cv2.putText(
            annotated_image,
            f"Obstacle ({center_x},{center_y})",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    return detections, annotated_image


def run_perception_demo(rover):
    """
    Captures one image from the rover's camera and
    runs obstacle detection on it. Shows the result.
    """

    print("📷 Capturing image from rover camera...")
    image, depth = get_rover_camera_image(rover)

    print("🔍 Running obstacle detection...")
    detections, annotated_image = detect_obstacles(image)

    print(f"✅ Detected {len(detections)} obstacles")
    for i, det in enumerate(detections):
        print(
            f"   Obstacle {i+1}: center={det['center']}, area={det['area']:.0f}px")

    # Show both original and annotated image side by side
    combined = np.hstack([image, annotated_image])
    cv2.imshow("Rover Camera — Left: Raw | Right: Detected", combined)
    cv2.waitKey(0)  # wait for any key press
    cv2.destroyAllWindows()

    return detections
