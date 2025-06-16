import { useEffect, useState } from "react";
import api from "../services/api"; 
import PlaylistCards from "./PlaylistCards";
import "../css/PlaylistCards.css";

function Playlists() {
  const [playlists, setPlaylists] = useState([]);

  useEffect(() => {
    api.get("/playlists")
      .then(response => setPlaylists(response.data.items))
      .catch(error => console.error(error));
  }, []);

  return (
          <div >
             <h2>Your Playlists</h2>
            <div className="pl-list">
                {playlists.map(pl => ( <PlaylistCards
                  key={pl.id}
                  pl_item={{ 
                    url: pl.images[0].url,
                     name: pl.name,
                     tracks: pl.tracks["total"]
                     }}
                  />
                ))}
            </div>
          </div>
  );
}

export default Playlists;
