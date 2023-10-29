import yt_dlp as youtube_dl

# URL of the video
url = input("Enter the video URL: ")

# Set options for yt_dlp to fetch available formats
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
}

# Fetch available formats for the video
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(url, download=False)
    formats = info_dict.get('formats', [])

# Create a dictionary to store unique video quality options
unique_qualities = {}

# Identify unique video quality options and store them in the dictionary
for format_info in formats:
    if format_info['vcodec'] != 'none':
        resolution = format_info['resolution'] if 'resolution' in format_info else 'Unknown'
        format_note = format_info.get('format_note', 'Unknown')
        unique_qualities[resolution] = format_note

# Display the unique video quality options
print("Available video quality options:")
for i, (resolution, format_note) in enumerate(unique_qualities.items(), start=1):
    print(f"{i}. {resolution} - {format_note}")

# Ask the user to choose the desired video quality by entering the option number
while True:
    try:
        choice = int(input("Enter the number of the desired video quality: "))
        if 1 <= choice <= len(unique_qualities):
            selected_quality = list(unique_qualities.keys())[choice - 1]
            break
        else:
            print("Invalid choice. Please enter a valid option number.")
    except ValueError:
        print("Invalid input. Please enter a valid option number.")

# Filter the video formats based on the selected quality
selected_formats = [format_info for format_info in formats if format_info['resolution'] == selected_quality]

if not selected_formats:
    print("No video format available in the selected quality.")
else:
    # Download one video from the selected quality
    ydl_opts['format'] = selected_formats[0]['format_id']
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"The requested video has been downloaded.")
