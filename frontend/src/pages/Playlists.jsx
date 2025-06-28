import { useEffect, useState } from "react";
import api from "../services/api"; 
import PlaylistCards from "./PlaylistCards";
import "../css/Playlists.css";
import Footer from "../components/Footer";

function Playlists() {
  const [playlists, setPlaylists] = useState([]);
  const [tracksData, setTracksData] = useState([]);
  const [allTracks, setAllTracks] = useState([]);
  const [tracksLoaded, setTracksLoaded] = useState(false); // New state

  useEffect(() => {
    api.get("/playlists")
      .then(response => {
        setPlaylists(response.data.items);
        return api.get("/tracks");
      })
      .then(response => setTracksData(response.data))
      .catch(error => console.error(error));
  }, []);

  useEffect(() => {
    const fetchTracks = async () => {
      try {
        const res = await fetch("/services/allTracks.json");
        if (!res.ok) throw new Error("Failed to load tracks");
        const data = await res.json();
        setAllTracks(data);
        setTracksLoaded(true);
      } catch (err) {
        console.error("Error loading allTracks:", err);
        // Retry after 2 seconds if failed
        setTimeout(fetchTracks, 2000);
      }
    };

    fetchTracks();
  }, []);

  return (
    <div className="pl-page-wrapper">
      <h1>Playlists</h1>
      <br></br>

      <strong>PLEASE READ!</strong>
      <p>If many songs are in the playlist it might take a while, please be patient. Do not refresh.</p>
      <p>Click the folder icon once the download spinner ends.</p>
      <p>Folder image download available only for 1 minute! </p>
      <p>If songs downloaded are not 100% accurate it is advised to download the specific song with the download search bar at the home page.</p>
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
            tracksLoaded={tracksLoaded} 
          />
        ))}
      </div>
      <Footer />
    </div>
  );
}

export default Playlists;
