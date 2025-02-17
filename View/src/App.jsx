import React, { useState, useRef, useEffect } from "react";
import PlotPoints from "./PlotPoints";
import "./App.css";
import PathAnimation from "./PathAnimation";

const App = () => {
    const videoRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const [devices, setDevices] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState("");
    const [recording, setRecording] = useState(false);
    const chunksRef = useRef([]);
    const [selectedPoints, setSelectedPoints] = useState([]);
    const [capturedFrame, setCapturedFrame] = useState(null);
    const intervalRef = useRef(null);

    // Check for supported MIME types
    const getSupportedMimeType = () => {
        const mimeTypes = [
            'video/mp4; codecs=avc1',
            'video/webm; codecs=vp9',
            'video/webm; codecs=vp8',
            'video/webm'
        ];
        return mimeTypes.find(mimeType => MediaRecorder.isTypeSupported(mimeType));
    };

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then((deviceList) => {
            const videoDevices = deviceList.filter(device => device.kind === "videoinput");
            setDevices(videoDevices);
            const defaultCamera = videoDevices.find(device => device.label.toLowerCase().includes("face time") || device.label.toLowerCase().includes("built-in"));
            setSelectedDevice(defaultCamera?.deviceId || videoDevices[0]?.deviceId || "");
        });
    }, []);

    useEffect(() => {
        if (!selectedDevice) return;
        navigator.mediaDevices
            .getUserMedia({ video: { deviceId: { exact: selectedDevice } } })
            .then((stream) => {
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
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
        ctx.drawImage(video, 0, 0);
        setCapturedFrame(canvas.toDataURL("image/png"));
    };

    const startRecording = (stream) => {
        chunksRef.current = [];
        const mimeType = getSupportedMimeType();
        if (!mimeType) {
            console.error("No supported MIME type found");
            return;
        }

        const recorder = new MediaRecorder(stream, { mimeType });
        recorder.ondataavailable = (event) => event.data.size > 0 && chunksRef.current.push(event.data);
        recorder.onstop = () => saveVideo();
        mediaRecorderRef.current = recorder;
        recorder.start();
        setRecording(true);

        setTimeout(() => {
            recorder.stop();
            setRecording(false);
        }, 15000); // Record for 15 seconds

    };

    const saveVideo = () => {
        if (!chunksRef.current.length || !mediaRecorderRef.current) return;    
        const blob = new Blob(chunksRef.current, { type: mediaRecorderRef.current.mimeType });
        const url = URL.createObjectURL(blob);
        const ext = mediaRecorderRef.current.mimeType.split('/')[1].split(';')[0];
        const a = document.createElement("a");
        a.href = url;
        a.download = `video_${Date.now()}.${ext}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        if (videoRef.current?.srcObject) startRecording(videoRef.current.srcObject);
    };
    const [jsonDataExists, setJsonDataExists] = useState(false);

    useEffect(() => {
        fetch("/output2.json")
            .then((res) => res.json())
            .then((data) => {
                if (data && Object.keys(data).length > 0) {
                    setJsonDataExists(true);
                } else {
                    setJsonDataExists(false);
                }
            })
            .catch((err) => {
                console.error("Error loading JSON:", err);
                setJsonDataExists(false);
            });
    }, []);
    
return (
    <div>
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
            <PlotPoints onPointsSelected={setSelectedPoints} presetImage={capturedFrame} />
            <PathAnimation jsonPath="/output2.json" className="animated" />
            <p className="selected-points">Selected Points: {JSON.stringify(selectedPoints)}</p>
        </div>
    </div>
    </div>
);
};

export default App;