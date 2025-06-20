import React, { useEffect, useState } from "react";
import "../css/PlaylistCards.css";
import folder from "../assets/folder.png";
import download from "../assets/download.png";
import api from "../services/api"



function PlaylistCards({ pl_item: plItem }) {

  const allTracks = api.get("/tracks")
  
  function playlistName() {

    if (plItem.name){
      console.log("YAH MAN")
    }else{
      console.log("Not here")
    }
  }

  return (
    <div className="pl-card">
      <div className="pl-poster">
        <img src={plItem.url} alt={plItem.name} />
        <div className="download-overlay">
          <button className="download-icon" onClick={playlistName}>
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