import cv2
import numpy as np
import imutils
from typing import Tuple, List, Dict
import time
import json

class LightBulbDetector:
    def __init__(self):
        self.camera = None
        self.is_camera_open = False
        self.detection_history = []
        self.debug_info = {}
        
    def open_camera(self, camera_index: int = 0) -> bool:
        """Open the camera for light detection"""
        try:
            self.camera = cv2.VideoCapture(camera_index)
            if self.camera.isOpened():
                self.is_camera_open = True
                return True
            else:
                print("Failed to open camera")
                return False
        except Exception as e:
            print(f"Error opening camera: {e}")
            return False
    
    def close_camera(self):
        """Close the camera"""
        if self.camera:
            self.camera.release()
        self.is_camera_open = False
    
    def analyze_frame_detailed(self, frame) -> Dict:
        """
        Detailed analysis of frame with step-by-step detection process
        Returns: Dictionary with detailed detection information
        """
        if frame is None:
            return {"error": "No frame provided"}
        
        # Store original frame dimensions
        height, width = frame.shape[:2]
        
        # Step 1: Convert to different color spaces for analysis
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Step 2: Calculate overall frame statistics
        frame_stats = {
            'dimensions': {'width': width, 'height': height},
            'total_pixels': width * height,
            'average_brightness': np.mean(gray),
            'brightness_std': np.std(gray),
            'max_brightness': np.max(gray),
            'min_brightness': np.min(gray)
        }
        
        # Step 3: HSV Analysis for light detection
        # Define multiple threshold ranges for different types of light
        thresholds = {
            'bright_white': {
                'lower': np.array([0, 0, 200]),
                'upper': np.array([180, 30, 255]),
                'description': 'Bright white light (high value, low saturation)'
            },
            'warm_light': {
                'lower': np.array([10, 50, 150]),
                'upper': np.array([25, 255, 255]),
                'description': 'Warm/yellow light (orange-yellow hue)'
            },
            'cool_light': {
                'lower': np.array([100, 50, 150]),
                'upper': np.array([130, 255, 255]),
                'description': 'Cool/blue light (blue hue)'
            }
        }
        
        # Step 4: Apply each threshold and analyze results
        threshold_results = {}
        for threshold_name, threshold_data in thresholds.items():
            mask = cv2.inRange(hsv, threshold_data['lower'], threshold_data['upper'])
            
            # Clean up mask with morphological operations
            kernel = np.ones((5, 5), np.uint8)
            mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)
            
            # Find contours in this threshold
            contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contours
            valid_contours = []
            total_area = 0
            total_brightness = 0
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 50:  # Filter out very small areas
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate brightness in this region
                    roi = gray[y:y+h, x:x+w]
                    if roi.size > 0:
                        brightness = np.mean(roi)
                        total_brightness += brightness
                        total_area += area
                        
                        # Calculate aspect ratio and circularity
                        aspect_ratio = w / h if h > 0 else 0
                        perimeter = cv2.arcLength(contour, True)
                        circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                        
                        # Determine if this looks like a light bulb
                        is_likely_bulb = (
                            area > 100 and  # Minimum size
                            brightness > 150 and  # Minimum brightness
                            (0.5 <= aspect_ratio <= 2.0) and  # Reasonable aspect ratio
                            circularity > 0.3  # Somewhat circular
                        )
                        
                        valid_contours.append({
                            'position': (x, y),
                            'size': (w, h),
                            'area': area,
                            'brightness': brightness,
                            'aspect_ratio': aspect_ratio,
                            'circularity': circularity,
                            'is_likely_bulb': is_likely_bulb,
                            'threshold_type': threshold_name
                        })
            
            threshold_results[threshold_name] = {
                'description': threshold_data['description'],
                'contours_found': len(contours),
                'valid_contours': len(valid_contours),
                'total_area': total_area,
                'total_brightness': total_brightness,
                'average_brightness': total_brightness / len(valid_contours) if valid_contours else 0,
                'contours': valid_contours
            }
        
        # Step 5: Overall analysis and decision making
        all_contours = []
        total_brightness_all = 0
        total_area_all = 0
        
        for threshold_name, result in threshold_results.items():
            all_contours.extend(result['contours'])
            total_brightness_all += result['total_brightness']
            total_area_all += result['total_area']
        
        # Step 6: Determine room lighting status
        # Calculate weighted score based on multiple factors
        brightness_score = frame_stats['average_brightness'] / 255.0  # Normalize to 0-1
        area_score = min(total_area_all / (width * height), 1.0)  # Normalize area coverage
        contour_score = min(len(all_contours) / 10.0, 1.0)  # Normalize contour count
        
        # Weighted decision making
        final_score = (brightness_score * 0.5 + area_score * 0.3 + contour_score * 0.2)
        
        if final_score > 0.6:
            room_status = "LIGHTS_ON"
            signal = "YES"
        elif final_score > 0.3:
            room_status = "PARTIAL_LIGHTING"
            signal = "PARTIAL"
        else:
            room_status = "LIGHTS_OFF"
            signal = "NO"
        
        # Step 7: Compile detailed results
        detailed_result = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'frame_analysis': frame_stats,
            'threshold_analysis': threshold_results,
            'detection_summary': {
                'total_contours_found': len(all_contours),
                'total_brightness': total_brightness_all,
                'total_area_covered': total_area_all,
                'area_percentage': (total_area_all / (width * height)) * 100,
                'decision_factors': {
                    'brightness_score': brightness_score,
                    'area_score': area_score,
                    'contour_score': contour_score,
                    'final_score': final_score
                }
            },
            'room_status': room_status,
            'signal': signal,
            'detected_light_sources': [
                {
                    'position': contour['position'],
                    'size': contour['size'],
                    'brightness': contour['brightness'],
                    'confidence': 'high' if contour['is_likely_bulb'] else 'medium',
                    'type': contour['threshold_type']
                }
                for contour in all_contours
            ]
        }
        
        # Store in history for debugging
        self.detection_history.append(detailed_result)
        if len(self.detection_history) > 10:  # Keep last 10 detections
            self.detection_history.pop(0)
        
        return detailed_result
    
    def detect_light_bulbs(self, frame) -> Dict:
        """
        Legacy method for backward compatibility
        """
        return self.analyze_frame_detailed(frame)
    
    def capture_and_analyze(self) -> Dict:
        """Capture a frame from camera and analyze for light bulbs"""
        if not self.is_camera_open or not self.camera:
            return {"error": "Camera not open"}
        
        ret, frame = self.camera.read()
        if not ret:
            return {"error": "Failed to capture frame"}
        
        # Analyze the frame with detailed information
        result = self.analyze_frame_detailed(frame)
        
        return result
    
    def get_camera_status(self) -> Dict:
        """Get current camera status"""
        return {
            'is_open': self.is_camera_open,
            'camera_index': 0 if self.camera else None
        }
    
    def get_detection_history(self) -> List[Dict]:
        """Get recent detection history for debugging"""
        return self.detection_history
    
    def get_debug_info(self) -> Dict:
        """Get current debug information"""
        return {
            'camera_status': self.get_camera_status(),
            'detection_history_count': len(self.detection_history),
            'last_detection': self.detection_history[-1] if self.detection_history else None
        }

# Example usage and testing
if __name__ == "__main__":
    detector = LightBulbDetector()
    
    if detector.open_camera():
        print("Camera opened successfully")
        
        # Wait a moment for camera to stabilize
        time.sleep(2)
        
        # Analyze lighting
        result = detector.capture_and_analyze()
        print("Detection result:", json.dumps(result, indent=2))
        
        detector.close_camera()
    else:
        print("Failed to open camera") 