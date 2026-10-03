# Hoàng Yến – Đề xuất thiết kế trang chủ (bản 1)

## Bài toán khách đặt ra
- Màu đỏ thương hiệu dùng liên tục rất **nhức mắt** → cần dùng đỏ "có tâm".
- Thích **nền chìm** để bố cục có chiều sâu.
- Ưng ~70% phong cách **yanyen.vn** + style **tretruc** (menu ở giữa, banner SVG).
- Đây là **web bán hàng**, không phải web giới thiệu → phải giữ luồng mua hàng.

## Giải pháp

### 1. Hệ màu: đỏ chỉ là điểm nhấn
| Vai trò | Màu | Dùng ở đâu |
|---|---|---|
| Đỏ đô trầm (wine) | `#2e0b0e → #621820` | Hero, khối khách hàng, footer – mảng lớn nhưng tối, sang, không chói |
| Đỏ thương hiệu | `#9e1b22` | **Chỉ** nút "Gọi/Mua", giá tiền, badge "Bán chạy" |
| Vàng đồng | `#b48a45` | Nút chính, viền, icon, hoa văn – lấy từ viền logo |
| Kem / cát | `#fcf8f2` / `#f6eee2` | Nền đọc nội dung, xen kẽ từng section |

Tỷ lệ ước tính: ~70% kem, ~20% đỏ đô trầm, ~10% đỏ tươi + vàng. Mắt luôn có chỗ nghỉ.

### 2. Nền chìm 3 lớp (chiều sâu)
- Hoa văn **mây cát tường** vẽ bằng SVG, mờ 11% trên các section nền kem.
- Ảnh **chim yến bay vàng** (tài sản có sẵn của Hoàng Yến) mờ dần trên/dưới (mask), xen kẽ section nền cát.
- Quầng sáng vàng (radial glow) trong hero + khối quà biếu.

### 3. Lấy từ yanyen.vn (≈70%)
- Tiêu đề có nhãn nhỏ + tiêu đề gradient + hoa văn ngăn cách.
- Thẻ danh mục bo góc lệch (giống viền "khung tranh" của Ý An).
- Khối kể chuyện thương hiệu ghép ảnh + số liệu, khối "Vì sao chọn" logo ở giữa.
- Cảm giác cao cấp, cổ điển, nhiều khoảng thở.

### 4. Lấy từ tretruc
- **Logo ở giữa, menu chia hai bên**, header trong suốt mờ, thu nhỏ khi cuộn.
- **Banner có đường sóng SVG** (viền vàng) nối hero xuống nội dung; footer cũng mở bằng sóng.
- Nhãn "pill", tab sản phẩm dạng viên thuốc, nút bo tròn.

### 5. Giữ sức mạnh bán hàng (thứ treviet không có)
- Tab lọc sản phẩm: Yến chưng sẵn / Yến tổ / Set quà / Yến chưng tươi.
- Nút thêm giỏ trên mọi card + thông báo nhỏ, đếm giỏ hàng.
- "Bạn mua yến dành cho ai?", khối quà biếu doanh nghiệp, CTA tư vấn (Gọi / Zalo / Messenger).
- Mobile: thanh tác vụ cố định đáy (Trang chủ · Danh mục · **Gọi ngay** · Zalo · Giỏ hàng).

### 6. Typography
- Tiêu đề: **Playfair Display** (serif, sang, hợp "Yến Tiến Vua").
- Nội dung: **Be Vietnam Pro** (dễ đọc, dấu tiếng Việt chuẩn).
- Font tự host, có subset tiếng Việt.

## Tư vấn thêm (điểm mù thường gặp)
1. **Ảnh hero**: hero dùng lại bộ banner của web hiện tại (3 banner ngang cho máy tính, 2 banner vuông cho mobile), dạng slider tự chạy 5s, có chấm chuyển và đường sóng vàng ở đáy. Lưu ý: 2 banner "Tuyết Lam An" mang logo **Banan** (nhãn khác) – nên thay bằng banner mang thương hiệu Hoàng Yến.
2. **Nặng ảnh**: web cũ ~49 MB ảnh (PNG 2 MB/ảnh). Bản này đã nén còn ~7 MB → tải nhanh hơn rõ trên 4G.
3. **Lặp sản phẩm**: web cũ lặp cùng sản phẩm ở 4–5 khối. Bản này gom vào 1 khối có tab → trang ngắn hơn, dễ tìm hơn.
4. **Đánh giá thật**: nên bổ sung 3–5 review có tên + ảnh khách (hiện chỉ có ảnh sự kiện).
5. **Số liệu "40 sản phẩm / 63 tỉnh"** trong khối khách hàng là số minh họa – cần khách xác nhận.
6. Nhãn "Bộ sưu tập Tết" trong menu Cửa hàng là nội dung đề xuất – đổi theo chiến dịch.
