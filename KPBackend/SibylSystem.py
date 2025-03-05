import os
from dotenv import load_dotenv
import google.generativeai as genai

import mimetypes
import time
import json

from neo4j import GraphDatabase
from tqdm.auto import tqdm
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()


# Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)


# Neo4j connection
uri = os.getenv("NEO4J_URI")
auth = ("neo4j", os.getenv("NEO4J_PASSWORD"))


# MongoDB Connection
MONGO_URI = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"

try:
    client = MongoClient(MONGO_URI)
    db = client["KPDatabase"]
    db.command("ping")
    collection = db["compiled_graph"]
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()  # Exit if connection fails


def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  if mime_type is None:
    mime_type, _ = mimetypes.guess_type(path)
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file


def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(5)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()


def extract_skill_from_text(text):
  chat_session = model.start_chat(history=[])

  response = chat_session.send_message([
                text,
                "extract skills (just keyword not detail such as \"proficiency in ...\") into python list",
                "example output :\n",
                "```json\n",
                "{\"skills\": [\"NET CORE\", \"ASP.NET CORE MVC framework\", \"C#\", \"object-oriented programming\", \"reusable libraries\", \"Web API\", \"Web Service\", \"JSON\", \"Microsoft SQL Server 2022\", \"TypeScript\", \"CSS\", \"SCSS\", \"HTML\", \"Angular framework\", \"npm\", \"Yarn\", \"Webpack\", \"CQRS pattern\", \"Visual Studio\", \"Azure DevOps\", \"English language\"]}",
                "\n```",
            ])

  return json.loads(response.text)


def extract_skill_from_image(image_path):
  image = upload_to_gemini(image_path)
  wait_for_files_active([image])

  chat_session = model.start_chat(history=[])

  response = chat_session.send_message([
                image,
                "extract skills (just keyword not detail such as \"proficiency in ...\") into python list",
                "example output :\n",
                "```json\n",
                "{\"skills\": [\"NET CORE\", \"ASP.NET CORE MVC framework\", \"C#\", \"object-oriented programming\", \"reusable libraries\", \"Web API\", \"Web Service\", \"JSON\", \"Microsoft SQL Server 2022\", \"TypeScript\", \"CSS\", \"SCSS\", \"HTML\", \"Angular framework\", \"npm\", \"Yarn\", \"Webpack\", \"CQRS pattern\", \"Visual Studio\", \"Azure DevOps\", \"English language\"]}",
                "\n```",
            ])

  return json.loads(response.text)


def extract_skill_from_pdf(pdf_path):
  pdf = upload_to_gemini(pdf_path)
  wait_for_files_active([pdf])

  chat_session = model.start_chat(history=[])

  response = chat_session.send_message([
                pdf,
                "extract skills (just keyword not detail such as \"proficiency in ...\") into python list",
                "example output :\n",
                "```json\n",
                "{\"skills\": [\"NET CORE\", \"ASP.NET CORE MVC framework\", \"C#\", \"object-oriented programming\", \"reusable libraries\", \"Web API\", \"Web Service\", \"JSON\", \"Microsoft SQL Server 2022\", \"TypeScript\", \"CSS\", \"SCSS\", \"HTML\", \"Angular framework\", \"npm\", \"Yarn\", \"Webpack\", \"CQRS pattern\", \"Visual Studio\", \"Azure DevOps\", \"English language\"]}",
                "\n```",
            ])

  return json.loads(response.text)


def merge_triple(tx, subject, predicate, object, subject_type, object_type):
  tx.run(
        f"MERGE (s:{subject_type} {{name: $subject}}) "
        f"MERGE (o:{object_type} {{name: $object}}) "
        f"MERGE (s)-[:{predicate}]->(o)",
        subject=subject,
        object=object
    )


