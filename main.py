import os
import cv2
import subprocess
from tqdm import tqdm

def encode_video(input_video, output_video, resolution, bitrate):
    command = [
        'ffmpeg', '-i', input_video, '-s', resolution, '-b:v', bitrate,
        '-vcodec', 'libx264', '-preset', 'slow', '-y', output_video
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def calculate_psnr(original_video, encoded_video):
    cap_original = cv2.VideoCapture(original_video)
    cap_encoded = cv2.VideoCapture(encoded_video)

    frame_count = 0
    psnr_values = []
    while True:
        ret_orig, frame_orig = cap_original.read()
        ret_enc, frame_enc = cap_encoded.read()
        #print(f"Reading frames: Original={ret_orig}, Encoded={ret_enc}, Frame={frame_count}")
        
        if not ret_orig or not ret_enc:
            break

        frame_count += 1
        psnr = cv2.PSNR(frame_orig, frame_enc)
        psnr_values.append(psnr)

    cap_original.release()
    cap_encoded.release()
    average_psnr = sum(psnr_values) / len(psnr_values) if psnr_values else None
    print(f"Average PSNR: {average_psnr} dB over {frame_count} frames.")
    return average_psnr

def main():
    original_video = '1080_test.y4m'
    # Check if the file exists from the script's perspective
    if os.path.exists(original_video):
        print(f"File exists: {original_video}")
    else:
        print(f"File does not exist: {original_video}")
        return

    # Additional debugging: Print the absolute path
        
    print(f"Absolute path: {os.path.abspath(original_video)}")
    resolutions = ['1920x1080', '1280x720', '640x480', '480x360']  # Example resolutions
    bitrates = [f'{x}k' for x in range(1000, 31000, 1000)]

    # Open a file for logging the results
    with open("psnr_results.txt", "w") as log_file:
        log_file.write("Resolution, Bitrate, PSNR\n")

        total_iterations = len(resolutions) * len(bitrates)
        progress_bar = tqdm(total=total_iterations, unit='iteration')

        for resolution in resolutions:
            for bitrate in bitrates:
                output_video = f'output_{resolution}_{bitrate}.mp4'
                encode_video(original_video, output_video, resolution, bitrate)
                psnr = calculate_psnr(original_video, output_video)
                os.remove(output_video)  # Delete the encoded video file
                progress_bar.update(1)  # Update progress bar after each iteration
                
                # Log the result to the file and also print it
                result = f"{resolution}, {bitrate}, {psnr}\n"
                log_file.write(result)
                print(result.strip())

        progress_bar.close()

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()