import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import schedule
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def lay_thong_tin_chi_tiet_viec_lam(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')

        tieu_de_tag = soup.find('h1', class_='entry-title')
        tieu_de = tieu_de_tag.text.strip() if tieu_de_tag else 'Không có tiêu đề'

        mo_ta_tag = soup.find('meta', {'name': 'description'})
        mo_ta = mo_ta_tag['content'] if mo_ta_tag else ''
        if not mo_ta:
            mo_ta_element = soup.find('div', class_='entry-content')
            mo_ta = mo_ta_element.text.strip()[:200] + '...' if mo_ta_element else 'Không có mô tả'

        ten_cong_ty = ''
        muc_luong = ''
        dia_diem = ''
        noi_dung = ''

        company_tag = soup.find('span', class_='company')
        ten_cong_ty = company_tag.text.strip() if company_tag else 'Không có tên công ty'

        salary_tag = soup.find('span', class_='salary')
        muc_luong = salary_tag.text.strip() if salary_tag else 'Không có mức lương'

        location_tag = soup.find('span', class_='location')
        dia_diem = location_tag.text.strip() if location_tag else 'Không có địa điểm'

        content_elements = soup.select('.entry-content p')
        noi_dung_parts = [p.text.strip() for p in content_elements if p.text.strip()]
        noi_dung = "\n".join(noi_dung_parts) if noi_dung_parts else "Không có nội dung"

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
        logging.error(f"Lỗi khi lấy thông tin việc làm từ {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Lỗi xử lý trang việc làm từ {url}: {e}")
        return None

def lay_tat_ca_cac_link_viec_lam():
    url = 'https://danang43.edu.vn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        for a in soup.find_all('a', {'href': True}):
            href = a.get('href')
            if href and ("tuyen-dung" in href or "viec-lam" in href or "tuyen-dung-viec-lam" in href): 
                full_link = href if href.startswith("http") else "https://danang43.edu.vn/" + href
                links.add(full_link)

        all_links = list(links)
        logging.info(f"Tìm thấy {len(all_links)} liên kết có thể chứa thông tin việc làm từ trang chủ danang43.edu.vn.")
        return all_links

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi khi truy cập trang chủ danang43.edu.vn: {e}")
        return []
    except Exception as e:
        logging.error(f"Lỗi không mong muốn: {e}")
        return []

def thu_thap_va_luu_du_lieu_viec_lam():
    logging.info(f"Bắt đầu thu thập dữ liệu việc làm từ danang43.edu.vn lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tat_ca_link = lay_tat_ca_cac_link_viec_lam()
    du_lieu_viec_lam = []

    if not tat_ca_link:
        logging.info("Không có liên kết việc làm nào để xử lý từ danang43.edu.vn.")
        return

    for link in tat_ca_link:
        logging.info(f"\nĐang xử lý trang việc làm từ: {link}")
        thong_tin_viec_lam = lay_thong_tin_chi_tiet_viec_lam(link)
        if thong_tin_viec_lam:
            logging.info("--- Đã thu thập thông tin việc làm ---")
            logging.info(f"Tiêu đề: {thong_tin_viec_lam['Tiêu đề']}")
            du_lieu_viec_lam.append(thong_tin_viec_lam)
        else:
            logging.warning(f"Không thể lấy thông tin chi tiết cho trang: {link}")

    if du_lieu_viec_lam:
        df = pd.DataFrame(du_lieu_viec_lam)
        file_name = f"vieclam_danang43_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        logging.info(f"\nĐã lưu dữ liệu việc làm từ danang43.edu.vn vào file: {file_name}")
    else:
        logging.info("\nKhông có dữ liệu việc làm nào được thu thập từ danang43.edu.vn để lưu.")

if __name__ == "__main__":
    thu_thap_va_luu_du_lieu_viec_lam()
    schedule.every().day.at("06:00").do(thu_thap_va_luu_du_lieu_viec_lam)
    logging.info("Đã lên lịch thu thập dữ liệu việc làm từ danang43.edu.vn hàng ngày vào lúc 06:00 sáng.")

    while True:
        schedule.run_pending()
        time.sleep(60)
