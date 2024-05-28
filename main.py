from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from collections import deque
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from numpy import array
import os
import uuid
from db_crud import CRUD
import logging

TRIPOSR_DIR = "./"
IMG_DIR = os.path.join(TRIPOSR_DIR,'input_image/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','TripoSR/','input_image/')

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ModelOut(BaseModel):
    glbUrl: str


@app.get("/", tags=["model"])
def modelCheck():
    """
    <b>서버 체크</b>할 때 사용하는 메소드입니다.
    """
    try:
        return {"message": "Model is running"}
    except:
        return {"message": "Something warning"}


@app.post("/", tags=["model"])
async def model(exhibit_id, file: UploadFile = File(...)) -> list[ModelOut]:
    """
    # 모델 실행
    - RequestBody: 이미지 파일
    """
    access_key = "AKIAQDCPJT66UNLYHXWZ"
    print("INFO:     [POST] 파일 업로드")
    saved_filename = str(uuid.uuid4())+".png"

    print("INFO:     [POST] UUID 생성")
    file_location = os.path.join(IMG_DIR, saved_filename)

    print("INFO:     [POST] file_location 생성")
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    print("INFO:     [POST] input_file 저장")
    UUID = uuid.uuid4()
    os.system(f"python run.py {file_location} --output-dir output/ --model-save-format glb --access-key {access_key} --uuid {UUID}")
    print("INFO:     [POST] input_file 저장")

    glbUrl = f"https://jolvrebucket.s3.ap-northeast-3.amazonaws.com/{UUID}.glb"
    # DB 연결
    print(f"exhibit_id = {exhibit_id}")
    db = CRUD(host="localhost", dbname="jolvre", user="ms9648", passwd="kjs730526^^", port="5432")
    db.updateDB(table="exhibit", column="image3d", data=glbUrl, exhibit_id=exhibit_id)
    print("main: Model processing exit")

    
    
    return [
        ModelOut(glbUrl = f"https://jolvrebucket.s3.ap-northeast-3.amazonaws.com/{UUID}.glb")
    ]