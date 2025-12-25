from flask import Flask, render_template, jsonify, request, Response
from light_detector import LightBulbDetector
import cv2
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)

# Global variables
detector = LightBulbDetector()
camera_thread = None
stop_camera = False
latest_result = None
debug_mode = True

def camera_worker():
    """Background thread for continuous camera monitoring"""
    global latest_result, stop_camera
    
    if not detector.open_camera():
        print("Failed to open camera in worker thread")
        return
    
    while not stop_camera:
        try:
            result = detector.capture_and_analyze()
            if 'error' not in result:
                latest_result = result
                if debug_mode:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Detection: {result['signal']} - Score: {result['detection_summary']['decision_factors']['final_score']:.3f}")
            time.sleep(1)  # Update every second
        except Exception as e:
            print(f"Error in camera worker: {e}")
            time.sleep(2)
    
    detector.close_camera()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/start_camera')
def start_camera():
    """Start the camera monitoring"""
    global camera_thread, stop_camera
    
    if camera_thread and camera_thread.is_alive():
        return jsonify({'status': 'Camera already running'})
    
    stop_camera = False
    camera_thread = threading.Thread(target=camera_worker)
    camera_thread.daemon = True
    camera_thread.start()
    
    return jsonify({'status': 'Camera started successfully'})

@app.route('/api/stop_camera')
def stop_camera_api():
    """Stop the camera monitoring"""
    global stop_camera
    
    stop_camera = True
    if camera_thread:
        camera_thread.join(timeout=2)
    
    return jsonify({'status': 'Camera stopped'})

@app.route('/api/status')
def get_status():
    """Get current camera and detection status"""
    global latest_result
    
    status = {
        'camera_status': detector.get_camera_status(),
        'latest_result': latest_result,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(status)

@app.route('/api/detect_once')
def detect_once():
    """Perform a single detection"""
    if not detector.is_camera_open:
        if not detector.open_camera():
            return jsonify({'error': 'Failed to open camera'})
    
    result = detector.capture_and_analyze()
    return jsonify(result)

@app.route('/api/camera_feed')
def camera_feed():
    """Stream camera feed"""
    def generate():
        if not detector.is_camera_open:
            if not detector.open_camera():
                yield b''
                return
        
        while True:
            ret, frame = detector.camera.read()
            if not ret:
                break
            
            # Resize frame for web streaming
            frame = cv2.resize(frame, (640, 480))
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/light_status')
def light_status():
    """Get current light status"""
    global latest_result
    
    if latest_result:
        return jsonify({
            'signal': latest_result.get('signal', 'UNKNOWN'),
            'room_status': latest_result.get('room_status', 'UNKNOWN'),
            'timestamp': latest_result.get('timestamp', ''),
            'detected_count': len(latest_result.get('detected_light_sources', [])),
            'decision_score': latest_result.get('detection_summary', {}).get('decision_factors', {}).get('final_score', 0)
        })
    else:
        return jsonify({
            'signal': 'UNKNOWN',
            'room_status': 'UNKNOWN',
            'timestamp': '',
            'detected_count': 0,
            'decision_score': 0
        })

@app.route('/api/debug_info')
def get_debug_info():
    """Get detailed debug information about the detection process"""
    global latest_result
    
    debug_data = {
        'camera_status': detector.get_camera_status(),
        'detection_history': detector.get_detection_history(),
        'latest_detection': latest_result,
        'system_info': {
            'timestamp': datetime.now().isoformat(),
            'debug_mode': debug_mode,
            'camera_thread_alive': camera_thread.is_alive() if camera_thread else False
        }
    }
    
    return jsonify(debug_data)

@app.route('/api/detection_details')
def get_detection_details():
    """Get detailed information about the latest detection"""
    global latest_result
    
    if not latest_result:
        return jsonify({'error': 'No detection data available'})
    
    # Extract key information for detailed view
    details = {
        'timestamp': latest_result.get('timestamp'),
        'final_decision': {
            'signal': latest_result.get('signal'),
            'room_status': latest_result.get('room_status')
        },
        'frame_analysis': latest_result.get('frame_analysis', {}),
        'threshold_analysis': latest_result.get('threshold_analysis', {}),
        'detection_summary': latest_result.get('detection_summary', {}),
        'detected_light_sources': latest_result.get('detected_light_sources', [])
    }
    
    return jsonify(details)

@app.route('/api/real_time_data')
def get_real_time_data():
    """Get real-time data for live monitoring"""
    global latest_result
    
    if not latest_result:
        return jsonify({'error': 'No data available'})
    
    # Extract real-time monitoring data
    real_time_data = {
        'timestamp': latest_result.get('timestamp'),
        'signal': latest_result.get('signal'),
        'room_status': latest_result.get('room_status'),
        'metrics': {
            'average_brightness': latest_result.get('frame_analysis', {}).get('average_brightness', 0),
            'total_contours': latest_result.get('detection_summary', {}).get('total_contours_found', 0),
            'area_coverage': latest_result.get('detection_summary', {}).get('area_percentage', 0),
            'decision_score': latest_result.get('detection_summary', {}).get('decision_factors', {}).get('final_score', 0)
        },
        'threshold_results': {
            name: {
                'contours_found': data.get('valid_contours', 0),
                'total_brightness': data.get('total_brightness', 0),
                'average_brightness': data.get('average_brightness', 0)
            }
            for name, data in latest_result.get('threshold_analysis', {}).items()
        }
    }
    
    return jsonify(real_time_data)

@app.route('/api/toggle_debug')
def toggle_debug():
    """Toggle debug mode on/off"""
    global debug_mode
    debug_mode = not debug_mode
    return jsonify({
        'debug_mode': debug_mode,
        'status': f'Debug mode {"enabled" if debug_mode else "disabled"}'
    })

if __name__ == '__main__':
    try:
        print("Starting Light Bulb Detection Web Application...")
        print("Access the application at: http://localhost:5000")
        print("Debug mode is enabled by default")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_camera = True
        if camera_thread:
            camera_thread.join(timeout=2)
        detector.close_camera()
    except Exception as e:
        print(f"Error starting application: {e}")
        detector.close_camera() 