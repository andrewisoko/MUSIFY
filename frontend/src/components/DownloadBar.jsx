import { useState } from "react";
import "../css/Home.css";
import api from "../services/api";

function DownloadBar() {
  const [inputUser, setInputUser] = useState("");
  const [downloading, setDownloading] = useState(false);
  const [downloadReady, setDownloadReady] = useState(false);
  const [linkDisabled, setLinkDisabled] = useState(false);

  const changeVal = (event) => {
    setInputUser(event.target.value);
    setDownloadReady(false);
    setLinkDisabled(false);
  };

  function DownloadAudio() {
    if (downloading || !inputUser.trim()) return;
    
    setDownloading(true);
    setDownloadReady(false);

    api
      .post("/download-audio", { audio_url: inputUser })
      .then(() => {
        setDownloading(false);
        setDownloadReady(true);
      })
      .catch(() => {
        setDownloading(false);
      });
    
    // Cleanup operations
    api.get("/0101delete-audio");
    api.get("/delete-zipaudio");
  }

  const downloadAudioZip = () => {
    const downloadUrl = `http://127.0.0.1:8888/download-zipaudio`;
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = `Youtube Downloads.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setLinkDisabled(true);
  };

  return (
    <>
      <div className="download-bar">
        <input
          placeholder="Enter a URL"
          value={inputUser}
          onChange={changeVal}
          type="text"
          className="download-input"
        />

        <button
          onClick={DownloadAudio}
          className="download-btn"
          disabled={downloading || !inputUser.trim()}
          aria-label={downloading ? "Processing..." : "Download"}
        >
          {downloading ? (
            <span 
              className="spinner" 
              style={{
                width: "10px",
                height: "10px",
                borderTop: "4px solid",
                transform: "translate(-50%, -50%)"
              }}
            ></span>
          ) : (
            <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
              <path
                d="M11 3v10"
                stroke="#fff"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <path
                d="M7 11l4 4 4-4"
                stroke="#fff"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <rect x="5" y="17" width="12" height="2" rx="1" fill="#fff" />
            </svg>
          )}
        </button>
      </div>

  
      {downloadReady && !linkDisabled && (
        <a
          onClick={downloadAudioZip}
          style={{
            cursor: "pointer",
            fontWeight: "bold",
            textAlign: "center",
            textDecoration: "none",
            display: "block",
            margin: "12px auto 0 auto",
            color: "#06f",
          }}
        >
          Download zip
        </a>
      )}
    </>
  );
}

export default DownloadBar;