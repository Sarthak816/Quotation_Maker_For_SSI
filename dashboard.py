import os

def get_all_quotations():
    folder = "quotations"
    files = []
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".pdf"):
                files.append(filename)
    return sorted(files, reverse=True)
