#!/usr/bin/env python3
"""
Test script to verify the light bulb detection system installation
"""

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import flask
        print(f"✓ Flask version: {flask.__version__}")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✓ Pillow (PIL) imported successfully")
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False
    
    try:
        import imutils
        print(f"✓ Imutils imported successfully")
    except ImportError as e:
        print(f"✗ Imutils import failed: {e}")
        return False
    
    return True

def test_camera_access():
    """Test if camera can be accessed"""
    print("\nTesting camera access...")
    
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        
        if camera.isOpened():
            print("✓ Camera access successful")
            ret, frame = camera.read()
            if ret:
                print(f"✓ Camera frame captured: {frame.shape}")
            else:
                print("✗ Camera frame capture failed")
                camera.release()
                return False
            
            camera.release()
            return True
        else:
            print("✗ Camera access failed - camera not available")
            return False
            
    except Exception as e:
        print(f"✗ Camera test error: {e}")
        return False

def test_light_detector():
    """Test if the light detector module can be imported"""
    print("\nTesting light detector module...")
    
    try:
        from light_detector import LightBulbDetector
        print("✓ LightBulbDetector class imported successfully")
        
        detector = LightBulbDetector()
        print("✓ LightBulbDetector instance created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Light detector test failed: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask application...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        print("✓ Flask application created successfully")
        
        # Test basic route
        @app.route('/test')
        def test():
            return 'OK'
        
        print("✓ Flask route creation successful")
        return True
        
    except Exception as e:
        print(f"✗ Flask test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Light Bulb Detection System - Installation Test")
    print("=" * 55)
    
    tests = [
        ("Package Imports", test_imports),
        ("Camera Access", test_camera_access),
        ("Light Detector", test_light_detector),
        ("Flask Application", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 TEST SUMMARY")
    print("=" * 55)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to run.")
        print("\nTo start the application:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Check camera permissions and availability")
        print("- Ensure Python version is 3.7 or higher")

if __name__ == "__main__":
    main() 