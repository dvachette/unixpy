#from unyx import FS
#fs = FS.FS("instances/marche.unyx")
#print(fs.listdir())

import io
from PIL import Image
with open("test.png", "rb") as f:
    data = f.read()

file = io.BytesIO(data)

img = Image.open(file)

img.show()
