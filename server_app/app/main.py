from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI, Request, UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, and_
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.responses import JSONResponse


app = FastAPI()

engine = create_engine('postgresql+psycopg2://postgres:postgres@db/postgres')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    ip_address = Column(String)
    http_method = Column(String)


class FirstTable(Base):
    __tablename__ = 'first_table'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    col1 = Column(Float)
    col2 = Column(Float)
    col3 = Column(Float)


class SecondTable(Base):
    __tablename__ = 'second_table'
    id = Column(Integer, primary_key=True)
    col1 = Column(Float)
    col2 = Column(Float)


class Data(BaseModel):
    id: int


def log_db(ip, http):
    timestamp = datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
    log = Log(timestamp=timestamp,
              ip_address=ip,
              http_method=http,
              )
    session = SessionLocal()
    session.add(log)
    session.commit()


@app.get("/endpoint1")
async def hello(request: Request):
    """
        Connection test function.
        Writes log into logs database
    """
    ip_address = request.client.host
    http_method = request.method + " test"
    log_db(ip_address, http_method)

    return {"message": "Hello. Test endpoint"}


@app.post("/endpoint2")
async def print_notes(request: Request, item: Data):
    ip_address = request.client.host
    http_method = request.method + " get_prediction"
    log_db(ip_address, http_method)

    idx = item.id
    if type(idx) != int:
        return {"error": "id is required"}
    
    session = SessionLocal()
    result = session.query(SecondTable.col1).filter(
        and_(SecondTable.id == idx)).all()

    return {"id": idx, "col1": result}



@app.post("/endpoint3")
async def load_dag(request: Request, file: UploadFile = File(...)):
    ip_address = request.client.host
    http_method = request.method + " load_dag"
    
    log_db(ip_address, http_method)
    if not file.filename.endswith('.py'):
        return JSONResponse(content={"error": "Invalid file extension"}, status_code=400)


    with open(f'/app/data/{file.filename}', 'wb') as out_file:
        content = await file.read()
        out_file.write(content) 

    return {"filename uploaded": file.filename}
