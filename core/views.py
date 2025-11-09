# core/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import DeCuong, HocVien
from .serializers import DeCuongSerializer, UserSerializer, HocVienSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
import os
from django.conf import settings
# Thêm các import cho AI
import google.generativeai as genai
from django.conf import settings
# ... (các import hiện có)
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
# --- API Đăng ký ---
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        # Tự động tạo HocVien khi User đăng ký
        HocVien.objects.create(user=user, ho_ten=request.data.get('ho_ten', 'Tên Mặc Định'))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- API Lấy và Cập nhật Đề cương ---
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated]) # Chỉ người đã đăng nhập mới được vào
def de_cuong_view(request):
    # Lấy đề cương của chính học viên đang đăng nhập
    hoc_vien = get_object_or_404(HocVien, user=request.user)
    
    # Dùng get_or_create để tự động tạo đề cương nếu chưa có
    de_cuong, created = DeCuong.objects.get_or_create(hoc_vien=hoc_vien)

    if request.method == 'GET':
        serializer = DeCuongSerializer(de_cuong)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Cập nhật đề cương với dữ liệu mới
        serializer = DeCuongSerializer(de_cuong, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- API Gợi ý AI ---
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def goi_y_ai(request):
    try:
        # Lấy nội dung người dùng gửi lên
        prompt_ngu_dung = request.data.get('prompt', '')
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Sửa tên model thành phiên bản chính xác
        model = genai.GenerativeModel('models/gemini-pro-latest') 
        
        # Tạo câu lệnh (prompt) tốt hơn
        full_prompt = (
            "Bạn là một trợ lý giáo sư chuyên về Lý luận và Phương pháp dạy học Sinh học."
            "Hãy đưa ra góp ý học thuật, ngắn gọn và mang tính xây dựng cho phần sau đây của một luận văn: \n\n"
            f"{prompt_ngu_dung}"
        )
        
        response = model.generate_content(full_prompt)
        return Response({'goi_y': response.text})
            
    except Exception as e:
        # Đây là phần chúng ta thêm vào để tìm lỗi
        print("================ LỖI GOOGLE AI ================") 
        print(e) 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def index(request):
    return render(request, 'core/index.html')
# ... (sau hàm goi_y_ai)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_pdf_view(request):
    try:
        # 1. Lấy dữ liệu
        hoc_vien = get_object_or_404(HocVien, user=request.user)
        de_cuong = get_object_or_404(DeCuong, hoc_vien=hoc_vien)

        # 2. Tạo context (dữ liệu để điền vào template)
        context = {
            'hoc_vien': hoc_vien,
            'ten_de_tai': de_cuong.ten_de_tai,
            'ly_do_chon_de_tai': de_cuong.ly_do_chon_de_tai,
            'khung_ly_thuyet': de_cuong.khung_ly_thuyet,
            'thiet_ke_va_to_chuc': de_cuong.thiet_ke_va_to_chuc,
            'thuc_nghiem': de_cuong.thuc_nghiem,
            'font_path': f'file://{os.path.join(settings.BASE_DIR, "static", "fonts", "DejaVuSans.ttf")}',
        }

        # 3. Render HTML từ template
        template = get_template('core/pdf_template.html')
        html = template.render(context)

        # 4. Tạo PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="DeCuongLuanVan.pdf"'
            return response

    except Exception as e:
        print(f"Lỗi tạo PDF: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Lỗi tạo PDF'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)