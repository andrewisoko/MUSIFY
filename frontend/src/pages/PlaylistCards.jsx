import React, { useEffect, useState } from "react";
import "../css/PlaylistCards.css";
import folder from "../assets/folder.png";
import download from "../assets/download.png";
import api from "../services/api"
import tracksData from "../services/allTracks.json"



function PlaylistCards({ pl_item: plItem }) {

  const [downloading,setDownloading] = useState(false)
  const [downloaded, setDownloaded] = useState(false);

  api.get("/tracks")

  function playlistTracksLoad() {
    
    const titleList = []

    for (const item of tracksData) {
      for (const [key, values] of Object.entries(item)) {
        titleList.push(key)
          }
        }
    if (titleList.includes(plItem.name)){
      const playlistName = plItem.name
      setDownloading(true);
      api.post("/download-playlist",{playlist_name:playlistName})
      .then(()=>{
        setDownloading(false);
        setDownloaded(true);
      })
      .catch(() => {
        downloading(false);
      });
    }else{
      console.log("NOO")
    };
  };
  
  const downloadZip = () => {
  const downloadUrl = `http://127.0.0.1:8888/api/download/${encodeURIComponent(plItem.name)}`;
  const link = document.createElement('a');
  link.href = downloadUrl;
  link.download = `${plItem.name}.zip`; 
  link.click();
  document.body.removeChild(link);
};
  return (
    <div className="pl-card">
  <div className="pl-poster">
    <img src={plItem.url} alt={plItem.name} />

    {!downloading && !downloaded && (
      <div className="download-overlay">
        <button
          className="download-icon"
          onClick={playlistTracksLoad}
        >
          <img
            src={download}
            style={{ width: "30px", height: "30px" }}
            alt="download"
          />
        </button>
      </div>
    )}

    {downloading && (
      <span className="spinner"  style={{
        position: "absolute",
        top: "40%",
        left: "40%",
        transform: "translate(-50%, -50%)"
      }} 
      ></span>
    )}


  </div>
  <div className="pl-title">{plItem.name}</div>
  <div className="pl-songs">
    <span className="song-count">{plItem.tracks} song/s</span>
    {downloaded && (
        <a onClick={downloadZip} download={`${plItem.name}.zip`}>
        <img src={folder} className="folder-style" alt="folder" />
      </a>
    )}
  </div>
</div>

      );
    }

export default PlaylistCards;