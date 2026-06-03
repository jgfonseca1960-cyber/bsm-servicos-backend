import cloudinary
import os

cloudinary.config(
    cloud_name=os.getenv("dksia9lvn"),
    api_key=os.getenv("477495685379182"),
    api_secret=os.getenv("HBNvXFfrl8fa7s3a2v5VjSPftz0"),
    secure=True)

import os

print("==== CLOUDINARY DEBUG ====")
print("CLOUD_NAME =", os.getenv("CLOUDINARY_CLOUD_NAME"))
print("API_KEY =", os.getenv("CLOUDINARY_API_KEY"))
print("SECRET OK =", bool(os.getenv("CLOUDINARY_API_SECRET")))
print("==========================")
print("🔥 Cloudinary carregado!")
