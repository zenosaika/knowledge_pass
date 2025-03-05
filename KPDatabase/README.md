# KnowledgePass

### 1. Install Requirements
```
pip install -r requirements.txt
```

### 2. Deploy Neo4j & MongoDB on local
```
cd KPDatabase
docker-compose up -d
```

### 3. Run FastAPI on local
```
cd KPBackend
uvicorn main:app --reload --port 8081
```

### 4. Run Django on local
```
cd KPFrontend
python manage.py runserver
```

### 5. Go to [http://127.0.0.1:8000](http://127.0.0.1:8000)