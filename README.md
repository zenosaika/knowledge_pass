# Knowledge Pass
### How Thammasat's Software Engineering Courses Align with Industry Needs

- [Release 2.0.0]  [https://neo-knowledgepass.fly.dev](https://neo-knowledgepass.fly.dev)
- [Release 1.0.0]  [https://knowledge-pass.fly.dev](https://knowledge-pass.fly.dev)

## WorkHeart : Team Members
- 6510742163 นางสาวศุภิสรา สีถาวร
- 6510742254 นายสรยุทธ์ อิงบุญ
- 6510742452 นายพีรภาส งอกผล
- 6510742502 นายภูรี เพ็ญหิรัญ
- 6510742510 นายมณฑิระ อินทร์น้อย

## v2.0.0 Logs
### Features
```
- เพิ่มฟังก์ชัน Learning Path Generation สำหรับแสดงแผนการเรียนเบื้องต้น
- เพิ่มฟังก์ชัน Skill Gap Alignment โดยใช้เทคนิค Retrieval Augmented Generation (RAG) สำหรับแนะนำการจัดเนื้อหาลงในวิชาที่เหมาะสม
- ทำให้หน้า Visualization มีการจัดลำดับงานที่เหมาะสมสำหรับแต่ละบุคคล
- ปรับปรุง Interface ให้ใช้งานสะดวกและตรงกับความต้องการของผู้ใช้มากขึ้น
- แบ่งหน้า homepage แยกสำหรับแต่ละฟังก์ชันหลักได้แก่ Personalized Job Recommendation, Learning Path Generation, Skill Gap Alignment
- มีการเพิ่มขั้นตอนในการทำ Graph Augmentation โดยการ augment taxonomy ของ Skill node เพื่อเพิ่ม Connectivity ใน Graph
- ปรับปรุง Admin Dashboard ให้สามารถจัดการกับข้อมูลใน Graph Database ได้ง่ายยิ่งขึ้น
```

### Installation
```
virtualvenv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Create Environment File (.env)
```
NEO4J_URI=
NEO4J_PASSWORD=
GOOGLE_API_KEY=
```

### Run Neo4j (Graph Database) in Docker
```
docker run \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_AUTH=neo4j/<your_password> \
    --volume=<path_to_mount_folder>:/data \
    neo4j:2025.03.0
```

### Run FastAPI
```
fastapi dev main.py --port 8081
```

### Previews
<video src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/v200_demo.mp4" controls></video><br>

## v1.2.0 Logs
### Features
```
- พัฒนาหน้า Interface ของ Admin Dashboard ให้มีความสวยงาม ใช้งานง่ายขึ้น
- ทำการเพิ่มฟังก์ชัน Add New Course และ Add New Job ให้สามารถใช้ได้ผ่านหน้า Admin Dashboard
- ทำให้หน้า Result Page (Visualization) มีความ Responsive ในหลายอุปกรณ์มากขึ้น
```
### Previews
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/more_responsive_v120.jpg"><br>
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/admin_dashboard_v120.png"><br>
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/add_new_job_v120.png"><br>

## v1.1.0 Logs
### Features
```
- เปลี่ยน LLM Model API จาก Gemini-1.5-Flash เป็น Gemini-2.0-Flash
- ทำการเพิ่มประสิทธิภาพ Optimize การค้นหาข้อมูลในกราฟ ให้มีจำนวน Query ที่ต้องเรียกใช้ลดลง ด้วยการเพิ่ม Self-Loop ไปยัง Root Skill
- เพิ่มหน้า Admin Dashboard สำหรับดูภาพรวมของ Node ใน Graph Database และใช่คำสั่ง Compile Graph
```
### Previews
<img src="https://github.com/zenosaika/knowledge_pass/blob/main/assets/admin_dashboard_v110.png"><br>

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