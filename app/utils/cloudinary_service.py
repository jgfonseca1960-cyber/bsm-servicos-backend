import cloudinary.uploader


def upload_imagem(file, pasta="empresas"):
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=pasta
        )

        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }

    except Exception as e:
        print("Erro Cloudinary:", str(e))
        return None