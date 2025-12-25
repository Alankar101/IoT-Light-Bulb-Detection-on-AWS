# 💡 Light Bulb Detection System

A Python-based computer vision application that detects light bulbs in a room using your camera and determines whether they are on or off. The system provides a modern web interface for real-time monitoring.

## 🚀 Features

- **Real-time Camera Monitoring**: Live camera feed with continuous light detection
- **Smart Light Detection**: Uses OpenCV and computer vision algorithms to detect light bulbs
- **Status Signals**: Generates YES/NO signals based on room lighting conditions
- **Modern Web Interface**: Beautiful, responsive web application built with Flask
- **Real-time Updates**: Live status updates and camera feed streaming
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🛠️ Requirements

- Python 3.7 or higher
- Webcam or camera device
- Windows 10/11, macOS, or Linux

## 📦 Installation

1. **Clone or download this project** to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure your camera is accessible** and not being used by other applications

## 🚀 Usage

### Starting the Application

1. **Run the main application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Use the web interface** to:
   - Start/stop camera monitoring
   - View live camera feed
   - See real-time light detection results
   - Monitor room lighting status

### Web Interface Controls

- **Start Camera**: Begins continuous monitoring
- **Stop Camera**: Stops monitoring and releases camera
- **Detect Once**: Performs a single detection without continuous monitoring

### Understanding the Results

- **Signal**: 
  - `YES` = Lights are detected as ON
  - `NO` = Lights are detected as OFF
  - `UNKNOWN` = Detection status unclear

- **Room Status**: 
  - `LIGHTS_ON` = Room appears to have lights on
  - `LIGHTS_OFF` = Room appears to have lights off

- **Additional Metrics**:
  - Number of light bulbs detected
  - Average brightness levels
  - Timestamp of last detection

## 🔧 Technical Details

### Light Detection Algorithm

The system uses the following approach to detect light bulbs:

1. **Color Space Conversion**: Converts camera frames to HSV color space
2. **Brightness Thresholding**: Identifies bright areas using value channel
3. **Morphological Operations**: Cleans up detection masks
4. **Contour Analysis**: Finds and analyzes bright regions
5. **Classification**: Determines if detected regions are likely light bulbs

### Architecture

- **Backend**: Flask web server with RESTful API
- **Computer Vision**: OpenCV for image processing and analysis
- **Frontend**: Modern HTML5/CSS3/JavaScript interface
- **Real-time Processing**: Background threads for continuous monitoring

## 📁 Project Structure

```
light-bulb-detection/
├── app.py                 # Main Flask application
├── light_detector.py      # Core light detection logic
├── templates/
│   └── index.html        # Web interface template
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Camera Access Denied**:
   - Ensure no other applications are using the camera
   - Check camera permissions in your OS
   - Try running as administrator (Windows)

2. **Detection Not Working**:
   - Ensure adequate lighting in the room
   - Check camera focus and positioning
   - Verify camera is working in other applications

3. **Web Interface Not Loading**:
   - Check if port 5000 is available
   - Ensure firewall allows the connection
   - Verify all dependencies are installed

### Performance Tips

- **Good Lighting**: Ensure the room has consistent lighting for better detection
- **Camera Position**: Position camera to capture the entire room
- **Stable Mounting**: Use a tripod or stable mount for consistent results

## 🔮 Future Enhancements

- **Machine Learning**: Improved detection using trained models
- **Multiple Camera Support**: Support for multiple camera feeds
- **Historical Data**: Logging and analysis of lighting patterns
- **Mobile App**: Native mobile applications
- **API Integration**: Connect with smart home systems

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the troubleshooting section above
2. Review the error messages in the console
3. Ensure all dependencies are properly installed
4. Verify camera accessibility

---

**Happy Light Detection! 💡✨** 