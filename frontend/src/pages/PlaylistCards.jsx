import "../css/PlaylistCards.css";
import folder from "../assets/folder.png";
import download from "../assets/download.png";

function PlaylistCards({ pl_item }) {
  return (
    <div className="pl-card">
      <div className="pl-poster">
        <img src={pl_item.url} alt={pl_item.name} />
        <div className="download-overlay">
          <button className="download-icon">
            <img src={download} style={{ width: '30px', height: '30px'}}alt="download" />
          </button>
        </div>
      </div>
      <div className="pl-title">{pl_item.name}</div>
      <div className="pl-songs">
        <span className="song-count">{pl_item.tracks} song/s</span>
        <img src={folder} className="folder-style" alt="folder" />
      </div>
    </div>
  );
}

export default PlaylistCards;