def get_synonyms(word):
  chat_session = model.start_chat(history=[
      {
        "role": "user",
        "parts": [
          "Give me a Python list of terms related to \"css\" (in software engineering and tech domain) only synonyms, abbreviations, and the full name. all lowercase.",
        ],
      },
      {
        "role": "model",
        "parts": [
          "```json\n",
          "{\"related_terms\": [\"css\", \"cascading style sheets\", \"style sheets\", \"css3\", \"web styles\", \"stylesheet language\"]}",
          "\n```",
        ],
      },
  ])

  response = chat_session.send_message([
                f"Give me a Python list of terms related to \"{word}\" (in software engineering and tech domain) only synonyms, abbreviations, and the full name. all lowercase."
            ])


  return json.loads(response.text)


def add_new_skill(skill_name):
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      # link the skill with related term nodes
      llm_response = get_synonyms(skill_name)
      print(f'LLM: Related Terms of "{skill_name}" :\n')

      if 'related_terms' in llm_response:
        related_terms = llm_response['related_terms']
      else:
        related_terms = llm_response[list(llm_response.keys())[0]]

      for term in tqdm(related_terms, desc=f'Merge related terms of "{skill_name}"'):

        term = term.lower()

        session.execute_write(merge_triple,
                                  subject=term,
                                  predicate='relate',
                                  object=skill_name,
                                  subject_type='Skill',
                                  object_type='Skill')


def check_skill_existence(tx, skill_name):
  result = tx.run("MATCH (s:Skill {name: $skill_name}) RETURN s", skill_name=skill_name)
  return result.single() is not None


def skill_exists(skill_name):
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      result = session.execute_read(check_skill_existence, skill_name)
      return result


def add_new_course(course_name, skills):
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      for skill in tqdm(skills, desc=f'Merge Included Skills of "{course_name}"'):

        skill = skill.lower()

        if not skill_exists(skill):
          add_new_skill(skill)

        session.execute_write(merge_triple,
                                  subject=course_name,
                                  predicate='include',
                                  object=skill,
                                  subject_type='Course',
                                  object_type='Skill')


def add_new_job(job_name, skills):
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      for skill in tqdm(skills, desc=f'Merge Required Skills of "{job_name}"'):

        skill = skill.lower()

        if not skill_exists(skill):
          add_new_skill(skill)

        session.execute_write(merge_triple,
                                  subject=job_name,
                                  predicate='require',
                                  object=skill,
                                  subject_type='Job',
                                  object_type='Skill')
        

def find_course_job_paths(job_name):
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      result = session.execute_read(_find_course_job_paths, job_name)
      return result

def _find_course_job_paths(tx, job_name):
  query = (
      "MATCH (course:Course)-[:include]->(skill3:Skill)-[:relate]->(skill1:Skill)<-[:relate]-(skill2:Skill)<-[:require]-(job:Job {name: $job_name}) "
      "RETURN course, skill3, skill1, skill2, job"
  )
  result = tx.run(query, job_name=job_name)
  return [record for record in result]

def find_course_job_paths2(job_name):
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      result = session.execute_read(_find_course_job_paths2, job_name)
      return result

def _find_course_job_paths2(tx, job_name):
  query = (
      "MATCH (course:Course)-[:include]->(skill1:Skill)<-[:require]-(job:Job {name: $job_name}) "
      "RETURN course, skill1, job"
  )
  result = tx.run(query, job_name=job_name)
  return [record for record in result]


def describe_course_job_path(path):
  course_name = path["course"]["name"]
  skill3 = path["skill3"]["name"]
  skill1 = path["skill1"]["name"]
  skill2 = path["skill2"]["name"]
  job_name = path["job"]["name"]

  if skill3 == skill1 == skill2:
    description = f'เพราะวิชานี้สอน <i style="color:#CCCCFF;">{skill3.title()}</i> ซึ่ง require ในงาน <b style="color:rgb(116,238,21);">{job_name}</b>'
  elif skill3 == skill1:
    description = f'เพราะวิชานี้สอน <i style="color:#CCCCFF;">{skill3.title()} -> ซึ่งเกี่ยวข้องกับ -> {skill2.title()}</i> ซึ่ง require ในงาน <b style="color:rgb(116,238,21);">{job_name}</b>'
  elif skill1 == skill2:
    description = f'เพราะวิชานี้สอน <i style="color:#CCCCFF;">{skill3.title()} -> ซึ่งเกี่ยวข้องกับ -> {skill2.title()}</i> ซึ่ง require ในงาน <b style="color:rgb(116,238,21);">{job_name}</b>'
  else:
    description = f'เพราะวิชานี้สอน <i style="color:#CCCCFF;">{skill3.title()} -> ซึ่งเกี่ยวข้องกับ -> {skill1.title()} -> ซึ่งเกี่ยวข้องกับ -> {skill2.title()}</i> ซึ่ง require ในงาน <b style="color:rgb(116,238,21);">{job_name}</b>'

  return course_name, description, skill2

