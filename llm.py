import os
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from embedchain_setup import initialize_app

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
        # Use the Embedchain app to run the quer
        
        full_response = app_embedchain.query(request.query)
        answer = full_response.split('Answer:')[-1].strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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
