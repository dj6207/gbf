import os
 
def menu():
	lst = [str(n) + " " + file for n,file in enumerate(os.listdir())]
	print(*lst, sep="\n")
	file = os.listdir()[int(input("File n."))]
	return file
#print(file)
 
# This is what it is executed below using the file input above
file = menu()
output = os.path.splitext(file)[0] + "_2xb" + ".mp4"
cmd = f"""ffmpeg.exe -i {file} -filter:v "setpts=0.25*PTS" -an {output}
 
pause
"""
os.system(cmd) # run the ffmpeg command to 4x velocity
os.startfile(f"{output}") # runs the video