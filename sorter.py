def get_category(file):
    extension = file.suffix.lower()

    if extension in [".jpg", ".jpeg", ".png"]:
        return "Images"
    elif extension in [".pdf", ".docx", ".txt"]:
        return "Documents"
    elif extension in [".mp3", ".wav"]:
        return "Audio"
    else:
        return "Others"