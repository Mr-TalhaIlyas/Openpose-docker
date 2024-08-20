
import os
# Get current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
import sys
import cv2
import os
from sys import platform
import argparse
import pyopenpose as op

input_dir = os.path.join(current_dir, 'input')
output_dir = str(os.path.join(current_dir, 'output'))
log_dir = os.path.join(current_dir, 'logs')

os.makedirs(output_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)
# Set up the parameters for OpenPose
params = dict()
params["model_folder"] = os.path.join(current_dir, "models")
params["face"] = True
params["hand"] = True

def process_video(video_path, output_dir, save_annotated_video=False):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    video_name = os.path.basename(video_path)
    
    # Set JSON output directory for the current video
    json_output_dir = os.path.join(output_dir, video_name)
    os.makedirs(json_output_dir, exist_ok=True)
    params["write_json"] = json_output_dir

    # Initialize OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Video capture and processing
    cap = cv2.VideoCapture(video_path)
    
    if save_annotated_video:
        # Get video properties
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Output video writer
        out_video_path = os.path.join(output_dir, f"annotated_{video_name}")
        out_video = cv2.VideoWriter(out_video_path, fourcc, fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        
        # Save the annotated frame if needed
        if save_annotated_video:
            out_video.write(datum.cvOutputData)


    # Clean up
    cap.release()
    if save_annotated_video:
        out_video.release()
    print(f"Video processing complete for {video_name}")
    print(30*'-')

# load all video files in a dir
video_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4') or f.endswith('.avi')]
print(60*'=')
print(f'Found {len(video_files)} files.')
for video_file in video_files:
    video_path = os.path.join(input_dir, video_file)
    process_video(video_path=video_path, output_dir=output_dir, save_annotated_video=True)

