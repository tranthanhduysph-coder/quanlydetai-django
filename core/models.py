# core/models.py
from django.db import models
from django.contrib.auth.models import User
class CBHD(models.Model):
    """Lưu trữ thông tin Cán bộ hướng dẫn (Giảng viên)"""
    ho_ten = models.CharField(max_length=255, unique=True)
    hoc_ham_hoc_vi = models.CharField(max_length=100, blank=True, help_text="Ví dụ: TS. hoặc PGS.TS.")
    
    def __str__(self):
        return f"{self.hoc_ham_hoc_vi} {self.ho_ten}"

    class Meta:
        verbose_name = "Cán bộ hướng dẫn"
        verbose_name_plural = "Cán bộ hướng dẫn"

class HocVien(models.Model):
    """Lưu trữ thông tin Học viên Cao học"""

    # Sau này, bạn sẽ liên kết cái này với một tài khoản User
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    
    ho_ten = models.CharField(max_length=255)
    ngay_sinh = models.DateField(null=True, blank=True)
    que_quan = models.CharField(max_length=255, blank=True)
    
    # Một học viên có thể có MỘT hoặc NHIỀU CBHD
    cbhd = models.ManyToManyField(CBHD, blank=True, related_name="hoc_vien_huong_dan")

    def __str__(self):
        return self.ho_ten

    class Meta:
        verbose_name = "Học viên"
        verbose_name_plural = "Danh sách Học viên"

class DeCuong(models.Model):
    """Lưu trữ thông tin chi tiết về Đề cương/Luận văn"""
    TRANG_THAI_CHOICES = [
        ('ban_nhap', 'Bản nháp'),
        ('da_nop', 'Đã nộp'),
        ('da_duyet', 'Đã duyệt'),
        ('can_chinh_sua', 'Cần chỉnh sửa'),
    ]

    # Mỗi học viên chỉ có MỘT đề cương
    hoc_vien = models.OneToOneField(HocVien, on_delete=models.CASCADE, primary_key=True)
    ten_de_tai = models.TextField()
    
    # Các phần nội dung đề cương
    ly_do_chon_de_tai = models.TextField(blank=True, null=True)
    khung_ly_thuyet = models.TextField(blank=True, null=True, verbose_name="Chương 1: Khung lý thuyết")
    thiet_ke_va_to_chuc = models.TextField(blank=True, null=True, verbose_name="Chương 2: Thiết kế/Tổ chức")
    thuc_nghiem = models.TextField(blank=True, null=True, verbose_name="Chương 3: Thực nghiệm")
    
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='ban_nhap')
    
    # Tệp đính kèm (sản phẩm)
    # file_san_pham = models.FileField(upload_to='san_pham/', null=True, blank=True)

    def __str__(self):
        return self.ten_de_tai

    class Meta:
        verbose_name = "Đề cương"
        verbose_name_plural = "Quản lý Đề cương"