# core/serializers.py
from rest_framework import serializers
from .models import DeCuong, HocVien
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class HocVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = HocVien
        fields = ['ho_ten', 'ngay_sinh', 'que_quan']

class DeCuongSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeCuong
        # Lấy tất cả các trường bạn đã định nghĩa
        fields = ['ten_de_tai', 'ly_do_chon_de_tai', 'khung_ly_thuyet', 'thiet_ke_va_to_chuc', 'thuc_nghiem', 'trang_thai']