def describe_course_job_path2(path):
  course_name = path["course"]["name"]
  skill1 = path["skill1"]["name"]
  job_name = path["job"]["name"]

  description = f'เพราะวิชานี้สอน <i style="color:#CCCCFF;">{skill1.title()}</i> ซึ่ง require ในงาน <b style="color:rgb(116,238,21);">{job_name}</b>'

  return course_name, description, skill1


def get_all_required_skills(job_name):
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      result = session.execute_read(_get_all_required_skills, job_name)
      return result

def _get_all_required_skills(tx, job_name):
  query = (
      "MATCH (job:Job {name: $job_name})-[:require]->(skill:Skill) "
      "RETURN skill"
  )
  result = tx.run(query, job_name=job_name)
  return [record['skill']['name'] for record in result]


def inference(job_name):
  results = list(collection.find({"job_name": job_name}))
  return results[0]


def getalljob():
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      result = session.execute_read(_getalljob)
      return result
    

def _getalljob(tx):
  query = (
      "MATCH (job:Job) RETURN job"
  )
  result = tx.run(query)
  return [record['job']['name'] for record in result]


def compile_graph():
  job_names = getalljob()
  for job_name in job_names:
    paths = find_course_job_paths(job_name)
    data = set()
    for path in paths:
      skill2 = path["skill2"]["name"]
      skill1 = path["skill1"]["name"]
      skill3 = path["skill3"]["name"]
      course_name = path["course"]["name"]
      if skill2 != skill1 != skill3:
        data.add((skill2, skill1, skill3, course_name))
      elif skill1 == skill2 or skill1 == skill3:
        data.add((skill2, skill3, course_name))
      elif skill2 == skill3:
        data.add((skill2, course_name))
      else:
        print('Warning: Unhandled case', skill2, skill1, skill3)

    # Convert the set of tuples to a list of lists for MongoDB
    data = list(data)  # Convert the set to a list

    required_skills = get_all_required_skills(job_name)

    # Store in MongoDB
    job_data = {
        "job_name": job_name,  # Use "job_name" as the key
        "data": data, # Store the list of tuples
        "required_skills": required_skills
    }

    try:
        result = collection.replace_one(  # Use replace_one for upsert
            {"job_name": job_name},  # Query to find the document by job_name
            job_data,               # The new data to insert or update
            upsert=True             # Set upsert to True
        )

        if result.modified_count > 0:
            print(f"Data for job '{job_name}' updated.")
        elif result.upserted_id:
            print(f"Data for job '{job_name}' inserted with ID: {result.upserted_id}")
        else:
          print(f"Data for job '{job_name}' not modified")

    except Exception as e:
        print(f"Error inserting/updating data for job '{job_name}': {e}")


def get_graph_info():
  with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
      n_job = session.execute_read(_get_graph_info, 'Job')
      n_course = session.execute_read(_get_graph_info, 'Course')
      n_skill = session.execute_read(_get_graph_info, 'Skill')
      return n_job, n_course, n_skill
    
def _get_graph_info(tx, node_type):
  query = (
      f"MATCH (n:{node_type}) RETURN n"
  )
  result = tx.run(query)
  return len(list(result))


def get_all_job():
  all_keys = collection.distinct("job_name")  # Get all unique job names
  return all_keys