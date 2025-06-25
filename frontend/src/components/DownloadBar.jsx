import { useState,useEffect } from "react";
import "../css/Home.css"
import api from "../services/api";


function DownloadBar(){

    const [inputUser,setInputUser] = useState("")
    const[Downloaded,setDownloaded] = useState(false)
    const [downloading, setDownloading] = useState(false);
  

    const changeVal = event => {
        setInputUser(event.target.value)
    }
    
    function DownloadAudio(){

        setDownloading(true)

        api.post("/download-audio",{audio_url:inputUser})
        .then(()=> {
            setDownloading(false)
        })
        .then(()=>{
            setDownloaded(true)
        })
       
        
    }

    const downloadAudioZip = () => {
        const downloadUrl = `http://127.0.0.1:8888/download-zipaudio`;
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `Youtube Downloads.zip`;
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

      {/* Download button logic */}
      {!downloading && !Downloaded && (
        <button
          onClick={DownloadAudio}
          className="download-btn"
          aria-label="Download"
        >
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M11 3v10" stroke="#fff" strokeWidth="2" strokeLinecap="round"/>
            <path d="M7 11l4 4 4-4" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <rect x="5" y="17" width="12" height="2" rx="1" fill="#fff"/>
          </svg>
        </button>
      )}

      {downloading && (
        <button className="download-btn">
          <span className="spinner" style={{
            width: "10px",
            height: "10px",
            borderTop: "4px solid",
            transform: "translate(-50%, -50%)"
          }}></span>
        </button>
      )}

      {/* Downloaded button INSIDE the bar */}
      {Downloaded && (
        <button
          onClick={DownloadAudio}
          className="download-btn"
          aria-label="Download"
        >
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M11 3v10" stroke="#fff" strokeWidth="2" strokeLinecap="round"/>
            <path d="M7 11l4 4 4-4" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <rect x="5" y="17" width="12" height="2" rx="1" fill="#fff"/>
          </svg>
        </button>
      )}
    </div>

    {/* Downloaded anchor OUTSIDE the bar */}
    {Downloaded && (
      <a
        onClick={downloadAudioZip}
        style={{
          cursor: "pointer",
          fontWeight: "bold",
          textAlign: "center",
          textDecoration: "none",
          display: "block",
          margin: "12px auto 0 auto"
        }}
      >
        Download zip
      </a>
    )}
  </>
);

            
};

export default DownloadBar;