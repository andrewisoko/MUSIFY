import { useEffect, useState } from "react";
import api from "../services/api"; 
import PlaylistCards from "./PlaylistCards";
import "../css/Playlists.css";
import Footer from "../components/Footer";

function Playlists() {
  const [playlists, setPlaylists] = useState([]);
  const [tracksData, setTracksData] = useState([]);
  const [allTracks, setAllTracks] = useState([]);

  useEffect(() => {
    api.get("/playlists")
      .then(response => setPlaylists(response.data.items))
      .catch(error => console.error(error));
  }, []);

  useEffect(() => {
    api.get("/tracks")
      .then(response => setTracksData(response.data))
      .catch(error => console.error(error));
    fetch("/services/allTracks.json")
      .then(res => res.json())
      .then(data => setAllTracks(data))
      .catch(err => console.error("Error loading allTracks:", err));
  }, []);

  return (
    <div className="pl-page-wrapper">
             <h1>Playlists</h1>
              <br></br>
             <p>Load the playlist songs to download by clicking the playlist image. </p>
             <p>After the playlists load, click the folder icon on a playlist to download it. </p>
             <p>If songs are not 100% accurate it is advised to download the specific song with the download search bar at the home page.</p>
             <p>Click the folder icon once the download spinner ends.</p>
             <p>Enjoy your music.</p>
      <div className="pl-list">
        {playlists.map(pl => (
          <PlaylistCards
            key={pl.id}
            pl_item={{
              url: pl.images[0].url,
              name: pl.name,
              tracks: pl.tracks["total"]
            }}
            tracksData={tracksData}
            allTracks={allTracks}
          />
        ))}
      </div>
      <Footer />
    </div>
  );
}

export default Playlists;
