# Prerequesites:
#  Install moviepy to convert .mov to .mp4 files via pip:  !pip install moviepy
import moviepy.editor as mp
import os
 
def convert_mov_to_mp4(input_file, output_file):
    """
    This function converts a .mov file to .mp4 format.
    
    Parameters:
    input_file (str): The path to the input .mov file
    output_file (str): The path to save the output .mp4 file
    
    Returns:
    bool: True if the conversion is successful, False otherwise
    """
    try:
        # Check if the input file has .mov extension
        if not input_file.endswith('.mov'):
            raise ValueError("Input file must have .mov extension")
        
        # Check if the output file has .mp4 extension
        if not output_file.endswith('.mp4'):
            raise ValueError("Output file must have .mp4 extension")
        
        # Convert the .mov file to .mp4 using moviepy
        video = mp.VideoFileClip(input_file)
        video.write_videofile(output_file)
        
        return True
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return False
    

def main():

    directory = "./videos/Sprungtest2/Front"
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename)) as f:
                output_file = "./videos/Sprungtest2/Front" + filename + ".mov"
                convert_mov_to_mp4(f, output_file)


if __name__ == "__main__":
    main()
