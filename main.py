import os
import cv2
import subprocess
from skimage.metrics import structural_similarity as compare_ssim
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

        if not ret_orig or not ret_enc:
            break

        # Resize frame_enc to match frame_orig's size
        if frame_orig.shape[:2] != frame_enc.shape[:2]:
            # Resize the encoded frame to match the original frame's resolution
            frame_enc = cv2.resize(frame_enc, (frame_orig.shape[1], frame_orig.shape[0]))

        frame_count += 1
        psnr = cv2.PSNR(frame_orig, frame_enc)
        psnr_values.append(psnr)

    cap_original.release()
    cap_encoded.release()

    average_psnr = sum(psnr_values) / len(psnr_values) if psnr_values else None
    print(f"Average PSNR: {average_psnr} dB over {frame_count} frames.")
    return average_psnr

def calculate_ssim(original_video, encoded_video):
    cap_original = cv2.VideoCapture(original_video)
    cap_encoded = cv2.VideoCapture(encoded_video)

    ssim_values = []
    while True:
        ret_orig, frame_orig = cap_original.read()
        ret_enc, frame_enc = cap_encoded.read()

        if not ret_orig or not ret_enc:
            break

        # Convert frames to grayscale as SSIM is traditionally calculated on grayscale images
        frame_orig_gray = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2GRAY)
        frame_enc_gray = cv2.cvtColor(frame_enc, cv2.COLOR_BGR2GRAY)

        # Resize encoded frame to match original frame's size for SSIM calculation
        frame_enc_gray = cv2.resize(frame_enc_gray, (frame_orig_gray.shape[1], frame_orig_gray.shape[0]))

        # Calculate SSIM between the two frames
        ssim = compare_ssim(frame_orig_gray, frame_enc_gray)
        ssim_values.append(ssim)

    cap_original.release()
    cap_encoded.release()

    # Calculate average SSIM over all frames
    average_ssim = sum(ssim_values) / len(ssim_values) if ssim_values else 0
    print(f"Average SSIM: {average_ssim}")
    return average_ssim

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
    resolutions = ['1920x1080','1280x720','720x480','480x360']  # Example resolutions
    bitrates = [f'{x}k' for x in range(1000, 21000, 1000)]

    # Open a file for logging the results in CSV format
    with open("ssim_results.csv", "w") as log_file:
        log_file.write(",")  # Header row starts with a blank cell
        for resolution in resolutions:
            log_file.write(resolution + ",")
        log_file.write("\n")
        
        total_iterations = len(bitrates)
        progress_bar = tqdm(total=total_iterations, unit='iteration')

        for bitrate in bitrates:
            log_file.write(bitrate + ",")  # Row starts with bitrate
            for resolution in resolutions:
                output_video = f'output_{resolution}_{bitrate}.mp4'
                encode_video(original_video, output_video, resolution, bitrate)
                ssim_value = calculate_ssim(original_video, output_video)
                # os.remove(output_video)  # Delete the encoded video file
                progress_bar.update(1)  # Update progress bar after each iteration
                
                # Log the result to the file and also print it
                log_file.write(str(ssim_value) + ",")
                print(f"Bitrate: {bitrate}, Resolution: {resolution}, SSIM: {ssim_value}")
            log_file.write("\n")

        progress_bar.close()

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()