from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import json

app = FastAPI(
    title="오픈소스소프트웨어실습 - Courses API",
    description="Docker 및 EC2 배포 실습을 위한 FastAPI 애플리케이션입니다.",
    version="1.0.0"
)

# 데이터 파일 경로 설정 (동일 디렉토리의 courses.json)
DB_FILE = "courses.json"

# 과제 조건에 맞는 Pydantic 모델 정의
class Course(BaseModel):
    id: int
    title: str
    instructor: str
    description: Optional[str] = None

# 초기 데이터 생성 함수 (파일이 없을 경우 대비)
def load_data() -> List[dict]:
    if not os.path.exists(DB_FILE):
        initial_data = [
            {"id": 1, "title": "오픈소스소프트웨어실습", "instructor": "교수님", "description": "Docker 배포 실습"},
            {"id": 2, "title": "웹프로그래밍", "instructor": "김교수", "description": "FastAPI 실습"}
        ]
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=4)
        return initial_data
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: List[dict]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# [기능 1] GET /courses - 전체 과목 목록 조회
@app.get("/courses", response_model=List[Course])
def get_courses():
    return load_data()

# [기능 2] POST /courses - 새로운 과목 추가
@app.post("/courses", response_model=Course)
def create_course(course: Course):
    data = load_data()
    
    # 중복 ID 검사
    for existing_course in data:
        if existing_course["id"] == course.id:
            raise HTTPException(status_code=400, detail="이미 존재하는 과목 ID입니다.")
    
    # 새로운 과목 추가 및 저장
    data.append(course.dict())
    save_data(data)
    return course

# [기능 3] 루트 경로 확인용
@app.get("/")
def read_root():
    return {"message": "FastAPI Docker 애플리케이션이 정상 구동 중입니다. /courses 나 /docs 로 접속해 주세요."}