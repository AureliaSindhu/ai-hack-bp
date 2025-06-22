"use client";

import { useState } from "react";

interface SquatResult {
  success: boolean;
  squat_reps: number;
  processing_time: number;
  depth_threshold: number;
  csv_file: string;
}

export default function SquatDetector() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<SquatResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [depthThreshold, setDepthThreshold] = useState(90);

  const startSquatDetection = async () => {
    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("/api/squat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          use_webcam: true,
          depth_threshold: depthThreshold,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to process squat detection");
      }

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-center">Squat Detector</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Depth Threshold (degrees)
        </label>
        <input
          type="number"
          value={depthThreshold}
          onChange={(e) => setDepthThreshold(Number(e.target.value))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          min="0"
          max="180"
        />
      </div>

      <button
        onClick={startSquatDetection}
        disabled={isProcessing}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {isProcessing ? "Processing..." : "Start Squat Detection"}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          <h3 className="font-bold mb-2">Results:</h3>
          <p>
            <strong>Squat Reps:</strong> {result.squat_reps}
          </p>
          <p>
            <strong>Processing Time:</strong>{" "}
            {result.processing_time.toFixed(2)} seconds
          </p>
          <p>
            <strong>Depth Threshold:</strong> {result.depth_threshold}°
          </p>
        </div>
      )}
    </div>
  );
}
