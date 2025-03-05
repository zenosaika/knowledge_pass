# Connecting the Dots
### How Thammasat's Software Engineering Courses Align with Industry Needs

## v0.3.0 Logs
- `AutomatePipeline.ipynb` เป็นไฟล์ notebook สำหรับการทำ information extraction, graph construction, search relation in graph database แบบอัตโนมัติ 

## v0.2.0 Logs
- `visualizeD3` เป็น web app ซึ่งใช้ library `D3.js` ในการทำ visualization ความสัมพันธ์ระหว่าง course-job ที่ได้มาจากผลลัพธ์ของการทำ information extraction ด้วย llm

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