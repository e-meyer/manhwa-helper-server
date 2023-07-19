import re

def get_smaller_cover_url(cover_url):
  pattern = r"-\d{3}x\d{3}"
  smaller_cover_url = re.sub(pattern, "", cover_url)  
  return smaller_cover_url