import os
import cloudinary

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

print("==== CLOUDINARY DEBUG ====")
print("CLOUD_NAME =", os.getenv("CLOUDINARY_CLOUD_NAME"))
print("API_KEY =", os.getenv("CLOUDINARY_API_KEY"))
print("SECRET OK =", bool(os.getenv("CLOUDINARY_API_SECRET")))
print("==========================")
print("🔥 Cloudinary carregado!")