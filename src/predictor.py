import joblib
import pandas as pd
from datetime import datetime
import json
import os
from pdf_report import PDFReportGenerator

class NetworkPredictor:
    def __init__(self, model_path="model/my_model.pkl"):
        self.model = joblib.load(model_path)
        self.predictions_history = []
        
    def predict_single(self, packet_info):
        try:
            # Extract destination and create a pandas Series
            destination = pd.Series([packet_info['Destination']])
            
            # Make prediction using the Series directly
            # Convert prediction to numeric (0 or 1)
            raw_prediction = self.model.predict(destination)[0]
            prediction = 1 if str(raw_prediction).lower() == 'malicious' else 0
            
            # Store prediction with timestamp
            prediction_record = {
                'timestamp': packet_info['Timestamp'],
                'destination': packet_info['Destination'],
                'prediction': prediction,
                'source': packet_info['Source'],
                'protocol': packet_info['Protocol']
            }
            self.predictions_history.append(prediction_record)
            
            return prediction_record
        except Exception as e:
            print(f"Error predicting packet: {str(e)}")
            return None
            
    def predict_batch(self, df):
        try:
            # Extract the Destination column as a Series
            if 'Destination' not in df.columns:
                raise ValueError("DataFrame must contain 'Destination' column")
            
            # Make predictions and convert to numeric
            raw_predictions = self.model.predict(df['Destination'])
            df['prediction'] = [1 if str(p).lower() == 'malicious' else 0 for p in raw_predictions]
            return df
        except Exception as e:
            print(f"Error in batch prediction: {str(e)}")
            return None
        
    def generate_report(self, start_time=None, end_time=None):
        df = pd.DataFrame(self.predictions_history)
        
        if start_time and end_time:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            mask = (df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)
            df = df[mask]
            
        # Generate summary statistics
        total_packets = len(df)
        malicious_packets = len(df[df['prediction'] == 1])
        benign_packets = total_packets - malicious_packets
        
        # Group by source IP to find top sources of malicious traffic
        malicious_sources = df[df['prediction'] == 1]['source'].value_counts().head(5).to_dict()
        
        report = {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'period': {
                'start': start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else 'All time',
                'end': end_time.strftime('%Y-%m-%d %H:%M:%S') if end_time else 'All time'
            },
            'summary': {
                'total_packets': total_packets,
                'malicious_packets': malicious_packets,
                'benign_packets': benign_packets,
                'malicious_percentage': (malicious_packets / total_packets * 100) if total_packets > 0 else 0
            },
            'top_malicious_sources': malicious_sources
        }
        
        return report
        
    def save_report(self, report, filename=None):
        os.makedirs('reports', exist_ok=True)
        
        # Save JSON report
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_filename = f"report_{timestamp}.json"
            pdf_filename = f"report_{timestamp}.pdf"
        else:
            base_name = os.path.splitext(filename)[0]
            json_filename = f"{base_name}.json"
            pdf_filename = f"{base_name}.pdf"
            
        json_filepath = os.path.join('reports', json_filename)
        pdf_filepath = os.path.join('reports', pdf_filename)
        
        # Save JSON version
        with open(json_filepath, 'w') as f:
            json.dump(report, f, indent=4)
        
        # Generate PDF version
        pdf_generator = PDFReportGenerator()
        pdf_generator.generate_pdf(report, pdf_filepath)
        
        return {
            'json_path': json_filepath,
            'pdf_path': pdf_filepath
        }
