import React, { useEffect, useRef } from 'react';
import { FaceDetection } from '../types';
import { Camera, AlertCircle, Loader2 } from 'lucide-react';

interface CameraFeedProps {
  videoRef: React.RefObject<HTMLVideoElement>;
  canvasRef: React.RefObject<HTMLCanvasElement>;
  detections: FaceDetection[];
  isDetecting: boolean;
  error: string | null;
}

export const CameraFeed: React.FC<CameraFeedProps> = ({
  videoRef,
  canvasRef,
  detections,
  isDetecting,
  error
}) => {
  const overlayCanvasRef = useRef<HTMLCanvasElement>(null);

  // Draw detection boxes on overlay canvas
  useEffect(() => {
    if (!overlayCanvasRef.current || !videoRef.current || detections.length === 0) return;

    const canvas = overlayCanvasRef.current;
    const video = videoRef.current;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw detection boxes
    detections.slice(0, 1).forEach((detection, index) => {
      const { boundingBox, confidence } = detection;
      
      // Set up styling
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 3;
      ctx.fillStyle = 'rgba(16, 185, 129, 0.1)';
      ctx.font = '14px Inter, sans-serif';

      // Draw bounding box
      ctx.fillRect(boundingBox.x, boundingBox.y, boundingBox.width, boundingBox.height);
      ctx.strokeRect(boundingBox.x, boundingBox.y, boundingBox.width, boundingBox.height);

      // Draw confidence label
      const label = `Face ${(confidence * 100).toFixed(1)}%`;
      const labelWidth = ctx.measureText(label).width;
      const labelHeight = 20;

      ctx.fillStyle = '#10b981';
      ctx.fillRect(
        boundingBox.x,
        boundingBox.y - labelHeight - 5,
        labelWidth + 10,
        labelHeight
      );

      ctx.fillStyle = 'white';
      ctx.fillText(label, boundingBox.x + 5, boundingBox.y - 8);
    });
  }, [detections, videoRef]);

  // Update canvas size when video loads
  useEffect(() => {
    const video = videoRef.current;
    const overlay = overlayCanvasRef.current;

    if (!video || !overlay) return;

    const updateCanvasSize = () => {
      overlay.width = video.videoWidth;
      overlay.height = video.videoHeight;
    };

    video.addEventListener('loadedmetadata', updateCanvasSize);
    return () => video.removeEventListener('loadedmetadata', updateCanvasSize);
  }, [videoRef]);

  if (error) {
    return (
      <div className="relative aspect-video bg-red-900/20 rounded-xl border-2 border-red-500/30 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
          <p className="text-red-300 font-medium">{error}</p>
          <p className="text-red-400 text-sm mt-2">Please check camera permissions</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative">
      <div className="relative aspect-video bg-gray-900 rounded-xl overflow-hidden border-2 border-gray-700">
        {!isDetecting && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-800/50 backdrop-blur-sm z-10">
            <div className="text-center">
              <Camera className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-300 font-medium">Camera Ready</p>
              <p className="text-gray-400 text-sm mt-2">Click start to begin detection</p>
            </div>
          </div>
        )}

        {isDetecting && (
          <div className="absolute top-4 left-4 z-20">
            <div className="flex items-center space-x-2 bg-green-500/20 backdrop-blur-sm rounded-lg px-3 py-2 border border-green-500/30">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-green-300 text-sm font-medium">Live Detection</span>
            </div>
          </div>
        )}

        {detections.length > 0 && (
          <div className="absolute top-4 right-4 z-20">
            <div className="bg-purple-500/20 backdrop-blur-sm rounded-lg px-3 py-2 border border-purple-500/30">
              <span className="text-purple-300 text-sm font-medium">
                {detections.length} Detection{detections.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>
        )}

        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-cover"
        />

        <canvas
          ref={overlayCanvasRef}
          className="absolute inset-0 w-full h-full pointer-events-none"
        />

        <canvas
          ref={canvasRef}
          className="hidden"
        />
      </div>

      {isDetecting && (
        <div className="mt-4 flex items-center justify-center space-x-2 text-purple-300">
          <Loader2 className="h-4 w-4 animate-spin" />
          <span className="text-sm">Processing video feed...</span>
        </div>
      )}
    </div>
  );
};