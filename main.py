from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

# Lấy danh sách khóa học
@app.get("/courses", tags= ["Courses"])
async def get_all_courses():
    return {
        "massage": "Lấy danh sách khóa học thành công",
        "data": courses
    }

# Lấy danh sách khóa học chi tiết
@app.get("/course/{course_id}", tags=["Courses"])
async def get_course_infor(course_id: int):
    for course in courses:
        if course_id == course["id"]:
            return {
                "message": f"Lấy danh sách khóa học {course_id} thành công",
                "data": course
            }
    raise HTTPException(status_code= 404, detail= "Course not found.")

# Thêm khóa học

class courseCreate(BaseModel):
    code: str 
    name: str = Field(..., min_length=2)
    duration: int = Field(ge= 0)
    fee: float = Field(gl = 0)

@app.post("/course", tags=["Courses"])
async def create_course(new_course: courseCreate):

    list_course = {
        "id": len(courses) + 1,
        "code": new_course.code,
        "name": new_course.name,
        "duration": new_course.duration,
        "fee": new_course.fee
    }

    for course in courses:
        if course["code"] == new_course.code:
            raise HTTPException(
                status_code= 409,
                detail= "Code khóa học đã tồn tại"
            )

    courses.append(list_course)
    return {
        "message": "Thêm khóa học thành công",
        "data": list_course
    }

# Cập nhật khóa học
@app.put("/course/{course_id}", tags= ["Courses"])
async def update_course(course_id: int, update_course: courseCreate):
    for course in courses:
        if course["id"] == course_id:
            course.update(update_course)
            return {
                "message": "Cập nhật khóa học thành công",
                "data": course
            }
    raise HTTPException (
        status_code= 404,
        detail= "Course not found"
    )

# Xóa khóa học
@app.delete("/couse/{course_id}", tags= ["Courses"])
async def delete_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return {
                "message": "Xóa thành công",
            }
    raise HTTPException(
        status_code= 404,
        detail= "Course not found"
    )
