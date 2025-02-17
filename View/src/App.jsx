// init: our app.jsx with routing for a start page and main content, you chutiya.
import React, { useState, useRef, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import PlotPoints from "./PlotPoints";
import "./App.css";
import PathAnimation from "./PathAnimation";

// init: start page component, yo. this is the welcome screen, you magnificent bastard.
const StartPage = () => {
  const navigate = useNavigate();
  return (
    <div className="start-page" style={{ textAlign: "center", padding: "50px" }}>
      <h1>Welcome to CrowdNav!</h1>
      <p>Press the button below to run the app!</p>
      <button 
        onClick={() => navigate("/main")}
        style={{ padding: "10px 20px", fontSize: "16px" }}
      >
        Run app
      </button>
    </div>
  );
};

// init: main content component with your original app logic, you dumbass.
const MainContent = () => {
  const navigate = useNavigate(); // init: use navigate hook for routing on stop, motherfucker.
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [devices, setDevices] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState("");
  const [recording, setRecording] = useState(false);
  const chunksRef = useRef([]);
  const [selectedPoints, setSelectedPoints] = useState([]);
  const [capturedFrame, setCapturedFrame] = useState(null);
  const [stream, setStream] = useState(null);
  const recordingIntervalRef = useRef(null);

  // init: check for supported mime types, cuz we ain't recording with bullshit formats.
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
    
    const initializeCamera = async () => {
      try {
        const newStream = await navigator.mediaDevices.getUserMedia({ 
          video: { deviceId: { exact: selectedDevice } } 
        });
        setStream(newStream);
        
        if (videoRef.current) {
          videoRef.current.srcObject = newStream;
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
        }
      } catch (err) {
        console.error("error accessing webcam:", err);
      }
    };

    initializeCamera();
  }, [selectedDevice]);

  const captureFrame = (video) => {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);
    setCapturedFrame(canvas.toDataURL("image/png"));
  };

  const startRecording = () => {
    if (!stream) return;

    const startNewRecording = () => {
      chunksRef.current = [];
      const mimeType = getSupportedMimeType();
      if (!mimeType) {
        console.error("no supported mime type found");
        return;
      }

      const recorder = new MediaRecorder(stream, { mimeType });
      recorder.ondataavailable = (event) => event.data.size > 0 && chunksRef.current.push(event.data);
      recorder.onstop = saveVideo;
      mediaRecorderRef.current = recorder;
      recorder.start();
      setRecording(true);

      // init: stop recording after 15 seconds, cuz we ain't got all day.
      setTimeout(() => {
        recorder.stop();
      }, 15000);
    };

    // init: start the first recording, you dumbass.
    startNewRecording();

    // init: set up an interval to keep recording every 15 seconds.
    recordingIntervalRef.current = setInterval(startNewRecording, 15000);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    if (recordingIntervalRef.current) {
      clearInterval(recordingIntervalRef.current);
    }
    setRecording(false);
    // init: navigating back to start page after stop is clicked, motherfucker.
    navigate("/");
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
        console.error("error loading json:", err);
        setJsonDataExists(false);
      });
  }, []);
  
  return (
    <div>
      <div className="grid-container">
        <div className="video-container">
          <h2>webcam feed</h2>
          <select onChange={(e) => setSelectedDevice(e.target.value)} value={selectedDevice}>
            {devices.map((device) => (
              <option key={device.deviceId} value={device.deviceId}>
                {device.label || `camera ${device.deviceId}`}
              </option>
            ))}
          </select>
          <video ref={videoRef} autoPlay playsInline />
          <div className="recording-controls">
            <button 
              onClick={startRecording}
              disabled={!selectedDevice || recording}
              className="record-button"
            >
              start recording
            </button>
            <button 
              onClick={stopRecording}
              disabled={!recording}
              className="stop-button"
            >
              stop recording
            </button>
          </div>
        </div>

        <div className="plot-container">
          <h2>plot points on image</h2>
          <PlotPoints onPointsSelected={setSelectedPoints} presetImage={capturedFrame} />
          <PathAnimation jsonPath="/output2.json" className="animated" />
          <p className="selected-points">selected points: {JSON.stringify(selectedPoints)}</p>
        </div>
      </div>
    </div>
  );
};

// init: our main app component with routing. this is the entry point, you piece of shit.
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/main" element={<MainContent />} />
      </Routes>
    </Router>
  );
};

export default App;
