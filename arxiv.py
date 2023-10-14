import requests
from bs4 import BeautifulSoup
import time
import os
import platform
import subprocess
import pandas as pd

def fetch_links_from_arxiv(query, count="25"):  # 25,50,100,200
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    url = f"https://arxiv.org/search/cs?query={query}&searchtype=all&abstracts=show&order=-announced_date_first&size={count}"  # 最新的
    url = f"https://arxiv.org/search/?searchtype=all&query={query}&abstracts=show&size={count}&order=announced_date_first"  # 最老的
    url = f"https://arxiv.org/search/?searchtype=all&query={query}&abstracts=show&size={count}&order="  # 相关度最高的
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch the search page. Error: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(('https://arxiv.org/abs', 'https://arxiv.org/pdf'))]
    return links

def open_file(filename):
    """打开文件的函数"""
    if platform.system() == "Windows":
        os.startfile(filename)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", filename])
    elif platform.system() == "Linux":
        subprocess.Popen(["xdg-open", filename])
    else:
        print("Sorry, we don't support this operating system.")

def arxiv_fetch_and_save_to_excel_and_pdf(query):
    filename = query.replace(" ", "_") + ".xlsx"
    
    links = fetch_links_from_arxiv(query)
    unique_links = set(links)

    if not unique_links:
        print("No links fetched. Exiting...")
        return

    for link in unique_links:
        if link.startswith('https://arxiv.org/pdf'):
            print(f"Downloading PDF from: {link}")
            # Download the PDF
            download_pdf_from_link(link, query)

        elif link.startswith('https://arxiv.org/abs'):
            print(f"Fetching content from: {link}")
            info = fetch_info_from_arxiv(link)
            if info:
                save_to_excel(info, filename)
            else:
                print(f"Skipping {link} due to fetch error.")

        time.sleep(2)

    print(f"File saved as {filename}")
    open_file(filename) 

def download_pdf_from_link(link, query):
    if not os.path.exists(query):
        os.makedirs(query)
    pdf_link = link if link.endswith(".pdf") else link + ".pdf"
    pdf_name = pdf_link.split("/")[-1]
    
    try:
        response = requests.get(pdf_link, stream=True)
        with open(os.path.join(query, pdf_name), 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"Failed to download the PDF for {pdf_link}. Error: {e}")

def fetch_info_from_arxiv(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch the page. Error: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title
    title_tag = soup.find("h1", class_="title mathjax")
    title = title_tag.text.replace("Title:", "").strip() if title_tag else None

    # Extract authors
    authors_tag = soup.find("div", class_="authors")
    authors = ', '.join([a.text for a in authors_tag.find_all("a")]) if authors_tag else None
    
    # Extract abstract
    abstract_tag = soup.find("blockquote", class_="abstract mathjax")
    abstract = abstract_tag.text.replace("Abstract:", "").strip() if abstract_tag else None

    # Extract subjects
    subjects_tag = soup.find("td", class_="tablecell subjects")
    subjects = subjects_tag.text.strip() if subjects_tag else None

    return {
        "Title": title,
        "Authors": authors,
        "Abstract": abstract,
        "Subjects": subjects,
        "URL": url
    }

def save_to_excel(data, filename):
    # 创建一个 DataFrame 从提供的数据
    df_new = pd.DataFrame([data])

    # 检查文件是否存在
    if os.path.exists(filename):
        # 读取现有的数据
        df_old = pd.read_excel(filename)
        # 追加新数据
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    # 保存 DataFrame 到 Excel 文件
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    cambria_format = workbook.add_format({'font_name': 'Cambria'})
    worksheet.set_column('A:XFD', None, cambria_format)
    header_format = workbook.add_format({
        'font_name': 'Cambria',
        'bold': True,
        'border': 1
    })
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    writer.save()

    print(f"Data saved to {filename}")

if __name__ == '__main__':
    arxiv_fetch_and_save_to_excel_and_pdf("LLM")