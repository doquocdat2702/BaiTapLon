import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
from datetime import datetime

def lay_tat_ca_cac_link_viec_lam():
    url = 'https://danang43.edu.vn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = set()

        for a in soup.find_all('a', {'href': True}):
            href = a.get('href')
            if href and ("tuyen-dung" in href or "viec-lam" in href):
                full_link = href if href.startswith("http") else "https://danang43.edu.vn/" + href
                links.add(full_link)

        all_links = list(links)
        print(f"Tìm thấy {len(all_links)} liên kết có thể chứa thông tin việc làm từ trang chủ.")
        return all_links

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi truy cập trang chủ: {e}")
        return []

def lay_thong_tin_chi_tiet_viec_lam(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        tieu_de_tag = soup.find('h1', class_='entry-title')
        tieu_de = tieu_de_tag.text.strip() if tieu_de_tag else ''

        mo_ta_tag = soup.find('meta', {'name': 'description'})
        mo_ta = mo_ta_tag['content'] if mo_ta_tag else ''
        if not mo_ta:
            mo_ta_element = soup.find('div', class_='entry-content')
            mo_ta = mo_ta_element.text.strip()[:200] + '...' if mo_ta_element else ''

        ten_cong_ty = ''
        muc_luong = ''
        dia_diem = ''
        noi_dung = ''

        company_tag = soup.find('span', class_='company')
        ten_cong_ty = company_tag.text.strip() if company_tag else ''

        salary_tag = soup.find('span', class_='salary')
        muc_luong = salary_tag.text.strip() if salary_tag else ''

        location_tag = soup.find('span', class_='location')
        dia_diem = location_tag.text.strip() if location_tag else ''

        content_elements = soup.select('.entry-content p')
        noi_dung_parts = [p.text.strip() for p in content_elements if p.text.strip()]
        noi_dung = "\n".join(noi_dung_parts)

        return {
            'Tiêu đề': tieu_de,
            'Mô tả': mo_ta,
            'Tên Công ty': ten_cong_ty,
            'Mức lương': muc_luong,
            'Địa điểm': dia_diem,
            'Nội dung': noi_dung,
            'Link': url
        }
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy thông tin việc làm từ {url}: {e}")
        return None
    except Exception as e:
        print(f"Lỗi xử lý trang việc làm từ {url}: {e}")
        return None

def thu_thap_va_luu_du_lieu_viec_lam():
    print(f"Bắt đầu thu thập dữ liệu việc làm lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tat_ca_link = lay_tat_ca_cac_link_viec_lam()
    du_lieu_viec_lam = []

    if not tat_ca_link:
        print("Không có liên kết việc làm nào để xử lý.")
        return

    for link in tat_ca_link:
        print(f"\nĐang xử lý trang việc làm từ: {link}")
        thong_tin_viec_lam = lay_thong_tin_chi_tiet_viec_lam(link)
        if thong_tin_viec_lam:
            print("--- Đã thu thập thông tin việc làm ---")
            print(f"Tiêu đề: {thong_tin_viec_lam['Tiêu đề']}")
            du_lieu_viec_lam.append(thong_tin_viec_lam)
        else:
            print(f"Không thể lấy thông tin chi tiết cho trang: {link}")

    if du_lieu_viec_lam:
        df = pd.DataFrame(du_lieu_viec_lam)
        file_name = f"vieclam_danang43_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"\nĐã lưu dữ liệu việc làm vào file: {file_name}")
    else:
        print("\nKhông có dữ liệu việc làm nào được thu thập để lưu.")

thu_thap_va_luu_du_lieu_viec_lam()
while True:
    schedule.run_pending()
    time.sleep(60)