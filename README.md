# Scraper Thông Tin Việc Làm

## Mô tả

Đoạn code Python này được thiết kế để thu thập thông tin về các vị trí việc làm từ trang web [danang43.edu.vn](https://danang43.edu.vn/). Nó thực hiện các bước sau:

1.  **Lấy danh sách các liên kết việc làm:** Bắt đầu bằng cách truy cập trang chủ và tìm tất cả các liên kết có thể dẫn đến các trang chi tiết về việc làm (ví dụ: các trang có chứa "tuyen-dung" hoặc "viec-lam").
2.  **Trích xuất thông tin chi tiết:** Tiếp theo, đối với mỗi liên kết được tìm thấy, code sẽ truy cập trang đó và trích xuất các thông tin liên quan như tiêu đề công việc, mô tả, tên công ty, mức lương, địa điểm và nội dung chi tiết.
3.  **Lưu dữ liệu vào file CSV:** Cuối cùng, tất cả thông tin được thu thập sẽ được lưu vào một file CSV, với mỗi hàng đại diện cho một vị trí việc làm.  Tên của file CSV sẽ bao gồm dấu thời gian để đảm bảo không bị ghi đè.
4.  **Lên lịch thu thập dữ liệu (tùy chọn):** Code cũng có thể được lên lịch để chạy định kỳ, ví dụ: hàng ngày vào một thời điểm cụ thể.

## Các hàm chính

* `lay_tat_ca_cac_link_viec_lam()`:  Hàm này chịu trách nhiệm truy cập trang chủ và tìm tất cả các liên kết có thể dẫn đến các trang chi tiết về việc làm.
* `lay_thong_tin_chi_tiet_viec_lam(url)`:  Hàm này lấy URL của một trang chi tiết việc làm và trích xuất thông tin liên quan từ trang đó.
* `thu_thap_va_luu_du_lieu_viec_lam()`:  Hàm này điều phối toàn bộ quá trình thu thập dữ liệu.  Nó gọi hàm để lấy danh sách các liên kết, sau đó lặp qua từng liên kết để lấy thông tin chi tiết và cuối cùng lưu trữ dữ liệu vào một file CSV.

## Cách sử dụng

1.  **Cài đặt các thư viện cần thiết:** Đảm bảo bạn đã cài đặt các thư viện `requests`, `beautifulsoup4`, `pandas`, `schedule` và `time`. Bạn có thể cài đặt chúng bằng pip:
    ```
    pip install requests beautifulsoup4 pandas schedule
    ```
2.  **Chạy script:** Chạy script Python.  Nó sẽ thu thập dữ liệu việc làm và lưu vào một file CSV.  Nếu bạn đã bỏ ghi chú phần lên lịch, nó sẽ tiếp tục chạy theo lịch trình đó.

## Cấu trúc file

Đầu ra của script là một file CSV chứa các cột sau:

* Tiêu đề: Tiêu đề của vị trí việc làm.
* Mô tả: Mô tả ngắn gọn về công việc.
* Tên Công ty: Tên của công ty tuyển dụng.
* Mức lương: Mức lương được cung cấp.
* Địa điểm: Địa điểm làm việc.
* Nội dung: Mô tả chi tiết về công việc.
* Link: URL của trang chi tiết việc làm.

## Lên lịch

Bạn có thể sử dụng thư viện `schedule` để lên lịch chạy script này định kỳ.  Ví dụ: để chạy nó hàng ngày vào lúc 6:00 sáng và 12:00 trưa, bạn có thể bỏ ghi chú các dòng sau:

```python
# schedule.every().day.at("06:00").do(thu_thap_va_luu_du_lieu_viec_lam)
# schedule.every().day.at("12:00").do(thu_thap_va_luu_du_lieu_viec_lam)
# print("Đang chờ đến 6h sáng và 12h trưa mỗi ngày để thu thập dữ liệu việc làm...")
```

Đoạn code này sẽ lên lịch cho hàm `thu_thap_va_luu_du_lieu_viec_lam` chạy vào thời gian đã chỉ định.  Vòng lặp `while True` ở cuối script là cần thiết để `schedule` có thể kiểm tra và chạy các công việc đã lên lịch.
