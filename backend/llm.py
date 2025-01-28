import os
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from embedchain_setup import initialize_app
import logging

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Initialize the Embedchain app
app_embedchain = initialize_app()

# Create FastAPI app
app = FastAPI()

# Define the request body model
class QueryRequest(BaseModel):
    query: str

# Define the FastAPI route for querying
@app.post("/query")
async def query_app(request: QueryRequest):
    try:
        logger.info(f"Received query: {request.query}")
        response = app_embedchain.query(input_query=request.query)
        logger.info(f"Response: {response}")
        return {"answer": response.split('Answer:')[-1].strip()}
    except Exception as e:
        logger.error(f"Query error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query error: {e}")
# Define the FastAPI route for uploading files to ChromaDB
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"./data/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Check the file extension to determine its type
        if file.filename.endswith('.pdf'):
            data_type = "pdf_file"
        elif file.filename.endswith('.csv'):
            data_type = "csv"
        elif file.filename.endswith('.json'):
            data_type= "json"

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and CSV files are supported.")
        
        # Add the file to Embedchain's ChromaDB
        app_embedchain.add(temp_file_path, data_type=data_type)
        
        return {"message": "File uploaded and added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Close the file and delete the temporary file
        file.file.close()
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# Run the FastAPI app using Uvicorn if needed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
