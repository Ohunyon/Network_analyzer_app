import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import threading
import queue
import json
from typing import Optional
from datetime import datetime, timedelta

from packet_capture import PacketCapture
from predictor import NetworkPredictor

# Create static directory if it doesn't exist
static_dir = Path("static")
static_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Network Traffic Analyzer")

# Mount static files and reports directory
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
app.mount("/reports", StaticFiles(directory=str(reports_dir)), name="reports")

@app.get("/")
async def root():
    return FileResponse(str(static_dir / "index.html"))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for packet capture
packet_queue = queue.Queue()
stop_event = threading.Event()
capture_thread = None
predictor = NetworkPredictor()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("New WebSocket connection request")
    await websocket.accept()
    print("WebSocket connection accepted")
    
    try:
        while True:
            if not packet_queue.empty():
                try:
                    packet_info = packet_queue.get()
                    print(f"Processing packet: {packet_info}")
                    
                    prediction = predictor.predict_single(packet_info)
                    if prediction:
                        print(f"Prediction result: {prediction}")
                        await websocket.send_json(prediction)
                    else:
                        print("No prediction result")
                except Exception as e:
                    print(f"Error processing packet: {str(e)}")
                    # Continue processing next packet even if current one fails
                    continue
            else:
                # Small delay to prevent CPU overuse
                await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        print("WebSocket connection closed")
        try:
            await websocket.close()
        except:
            pass  # Connection might already be closed

@app.post("/start-capture")
async def start_capture():
    global capture_thread, stop_event
    
    if capture_thread and capture_thread.is_alive():
        raise HTTPException(status_code=400, detail="Capture already running")
    
    stop_event.clear()
    packet_capture = PacketCapture(packet_queue, stop_event)
    capture_thread = packet_capture.start_capture()
    
    return {"status": "Capture started"}

@app.post("/stop-capture")
async def stop_capture():
    global capture_thread, stop_event
    
    if not capture_thread or not capture_thread.is_alive():
        raise HTTPException(status_code=400, detail="No capture running")
    
    stop_event.set()
    capture_thread.join()
    capture_thread = None
    
    return {"status": "Capture stopped"}

@app.post("/generate-report")
async def generate_report(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
):
    try:
        # Convert string timestamps to datetime if provided
        start_dt = datetime.fromisoformat(start_time) if start_time else None
        end_dt = datetime.fromisoformat(end_time) if end_time else None
        
        report = predictor.generate_report(start_dt, end_dt)
        filepaths = predictor.save_report(report)
        
        # Convert file paths to URLs
        pdf_url = f"/reports/{os.path.basename(filepaths['pdf_path'])}"
        json_url = f"/reports/{os.path.basename(filepaths['json_path'])}"
        
        return JSONResponse({
            "status": "Report generated",
            "filepaths": {
                "pdf_path": pdf_url,
                "json_path": json_url
            },
            "report": report
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.post("/predict-csv")
async def predict_csv(csv_file: UploadFile = File(...)):
    try:
        content = await csv_file.read()
        df = pd.read_csv(pd.io.common.BytesIO(content))
        
        if "Destination" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'Destination' column")
        
        predictions_df = predictor.predict_batch(df)
        return predictions_df.to_dict(orient="records")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import asyncio
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
