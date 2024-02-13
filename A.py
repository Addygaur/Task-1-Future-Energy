import cv2
import numpy as np

# Load the input image provided by the user
image_path = input("Enter the path to the input image: ")
input_image = cv2.imread(image_path)

# Copy the input image to draw overlays on
output_image = input_image.copy()

# Global variables
lines = []
polygons = []
line_count = 0
polygon_count = 0
drawing = False
start_point = None  # Variable to store the starting point of a line

# Function to draw shapes on the image
def draw_shapes(image, lines, polygons):
    global line_count, polygon_count
    for idx, line in enumerate(lines):
        cv2.line(image, line[0], line[1], (0, 0, 0), 2)
        dot1 = ((line[0][0] + line[1][0]) // 2, (line[0][1] + line[1][1]) // 2)  # Midpoint of the line
        cv2.circle(image, dot1, 5, (0, 255, 0), -1)  # Green dot
        label_position = (dot1[0] + 10, dot1[1] + 10)  # Adjust the label position
        cv2.putText(image, f'L-{idx + 1}', label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    for idx, polygon in enumerate(polygons):
        if len(polygon) > 2:
            cv2.polylines(image, [np.array(polygon)], True, (0, 0, 0), 2)  # Change color to black
            centroid = np.mean(np.array(polygon), axis=0, dtype=np.int32)
            side1 = polygon[0]  # First vertex
            side2 = polygon[-1]  # Last vertex
            cv2.circle(image, side1, 5, (0, 255, 0), -1)  # Green dot at one side
            cv2.circle(image, side2, 5, (0, 0, 255), -1)  # Red dot at other side
            label_position = (side1[0] + 10, side1[1] + 10)  # Adjust the label position
            cv2.putText(image, f'Bx-{idx + 1}', label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

# Set up the window and callback for drawing
cv2.namedWindow('Draw Shapes')

# Function to handle mouse events for drawing shapes
def mouse_callback(event, x, y, flags, param):
    global drawing, lines, polygons, start_point, line_count, polygon_count
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
        if shape_type == 'line':
            lines.append([start_point, start_point])  # Start and end point are the same initially for a line
            line_count += 1
        elif shape_type == 'polygon':
            polygons.append([(x, y)])
            polygon_count += 1
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if shape_type == 'line':
                lines[-1][1] = (x, y)  # Update the end point of the line
            elif shape_type == 'polygon':
                polygons[-1].append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if shape_type == 'polygon':
            polygons[-1].append(start_point)  # Close the polygon by adding the starting point

cv2.setMouseCallback('Draw Shapes', mouse_callback)

# Main loop
while True:
    output_copy = output_image.copy()

    # Draw shapes
    draw_shapes(output_copy, lines, polygons)

    # Show the output
    cv2.imshow('Draw Shapes', output_copy)

    # Check for key events
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.imwrite('output_image.png', output_copy)  # Save the final image
        break
    elif key == ord('l'):
        shape_type = 'line'
    elif key == ord('p'):
        shape_type = 'polygon'
    elif key == ord('c'):
        lines = []
        polygons = []
        line_count = 0
        polygon_count = 0

# Close all windows
cv2.destroyAllWindows()
