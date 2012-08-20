import magic, re


HEADER = 4096
mime = magic.Magic(mime=True)
video_re = re.compile("^video\/.+")

def is_video(path):
    type = mime.from_file(path)
#    return video_re.match(type) != None
    return (video_re.match(type) != None) | (type == "application/octet-stream")

def is_video_buffer(buffer):
    type = mime.from_buffer(buffer)
#    return video_re.match(type) != None
    return (video_re.match(type) != None) | (type == "application/octet-stream")

def is_webm(s):
    parts = s.split(".")
    if parts[-1].lower() not in ['webm', 'webm']:
        return False
    else:
        return True
