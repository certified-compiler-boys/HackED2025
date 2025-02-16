import NodeMediaServer from "node-media-server";

const config = {
  logType: 2,
  rtmp: {
    port: 1935,
    chunk_size: 60000,
    gop_cache: true,
    ping: 60,
    ping_interval: 2,
  },
  http: {
    port: 8000,
    mediaroot: "./media",
    allow_origin: "*",
  },
  trans: {
    ffmpeg: "/usr/bin/ffmpeg", // Ensure ffmpeg is installed
    tasks: [
      {
        app: "live",
        hls: true,
        hlsFlags: "[hls_time=2:hls_list_size=5:hls_flags=delete_segments]",
        dash: false,
      },
    ],
  },
};

const nms = new NodeMediaServer(config);
nms.run();
hls.loadSource("http://localhost:8000/live/stream.m3u8");

