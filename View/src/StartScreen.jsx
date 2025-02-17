import React, { useState } from "react";
import AppImplementation from "./App"; // your provided implementation
import "./StartScreen.css"; // custom styles for the start screen

const StartScreen = () => {
  const [started, setStarted] = useState(false);

  return (
    <div className="container">
      {started ? (
        <AppImplementation />
      ) : (
        <div className="start-screen">
          <h1 className="title">Welcome to the Video Recorder</h1>
          <button className="start-button" onClick={() => setStarted(true)}>
            Start
          </button>
        </div>
      )}
    </div>
  );
};

export default StartScreen;
