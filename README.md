# วิธีใช้งาน 
 python -m venv venv 
 venv\Scripts\activate
 pip install -r requirements.txt
# 1. ดาวน์โหลดไฟล์
 ไปที่หน้า release:
 https://github.com/oschwartz10612/poppler-windows/releases/

 หาเวอร์ชัน poppler-24.08.0

 โหลดไฟล์เช่น
 poppler-24.08.0-0-x86_64.zip

 แตกไฟล์ zip ไปยังที่ที่ต้องการ เช่น
 C:\poppler-24.08.0
# 5. เพิ่ม Poppler เข้า PATH
 เพื่อให้ใช้คำสั่ง poppler ในโปรแกรม/terminal ได้สะดวก

# วิธีเพิ่ม PATH:

 Copy path ของโฟลเดอร์ C:\poppler-24.08.0\Library\bin

 กด Start > พิมพ์ Environment Variables

 เลือก Edit the system environment variables > Environment Variables…

 ในช่อง System variables หา Path > กด Edit

 กด New แล้ววาง path ที่ copy ไว้ (C:\poppler-24.08.0\Library\bin)

 กด OK ให้ครบทุกหน้าต่าง
