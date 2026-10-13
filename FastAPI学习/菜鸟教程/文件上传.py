import shutil
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

# 使用 UploadFile 可以将大文件自动写入磁盘，小文件则写入内存，使用默认值 None 可以使文件上传变为可选
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "没有上传文件"}
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
    }

# 使用 File 可以将整个文件加载到内存，适用于小文件
@app.post("/files")
async def create_file(file: bytes=File()):
    return {"file_size": len(file)}

# 多文件上传，使用列表接收多个文件
@app.post("/uploadfiles")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

# 表单与文件混合上传
@app.post("/items/")
async def create_item(
        name: str = Form(...),
        description: str | None = Form(None),
        file: UploadFile | None = None,
):
    result = {"name": name, "description": description}
    if file:
        result["filename"] = file.filename
    return result

# 保存上传的文件
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "文件上传成功"}