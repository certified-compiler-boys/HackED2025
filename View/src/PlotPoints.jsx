import { useRef, useState, useEffect } from "react";

const PlotPoints = ({ onPointsSelected, presetImage }) => {
    const canvasRef = useRef(null);
    const fileInputRef = useRef(null);
    const [image, setImage] = useState(presetImage || null); // Initialize with preset image
    const [points, setPoints] = useState([]);
    const globalCoords = useRef([]);

    useEffect(() => {
        if (presetImage) {
            setImage(presetImage); // Update image when presetImage changes
        }
    }, [presetImage]);

    useEffect(() => {
        if (!image) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        const img = new Image();
        img.src = image;
        img.onload = () => {
            // Get the container size
            const maxWidth = 640;
            const maxHeight = 480;

            // Get the original image dimensions
            let width = img.width;
            let height = img.height;

            // Calculate the scaling factor to fit the image within the max dimensions
            const scaleWidth = maxWidth / width;
            const scaleHeight = maxHeight / height;
            const scale = Math.min(scaleWidth, scaleHeight);

            // Apply the scaling factor
            width = width * scale;
            height = height * scale;

            // Set canvas size to fit the image
            canvas.width = width;
            canvas.height = height;

            // Draw the image scaled down to fit the box
            ctx.drawImage(img, 0, 0, width, height);
        };
    }, [image]);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (!file || !file.type.startsWith("image/")) return;

        const reader = new FileReader();
        reader.onload = (e) => setImage(e.target.result);
        reader.readAsDataURL(file);
    };

    const handleClick = (event) => {
        if (points.length >= 2) return; // Only allow two points

        const canvas = canvasRef.current;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left; // Absolute x position
        const y = event.clientY - rect.top; // Absolute y position

        // Calculate percentages relative to image dimensions
        const width = canvas.width;
        const height = canvas.height;
        const xPercent = (x / width) * 100;
        const yPercent = (y / height) * 100;

        const newPoints = [...points, { x: xPercent, y: yPercent }];
        setPoints(newPoints);
        globalCoords.current = newPoints;

        if (newPoints.length === 2) {
            onPointsSelected(globalCoords.current); // Send points to parent

            // Send points to Flask (Model folder)
            sendPointsToFlask(globalCoords.current);
        }

        // Redraw image with points
        const ctx = canvas.getContext("2d");
        const img = new Image();
        img.src = image;
        img.onload = () => {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "red";
            ctx.beginPath();
            newPoints.forEach((p) => {
                const xPos = (p.x / 100) * width; // Convert percentage back to pixels for drawing
                const yPos = (p.y / 100) * height; // Convert percentage back to pixels for drawing
                ctx.arc(xPos, yPos, 10, 0, 2 * Math.PI);
            });
            ctx.fill();
        };
    };

    const sendPointsToFlask = async (points) => {
        const dataToSend = { points: points };
    
        console.log("🚀 Sending data to Flask:", dataToSend);  // Debugging log
    
        try {
            const response = await fetch("http://127.0.0.1:5000/save-points", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(dataToSend),
            });
    
            console.log("📡 Fetch Response Status:", response.status); // Log HTTP status code
    
            if (!response.ok) {
                throw new Error(`❌ HTTP error! Status: ${response.status}`);
            }
    
            const result = await response.json();
            console.log("✅ Response from Flask:", result);
        } catch (error) {
            console.error("❌ Error sending points to Flask:", error);
        }
    };

    return (
        <div
        style={{
            width: "640px",
            height: "480px",  // Fixed width and height for the container
            border: "2px dashed gray",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "flex-start",  // Align items at the top
            cursor: "pointer",
            overflow: "hidden",  // Ensure content doesn't overflow
        }}
        >
            {!image ? (
                <>
                </>
            ) : (
                <>
                    <canvas
                        className="cursor"
                        ref={canvasRef}
                        onClick={handleClick}
                        style={{ cursor: "crosshair", marginBottom: "20px" }}  // Add margin below canvas
                    />
                    {points.length === 2 && (
                        <button
                            onClick={() => setPoints([])}
                            style={{
                                marginBottom: "50px",
                                padding: "5px 10px ",
                                backgroundColor: "#ff0000",
                                color: "#ffffff",
                                border: "none",
                                borderRadius: "16px",
                                cursor: "pointer",
                                fontSize: "16px",
                                boxShadow: "0 0 10px rgba(255, 0, 0, 0.5)",
                                zIndex: 999,
                                position: "relative",
                                top: "-3%"
                            }}
                        >
                            Reset Points
                        </button>
                    )}
                </>
            )}
        </div>
    );
};

export default PlotPoints;