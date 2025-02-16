import React, { useState, useRef, useEffect } from "react";
import PlotPoints from "./PlotPoints";
import "./App.css";

const App = () => {
    const videoRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const [devices, setDevices] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState("");
    const [recording, setRecording] = useState(false);
    const chunksRef = useRef([]);
    const [selectedPoints, setSelectedPoints] = useState([]);
    const [capturedFrame, setCapturedFrame] = useState(null); // State to store the third frame

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then((deviceList) => {
            // Filter only video input devices
            const videoDevices = deviceList.filter(device => device.kind === "videoinput");
            setDevices(videoDevices);

            // Default to Mac's built-in camera if available
            const defaultCamera = videoDevices.find(device => device.label.toLowerCase().includes("face time") || device.label.toLowerCase().includes("built-in"));
            
            // If found, set the Mac camera as the selected device
            if (defaultCamera) {
                setSelectedDevice(defaultCamera.deviceId);
            } else if (videoDevices.length > 0) {
                // Fallback to the first available camera
                setSelectedDevice(videoDevices[0].deviceId);
            }
        });
    }, []);

    useEffect(() => {
        if (!selectedDevice) return;
        navigator.mediaDevices
            .getUserMedia({ video: { deviceId: { exact: selectedDevice } } })
            .then((stream) => {
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;

                    // Capture the third frame after the video starts playing
                    const video = videoRef.current;
                    let frameCount = 0;

                    const handleTimeUpdate = () => {
                        frameCount++;
                        if (frameCount === 3) {
                            captureFrame(video);
                            video.removeEventListener("timeupdate", handleTimeUpdate);
                        }
                    };

                    video.addEventListener("timeupdate", handleTimeUpdate);
                    startRecording(stream);
                }
            })
            .catch((err) => console.error("Error accessing webcam:", err));
    }, [selectedDevice]);

    const captureFrame = (video) => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const frameDataUrl = canvas.toDataURL("image/png");
        setCapturedFrame(frameDataUrl); // Set the captured frame
    };

    const startRecording = (stream) => {
        chunksRef.current = [];
        const recorder = new MediaRecorder(stream, { mimeType: "video/webm" });

        recorder.ondataavailable = (event) => {
            if (event.data.size > 0) chunksRef.current.push(event.data);
        };

        recorder.onstop = () => saveVideo();
        mediaRecorderRef.current = recorder;
        recorder.start();
        setRecording(true);

        setTimeout(() => {
            recorder.stop();
            setRecording(false);
        }, 1500000);
    };

    const saveVideo = () => {
        if (chunksRef.current.length === 0) return;
        const blob = new Blob(chunksRef.current, { type: "video/webm" });
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = `video_${Date.now()}.webm`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        if (videoRef.current?.srcObject) startRecording(videoRef.current.srcObject);
    };

    return (
        <div className="grid-container">
            <div className="video-container">
                <h2>Webcam Feed (Auto Recording 15s Clips)</h2>
                <select onChange={(e) => setSelectedDevice(e.target.value)} value={selectedDevice}>
                    {devices.map((device) => (
                        <option key={device.deviceId} value={device.deviceId}>
                            {device.label || `Camera ${device.deviceId}`}
                        </option>
                    ))}
                </select>
                <video ref={videoRef} autoPlay playsInline />
                <p className="recording-status">{recording ? "Recording..." : "Waiting to record"}</p>
            </div>

            <div className="plot-container">
                <h2>Plot Points on Image</h2>
                {/* Pass the captured frame to PlotPoints */}
                <PlotPoints onPointsSelected={setSelectedPoints} presetImage={capturedFrame} />
                <p className="selected-points">Selected Points: {JSON.stringify(selectedPoints)}</p>
            </div>
        </div>
    );
};

export default App;