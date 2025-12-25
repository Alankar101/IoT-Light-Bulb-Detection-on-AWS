#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced light bulb detection system
Shows real-time backend detection process
"""

import cv2
import time
import json
from light_detector import LightBulbDetector

def test_detection_system():
    """Test the enhanced detection system with detailed output"""
    print("🔍 Enhanced Light Bulb Detection System Test")
    print("=" * 60)
    
    # Initialize detector
    detector = LightBulbDetector()
    
    # Open camera
    print("📹 Opening camera...")
    if not detector.open_camera():
        print("❌ Failed to open camera")
        return
    
    print("✅ Camera opened successfully")
    print("\n🎯 Starting detection analysis...")
    print("-" * 60)
    
    try:
        # Perform multiple detections to show the process
        for i in range(5):
            print(f"\n📸 Detection #{i+1} - {time.strftime('%H:%M:%S')}")
            print("-" * 40)
            
            # Capture and analyze
            result = detector.capture_and_analyze()
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            # Display key results
            print(f"🎯 Signal: {result['signal']}")
            print(f"🏠 Room Status: {result['room_status']}")
            print(f"📊 Decision Score: {result['detection_summary']['decision_factors']['final_score']:.3f}")
            
            # Show frame analysis
            frame_stats = result['frame_analysis']
            print(f"📐 Frame: {frame_stats['dimensions']['width']}x{frame_stats['dimensions']['height']}")
            print(f"💡 Avg Brightness: {frame_stats['average_brightness']:.1f}")
            print(f"📈 Brightness Range: {frame_stats['min_brightness']:.1f} - {frame_stats['max_brightness']:.1f}")
            
            # Show threshold analysis
            print("\n🔍 Threshold Analysis:")
            for threshold_name, threshold_data in result['threshold_analysis'].items():
                print(f"  {threshold_name.replace('_', ' ').title()}:")
                print(f"    Contours: {threshold_data['valid_contours']}")
                print(f"    Total Brightness: {threshold_data['total_brightness']:.1f}")
                print(f"    Avg Brightness: {threshold_data['average_brightness']:.1f}")
            
            # Show detection summary
            summary = result['detection_summary']
            print(f"\n📋 Detection Summary:")
            print(f"  Total Contours: {summary['total_contours_found']}")
            print(f"  Area Coverage: {summary['area_percentage']:.2f}%")
            print(f"  Light Sources: {len(result['detected_light_sources'])}")
            
            # Show decision factors
            factors = summary['decision_factors']
            print(f"\n⚖️ Decision Factors:")
            print(f"  Brightness Score: {factors['brightness_score']:.3f}")
            print(f"  Area Score: {factors['area_score']:.3f}")
            print(f"  Contour Score: {factors['contour_score']:.3f}")
            print(f"  Final Score: {factors['final_score']:.3f}")
            
            # Wait before next detection
            if i < 4:  # Don't wait after the last detection
                print("\n⏳ Waiting 2 seconds for next detection...")
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n⏹️ Detection stopped by user")
    except Exception as e:
        print(f"\n❌ Error during detection: {e}")
    finally:
        # Close camera
        print("\n🔒 Closing camera...")
        detector.close_camera()
        print("✅ Camera closed")
    
    print("\n📊 Detection History:")
    print("-" * 30)
    history = detector.get_detection_history()
    for i, detection in enumerate(history):
        print(f"{i+1}. {detection['timestamp']} - {detection['signal']} (Score: {detection['detection_summary']['decision_factors']['final_score']:.3f})")

def test_single_detection():
    """Test a single detection with full output"""
    print("\n🔬 Single Detection Test")
    print("=" * 40)
    
    detector = LightBulbDetector()
    
    if not detector.open_camera():
        print("❌ Failed to open camera")
        return
    
    try:
        print("📸 Capturing and analyzing frame...")
        result = detector.capture_and_analyze()
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print("\n📋 Full Detection Result:")
        print(json.dumps(result, indent=2, default=str))
        
    finally:
        detector.close_camera()

if __name__ == "__main__":
    print("🚀 Starting Enhanced Light Detection Tests...")
    
    # Test 1: Multiple detections
    test_detection_system()
    
    # Test 2: Single detailed detection
    test_single_detection()
    
    print("\n🎉 All tests completed!")
    print("\n💡 To see the web interface:")
    print("1. Run: python app.py")
    print("2. Open: http://localhost:5000")
    print("3. Click 'Start Camera' to see real-time detection") 