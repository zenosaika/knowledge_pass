# Knowledge Pass
### How Thammasat's Software Engineering Courses Align with Industry Needs

- [Release 1.0.0]  [https://knowledge-pass.fly.dev](https://knowledge-pass.fly.dev)

## WorkHeart : Team Members
- 6510742163 นางสาวศุภิสรา สีถาวร
- 6510742254 นายสรยุทธ์ อิงบุญ
- 6510742452 นายพีรภาส งอกผล
- 6510742502 นายภูรี เพ็ญหิรัญ
- 6510742510 นายมณฑิระ อินทร์น้อย

## v1.0.0 Logs
- `KPFrontend` เป็นส่วน frontend ของระบบ โดยใช้ html, css, tailwind ในการพัฒนา และใช้ django ในการจัดการและควบคุม
- `KPBackend` เป็นส่วนโค้ด API และ test file ของฝั่ง backend ซึ่งใช้ FastAPI ในการทำ API สำหรับเรียกใช้ function ต่าง ๆ เช่น 
    - automated skill extraction
    - automated graph construction
    - search graph
    - compile graph
- `KPDatabase` ด้านในเก็บ docker-compose.yml ไว้สำหรับ start database services ได้แก่ 
    - Neo4j Graph Database
    - MongoDB No-SQL Database
- `frontend_test` เป็น folder ที่เก็บ test file สำหรับ frontend

### Features
```
- พัฒนาระบบ Visualization ที่สามารถแสดงข้อมูลที่ถูกดึงจากฐานข้อมูลได้อย่างถูกต้อง
- ปรับปรุงระบบแสดงผลของ Learning Path ให้แม่นยำขึ้นและรองรับการใช้งานตามแผนการเรียนของผู้ใช้
- พัฒนาฟังก์ชัน Data Extraction ให้สามารถสกัดข้อมูลได้อย่างแม่นยำถึง 80% ขึ้นไป
- เพิ่ม Interface สำหรับการค้นหาข้อมูลอาชีพ และการสืบค้นข้อมูลทักษะและรายวิชาในฐานข้อมูล
- ปรับปรุง User Experience (UX) เพื่อให้สามารถใช้งานบน Desktop Version ได้สมบูรณ์
```

### Instructions
```
# 1. Install Requirements

pip install -r requirements.txt


# 2. Deploy Neo4j & MongoDB on local

cd KPDatabase
docker-compose up -d

# 3. Run FastAPI on local

cd KPBackend
uvicorn main:app --reload --port 8081

# 4. Run Django on local

cd KPFrontend
python manage.py runserver

# 5. Go to http://127.0.0.1:8000
```

### Previews
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/v1_homepage.png"><br>
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/v1_result_page.png"><br>

## v0.3.0 Logs
- `AutomatePipeline.ipynb` เป็นไฟล์ notebook สำหรับการทำ information extraction, graph construction, search relation in graph database แบบอัตโนมัติ 

### Features
```
- ทำการทดสอบระบบ Matching Algorithm ให้มั่นใจได้ว่าการจับคู่ระหว่างทักษะและรายวิชามีความแม่นยำสูง
- พัฒนาระบบ Code-based Search ซึ่งช่วยให้ผู้ใช้สามารถค้นหาข้อมูลรายวิชาผ่านโค้ดของวิชาได้
- ตรวจสอบความถูกต้องของข้อมูลในฐานข้อมูล พร้อมปรับปรุงการประมวลผลให้มีประสิทธิภาพมากขึ้น
```

### Previews
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/automate_pipeline_result.png"><br>

## v0.2.0 Logs
- `visualizeD3` เป็น web app ซึ่งใช้ library `D3.js` ในการทำ visualization ความสัมพันธ์ระหว่าง course-job ที่ได้มาจากผลลัพธ์ของการทำ information extraction ด้วย llm

### Features
```
- ปรับปรุงระบบให้สามารถ แสดงผลการจับคู่ระหว่างทักษะและรายวิชาได้
- ออกแบบและพัฒนาโมเดลที่สามารถจับคู่ทักษะและรายวิชาได้อย่างเป็นระบบ โดยใช้ Machine Learning หรือ Rule-based Matching
- ปรับปรุง User Interface (UI) เพื่อให้ผู้ใช้งานสามารถเข้าถึงข้อมูลที่แมตช์กันได้ง่ายขึ้น
```

### Start The Server
~~~sh
npx http-server
~~~

### Previews
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/visualizeD3/previews/dense.png"><br>
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/visualizeD3/previews/lr.png"><br>
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/visualizeD3/previews/rl.png"><br>

## v0.1.0 Logs
- `preprocessed/sankey_course_mapping.csv` เป็นไฟล์ csv ที่แสดงถึงความสัมพันธ์ของรายวิชา กับงาน ซึ่งได้มาจากการ inference llm (by James)
- `raws/mappingCoursesAndCompany_AmplifyReasoning.json` เป็นผลลัพธ์การให้ llm ทำ course-job mapping โดยให้ amplify การให้เหตุผล (by James)
- `raws/*` เป็นไฟล์ข้อมูลดิบก่อนที่จะ preprocess ให้พร้อมใช้งาน

### Features
```
- พัฒนาและปรับปรุงระบบ Extraction Keyword โดยทำให้สามารถดึงคำสำคัญจากแหล่งข้อมูลต่าง ๆ ได้อย่างแม่นยำ
- ดำเนินการออกแบบโครงสร้างข้อมูลสำหรับ Graph Database เพื่อใช้ในการจัดเก็บข้อมูลที่ได้จากการสกัดคำสำคัญ
- วางรากฐานของการนำข้อมูลไปใช้ประโยชน์ในขั้นตอนถัดไป เช่น การวิเคราะห์ความสัมพันธ์ระหว่างทักษะและรายวิชา
```