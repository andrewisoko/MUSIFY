import React, { useEffect, useState } from "react";
import "../css/PlaylistCards.css";
import folder from "../assets/folder.png";
import download from "../assets/download.png";
import api from "../services/api"
import tracksData from "../services/allTracks.json"



function PlaylistCards({ pl_item: plItem }) {

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
      api.post("/download-playlist",{playlist_name:playlistName})
    }else{
      console.log("NOO")
    }
  }
  
  return (
    <div className="pl-card">
      <div className="pl-poster">
        <img src={plItem.url} alt={plItem.name} />
        <div className="download-overlay">
          <button className="download-icon" onClick={playlistTracksLoad}>
            <img src={download} style={{ width: '30px', height: '30px'}}alt="download" />
          </button>
        </div>
      </div>
      <div className="pl-title">{plItem.name}</div>
      <div className="pl-songs">
        <span className="song-count">{plItem.tracks} song/s</span>
        <img src={folder} className="folder-style" alt="folder" />
      </div>
    </div>
  );
}

export default PlaylistCards;