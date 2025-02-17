import React, { useRef, useEffect, useState } from 'react';

const PathAnimation = ({ jsonPath }) => {
    const canvasRef = useRef(null);
    const [points, setPoints] = useState([]);

    const fetchData = async () => {
        try {
            const response = await fetch(jsonPath + `?t=${Date.now()}`); // Prevent caching
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                throw new Error("Received non-JSON response");
            }
            const data = await response.json();
            setPoints(data.points || []);
        } catch (error) {
            console.error("Error loading JSON:", error);
        }
    };

    useEffect(() => {
        fetchData(); // Initial fetch
        const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
        return () => clearInterval(interval);
    }, [jsonPath]);

    useEffect(() => {
        if (points.length === 0) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let animationFrameId;

        canvas.width = 640;
        canvas.height = 480;

        const mappedPoints = points.map(([x, y]) => [
            (x / 100) * canvas.width,
            (y / 100) * canvas.height
        ]);

        const generateBezierPoints = (points) => {
            const smoothPath = [];
            for (let i = 0; i < points.length - 1; i++) {
                const p0 = points[i];
                const p1 = points[i + 1];
                const midX = (p0[0] + p1[0]) / 2;
                const midY = (p0[1] + p1[1]) / 2;
                smoothPath.push(p0, [midX, midY]);
            }
            smoothPath.push(points[points.length - 1]);
            return smoothPath;
        };

        const smoothPoints = generateBezierPoints(mappedPoints);
        let progress = 0;

        const drawGlowTrail = (ctx, points, progress) => {
            ctx.globalAlpha = 0.4;
            for (let i = 0; i < progress; i++) {
                ctx.beginPath();
                ctx.arc(points[i][0], points[i][1], 5, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(0, 255, 0, ${i / progress})`;
                ctx.fill();
            }
            ctx.globalAlpha = 1;
        };

        const drawArrow = (ctx, x, y, angle) => {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);
            ctx.beginPath();
            ctx.moveTo(-10, -5);
            ctx.lineTo(10, 0);
            ctx.lineTo(-10, 5);
            ctx.closePath();
            ctx.fillStyle = "limegreen";
            ctx.fill();
            ctx.restore();
        };

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.beginPath();
            ctx.moveTo(smoothPoints[0][0], smoothPoints[0][1]);
            for (let i = 1; i < smoothPoints.length; i++) {
                ctx.lineTo(smoothPoints[i][0], smoothPoints[i][1]);
            }
            ctx.strokeStyle = "limegreen";
            ctx.lineWidth = 2;
            ctx.stroke();

            drawGlowTrail(ctx, smoothPoints, progress);

            if (progress < smoothPoints.length - 1) {
                const [x1, y1] = smoothPoints[progress];
                const [x2, y2] = smoothPoints[progress + 1];
                const angle = Math.atan2(y2 - y1, x2 - x1);
                drawArrow(ctx, x1, y1, angle);
                progress++;
            } else {
                progress = 0;
            }

            animationFrameId = requestAnimationFrame(animate);
        };

        animate();

        return () => cancelAnimationFrame(animationFrameId);
    }, [points]);

    return <canvas ref={canvasRef} className="path-animation-canvas" />;
};

export default PathAnimation;