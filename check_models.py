import google.generativeai as genai

# ================================================================
# DÁN API KEY CỦA BẠN (key ...WYLs) VÀO ĐÂY
API_KEY = 'AIzaSyCi21kKIxKpoYT_pSsejCCbQ-FkiHVWYLs' 
# ================================================================

try:
    genai.configure(api_key=API_KEY)

    print("Đang tìm các model có sẵn cho key của bạn...")
    print("------------------------------------------")

    for m in genai.list_models():
        # Kiểm tra xem model có hỗ trợ 'generateContent' không
        if 'generateContent' in m.supported_generation_methods:
            print(f"TÊN MODEL: {m.name}")
            print(f"  Mô tả: {m.description}\n")

    print("------------------------------------------")
    print("Hãy chọn một 'TÊN MODEL' từ danh sách trên (ví dụ: 'models/gemini-pro')")
    print("Và dán tên đó vào tệp 'core/views.py'.")

except Exception as e:
    print(f"GẶP LỖI RỒI: {e}")
    print("Vui lòng kiểm tra lại API Key hoặc chắc chắn bạn đã bật 'Billing' (Thanh toán) cho dự án.")