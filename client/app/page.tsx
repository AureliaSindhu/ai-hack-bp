import SquatDetector from "./components/SquatDetector";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Squat Detection
          </h1>
          <p className="text-lg text-gray-600">
            Real-time pose detection and squat rep counting using computer
            vision
          </p>
        </header>

        <main className="flex flex-col lg:flex-row gap-8">
          <div className="lg:w-1/2">
            <SquatDetector />
          </div>

          <div className="lg:w-1/2">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">How it works</h2>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                    1
                  </div>
                  <div>
                    <h3 className="font-semibold">Camera Access</h3>
                    <p className="text-gray-600">
                      Allow camera access when prompted to start pose detection
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                    2
                  </div>
                  <div>
                    <h3 className="font-semibold">Pose Analysis</h3>
                    <p className="text-gray-600">
                      The AI analyzes your body position in real-time using
                      advanced pose estimation
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                    3
                  </div>
                  <div>
                    <h3 className="font-semibold">Rep Counting</h3>
                    <p className="text-gray-600">
                      Squat repetitions are automatically counted based on knee
                      flexion angles
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                    4
                  </div>
                  <div>
                    <h3 className="font-semibold">Results</h3>
                    <p className="text-gray-600">
                      View your squat count, processing time, and detailed
                      analysis results
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
