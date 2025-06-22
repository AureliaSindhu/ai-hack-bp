# AI Squat Detection

A real-time pose detection application that counts squat repetitions using computer vision. Built with Next.js frontend and Python Flask backend.

## Features

- 🎥 Real-time webcam pose detection
- 📊 Automatic squat rep counting
- 🎯 Configurable depth threshold
- 📈 Processing time analysis
- 🎨 Modern, responsive UI

## Tech Stack

### Frontend

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hooks** - State management

### Backend

- **Python Flask** - API server
- **Sports2D** - Pose detection library
- **OpenCV** - Computer vision
- **Pandas** - Data analysis

## Prerequisites

- Node.js 18+
- Python 3.8+
- Webcam access
- Sports2D library installed

## Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd ai-hack-bp
   ```

2. **Install all dependencies**

   ```bash
   npm run install:all
   ```

   This will install:

   - Root dependencies (concurrently)
   - Frontend dependencies (Next.js, React, etc.)
   - Backend dependencies (Flask, Sports2D, etc.)

## Running the Application

### Development Mode (Recommended)

Run both frontend and backend simultaneously:

```bash
npm run dev
```

This will start:

- Frontend: http://localhost:3000
- Backend: http://localhost:5000

### Running Separately

**Frontend only:**

```bash
npm run dev:frontend
```

**Backend only:**

```bash
npm run dev:backend
```

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Adjust the depth threshold if needed (default: 90 degrees)
3. Click "Start Squat Detection"
4. Allow camera access when prompted
5. Perform squats in front of the camera
6. View your results including rep count and processing time

## API Endpoints

### GET /api/squat

Returns information about the squat detection service.

**Response:**

```json
{
  "message": "Squat detection API is running",
  "status": "ready",
  "features": [
    "real-time pose detection",
    "squat rep counting",
    "angle analysis"
  ]
}
```

### POST /api/squat

Processes squat detection from webcam or video file.

**Request Body:**

```json
{
  "use_webcam": true,
  "depth_threshold": 90,
  "video_path": null
}
```

**Response:**

```json
{
  "success": true,
  "squat_reps": 5,
  "processing_time": 2.34,
  "depth_threshold": 90,
  "csv_file": "/path/to/angles.csv"
}
```

### GET /api/health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "service": "squat-detection-api"
}
```

## Configuration

### Environment Variables

Create a `.env.local` file in the `client` directory:

```env
BACKEND_URL=http://localhost:5000
```

### Backend Configuration

The backend uses a `config.toml` file for Sports2D configuration. See the Sports2D documentation for available options.

## Project Structure

```
ai-hack-bp/
├── client/                 # Next.js frontend
│   ├── app/
│   │   ├── api/           # API routes (proxies to backend)
│   │   ├── components/    # React components
│   │   └── page.tsx       # Main page
│   └── package.json
├── server/                # Python Flask backend
│   ├── app.py            # Main Flask application
│   ├── config.toml       # Sports2D configuration
│   └── requirements.txt  # Python dependencies
├── package.json          # Root package.json with scripts
└── README.md
```

## Troubleshooting

### Common Issues

1. **Camera not working**

   - Ensure you're using HTTPS or localhost
   - Check browser permissions
   - Try refreshing the page

2. **Backend connection failed**

   - Verify the backend is running on port 5000
   - Check the `BACKEND_URL` environment variable
   - Ensure all Python dependencies are installed

3. **Sports2D not found**
   - Install Sports2D: `pip install sports2d`
   - Check the Sports2D documentation for additional setup

### Development Tips

- Use browser dev tools to monitor API calls
- Check the browser console for frontend errors
- Monitor the terminal for backend logs
- Use the health check endpoint to verify backend status

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
