from fastapi import FastAPI, Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

import SibylSystem

app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Allow requests from this origin
    allow_credentials=True,  # Allow sending cookies and HTTP authentication
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)

def get_description(job_name, path):
    skills = path[:-1][::-1]
    description = 'เพราะวิชานี้สอน <i style="color:#CCCCFF;">'

    for skl in skills[:-1]:
        description += f'{skl.title()} -> ซึ่งเกี่ยวข้องกับ -> '
    description += f'{skills[-1].title()}</i> ซึ่ง require ในงาน <b style="color:rgb(116,238,21);">{job_name}</b>'
    
    return description

def get_sankey_data(paths):
    data = {}
    for path in paths:
        path = path[::-1]
        for i in range(len(path) - 1):
            k = (path[i], path[i+1])
            if k in data:
                data[k] += 1
            else:
                data[k] = 1

    sankey_data = []
    for k, v in data.items():
        sankey_data.append((k[0], k[1], v))

    return sankey_data


@app.get("/search")
async def search_jobs(q: Optional[str] = Query(None, description="Job title to retrieve")):
    if not q:
        return {"message": "No query provided"}

    obj = SibylSystem.inference(q)

    results = {}
    required_skills_checklist = {k:False for k in obj['required_skills']}

    to_be_print = []

    for path in obj['data']:
        course_name = path[-1]
        description = get_description(q, path)
        skill2 = path[0]
        if course_name in results:
            results[course_name].append(description)
        else:
            results[course_name] = [description]

        required_skills_checklist[skill2] = True

    to_be_print.append(f'<b style="font-size:large;">ผลการวิเคราะห์งาน</b>')
    to_be_print.append(f'<h2 style="color:rgb(116,238,21);">{q}</h2>')
    to_be_print.append(f'<b style="font-size:large;">ต้องการ Skills ที่เรียนได้จากวิชาดังต่อไปนี้ :</b><br>')

    for k, v in results.items():
        to_be_print.append(f'💠 <b>{k}</b>')
        to_be_print.append('<details><summary>ดูคำอธิบาย</summary>')
        for item in v:
            to_be_print.append(f'&nbsp;&nbsp;&nbsp;&nbsp;- {item}')
        to_be_print.append('</details>')

    to_be_print.append('<br><b style="font-size:large;">ความเกี่ยวข้องกับวิชาที่มีสอนในสาขา Soft-EN 💻 :</b><br>')
    for k, v in required_skills_checklist.items():
        to_be_print.append(f"&nbsp;&nbsp;&nbsp;&nbsp;{'🟩' if v else '⬛'}&nbsp;&nbsp;&nbsp;&nbsp;{'<b>' + k.title() + '</b>' if v else k.title()}")

    html_result = '<br>'.join(to_be_print)

    sankey_data = get_sankey_data(obj['data'])

    return {'html': [html_result], 'sankey_data': sankey_data}
    
@app.get("/compile_graph")
async def search_jobs():
    SibylSystem.compile_graph()
    return {"status": 200}

@app.get("/get_graph_info")
async def get_graph_info():
    n_job, n_course, n_skill = SibylSystem.get_graph_info()
    return {"n_job": n_job, "n_course": n_course, "n_skill": n_skill}

@app.get("/get_all_job")
async def get_all_job():
    jobs = SibylSystem.get_all_job()
    return jobs

@app.get("/")
async def root():
    return {"message": "Hello World"}