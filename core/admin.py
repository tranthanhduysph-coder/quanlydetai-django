

# core/admin.py
from django.contrib import admin
from .models import CBHD, HocVien, DeCuong

# Đăng ký đơn giản
admin.site.register(CBHD)

# Tùy chỉnh cách hiển thị cho HocVien
@admin.register(HocVien)
class HocVienAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'ngay_sinh', 'que_quan')
    search_fields = ('ho_ten',)

# Tùy chỉnh cách hiển thị cho DeCuong
@admin.register(DeCuong)
class DeCuongAdmin(admin.ModelAdmin):
    list_display = ('hoc_vien', 'ten_de_tai', 'trang_thai')
    search_fields = ('ten_de_tai', 'hoc_vien__ho_ten')
    list_filter = ('trang_thai',)
