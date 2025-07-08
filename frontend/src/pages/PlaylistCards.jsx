import React, { useRef, useState } from "react";
import "../css/PlaylistCards.css";
import folder from "../assets/folder.png";
import download from "../assets/download.png";
import api from "../services/api";

function PlaylistCards({ pl_item: plItem, tracksData, tracksLoaded }) {
  const [downloading, setDownloading] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [downloadLinkDisabled, setDownloadLinkDisabled] = useState(false);
  const timerRef = useRef(null);

  function playlistTracksLoad() {
    setDownloading(true);
    setDownloaded(false);
    setDownloadLinkDisabled(false);

   
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }

    const titleList = [];
    for (const item of tracksData) {
      for (const [key] of Object.entries(item)) {
        titleList.push(key);
      }
    }

    if (titleList.includes(plItem.name)) {
      api.post("/download-playlist", {playlist_name: plItem.name})
        .then(() => {
          setDownloading(false);
          setDownloaded(true);
          
          api.post("/delete-playlist", {playlist_name: plItem.name})
          
          timerRef.current = setTimeout(() => {
            setDownloadLinkDisabled(true);        
            api.post("/delete-zipplaylist", {playlist_name: plItem.name})
              .catch(err => console.error("Error deleting zip playlist:", err));
          }, 60000);
        })
        .catch(() => {
          setDownloading(false);
        });
    } else {
      console.log("No playlist data");
      setDownloading(false);
    }
  };

  React.useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const downloadZip = () => {
    const downloadUrl = `http://127.0.0.1:8888/zipdownload/${encodeURIComponent(plItem.name)}`;
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `${plItem.name}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="pl-card">
      <div className="pl-poster">
        <img src={plItem.url} alt={plItem.name} />
        
 
        {!tracksLoaded && (
          <div className="download-overlay">
            <span className="spinner"></span>
          </div>
        )}
        
      
        {tracksLoaded && (
          <>
            {!downloading && !downloaded && (
              <div className="download-overlay">
                <button className="download-icon" onClick={playlistTracksLoad}>
                  <img 
                    src={download} 
                    style={{ width: "30px", height: "30px" }} 
                    alt="download" 
                  />
                </button>
              </div>
            )}
            
            {downloading && (
              <span 
                className="spinner" 
                style={{
                  position: "absolute",
                  top: "40%",
                  left: "40%",
                  transform: "translate(-50%, -50%)"
                }}
              ></span>
            )}
          </>
        )}
      </div>
      
      <div className="pl-title">{plItem.name}</div>
      <div className="pl-songs">
        <span className="song-count">{plItem.tracks} song/s</span>
        {downloaded && (
          <a 
            onClick={downloadLinkDisabled ? (e) => e.preventDefault() : downloadZip}
            download={`${plItem.name}.zip`}
            style={{
              opacity: downloadLinkDisabled ? 0.5 : 1,
              pointerEvents: downloadLinkDisabled ? "none" : "auto",
              cursor: downloadLinkDisabled ? "not-allowed" : "pointer",
              transition: "opacity 0.3s"
            }}
            tabIndex={downloadLinkDisabled ? -1 : 0}
            aria-disabled={downloadLinkDisabled}
          >
            <img src={folder} className="folder-style" alt="folder"/>
          </a>
        )}
      </div>
    </div>
  );
}

export default PlaylistCards;