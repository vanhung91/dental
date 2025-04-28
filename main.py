from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
print("Biến môi trường server:", os.environ)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cho phép gọi API từ web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lấy API Key từ biến môi trường
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Định nghĩa body nhận câu hỏi
class QuestionRequest(BaseModel):
    question: str
@app.get("/env")
def read_env():
    return dict(os.environ)

@app.get("/")
def read_root():
    return {"message": "Hello, this is your Dental AI Chatbot 🚀 (powered by OpenAI)"}

@app.post("/ask")
async def ask_question(body: QuestionRequest):
    question = body.question
    api_key_check = os.getenv("OPENAI_API_KEY")
    print(f"API KEY thực tế server đọc được lúc request: {api_key_check}")  # <-- Dòng này thêm vào!

    if not api_key_check:
        return {"error": "API Key không tồn tại trên server"}

    openai.api_key = api_key_check

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Bạn là Bác sĩ răng hàm mặt của Nha Khoa Linh Xuân, với 20 năm kinh nghiệm. Vai trò của bạn là: Tư vấn, giải đáp các thắc mắc trước, trong và sau điều trị nha khoa. Giao tiếp thân thiện, nhẹ nhàng, chuyên nghiệp. Tư vấn các dịch vụ: Trồng răng Implant, Niềng răng, Bọc răng sứ thẩm mỹ, Nhổ răng khôn an toàn, Trám răng sâu. Am hiểu tâm lý khách hàng, biết gợi mở hành động đặt lịch hoặc để lại số điện thoại. Phong cách giao tiếp: Dùng từ ngữ đơn giản, dễ hiểu, thân thiện như CSKH chuyên nghiệp. Trả lời ngắn gọn, rõ ràng. Luôn đồng cảm, khuyến khích khách yên tâm, giải tỏa nỗi lo. Dữ liệu chính: Nha Khoa Linh Xuân hoạt động từ 2007, có 2 cơ sở Thủ Đức và Dĩ An. Cơ sở Thủ Đức: 51 Quốc Lộ 1K, Phường Linh Xuân, TP Thủ Đức, HCMC. Cơ sở Dĩ An: 20 Đường M, Khu TTHC Dĩ An, TP Dĩ An, Bình Dương. Cả 2 cơ sở đều được cấp phép hoạt động bởi Sở Y Tế. Website: https://nhakhoalinhxuan.com, Hotline: 0911.711.174. Thế mạnh: Chất lượng cao, Cam kết điều trị dứt điểm, Vô trùng chuẩn quốc tế, Bảo hành online, Đội ngũ bác sĩ giàu kinh nghiệm.Trang thiết bị hiện đại: Cone Beam CT 3D, iTero Element 5D, Laser, Piezotome, Medit Scan..."
                )},
                {"role": "user", "content": question}
            ]
        )

        answer = response['choices'][0]['message']['content']
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
 
