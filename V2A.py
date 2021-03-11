# importing the header lines
import moviepy.editor as mp
import os
import glob

# declaring the path of the dataset
path = os.path.join(r"C:\Users\hp\Desktop\VM\Video")

# list to store names of files that cannot be converted
not_completed = []

# operating over all files in the selected folder
for filename in glob.glob(os.path.join(path, "*")):
    try:
        # if the file has video, it gets converted to audio only
        clip = mp.VideoFileClip(filename)
        clip.audio.write_audiofile(os.path.join(r"C:\Users\hp\Desktop\VM\Audio", filename.split("\\")[-1] + "_audio.wav"), 
                                   codec='pcm_s16le', verbose=False)
    except:
        try:
            # if the file had no video, it is checked if it has audio and extracts audio
            clip = mp.AudioFileClip(filename)
            clip.write_audiofile(os.path.join(r"C:\Users\hp\Desktop\VM\Audio", filename.split("\\")[-1].split('.')[0] + "_audio.wav"), 
                                       codec='pcm_s16le', verbose=False)
        except:
            # save the names of files that cannot be converted
            print("File not converted to audio...", filename)
            not_completed.append(filename)
            f = open("not_completed_vid2aud.txt", "a")
            f.write(filename + "\n")
            f.close()

# indicate the end of the code and print filenames that gave problems
print("All files done.")
print("FILES NOT CONVERTED ARE...", not_completed)
