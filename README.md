# Video PSNR Comparison Tool

This tool encodes an existing video with different resolutions and bitrates, calculates the Peak Signal-to-Noise Ratio (PSNR) for each encoded version compared to the original, and logs the results. It's designed to help in analyzing the impact of various encoding settings on video quality.

## Features

- **Video Encoding**: Utilizes FFmpeg to encode videos with specified resolutions and bitrates.
- **PSNR Calculation**: Computes the PSNR between the original and each encoded video using OpenCV.
- **Progress Tracking**: Displays a progress bar during processing.
- **Results Logging**: Logs the resolution, bitrate, and PSNR of each encoded video to a file.

## Requirements

- **Python**: Version 3.6 or newer.
- **FFmpeg**: Must be installed and accessible from the command line.
- **Python Libraries**: `opencv-python`, `tqdm`.

## Installation

1. **Install FFmpeg**: Ensure FFmpeg is installed on your system. Instructions can be found on the [FFmpeg official website](https://ffmpeg.org/download.html).

2. **Install Python Dependencies**: Run the following command to install the required Python libraries:

  ```bash
  pip install opencv-python tqdm
  ```

## Usage

1. **Prepare Your Video File**: Place the video file you want to analyze in the same directory as the script or specify its path in the script.

2. **Modify Script Parameters** (optional): Adjust the `resolutions` and `bitrates` lists in the script to fit your analysis needs.

3. **Run the Script**: Execute the script with Python:

  ```bash
  python your_script_name.py
  ```

4. **Review the Results**: Check the generated `psnr_results.txt` file for the PSNR values, along with their corresponding resolutions and bitrates.

## Example Output

The `psnr_results.txt` file will contain lines formatted as follows:

    Resolution, Bitrate, PSNR
    1920x1080, 1000k, 45.67
    
## Troubleshooting

- **FFmpeg Not Found**: Ensure FFmpeg is correctly installed and its directory is added to your system's PATH environment variable.
- **Permission Issues**: Make sure you have read and write permissions in the script's directory.
- **Missing Input Video**: Verify the path to the input video is correct and accessible by the script.

## License

This project is open-source and available under the MIT License.
