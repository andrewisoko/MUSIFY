import { useEffect, useState } from "react";
import api from "../services/api"; 

function Playlists() {
  const [playlists, setPlaylists] = useState([]);

  useEffect(() => {
    api.get("/playlists")
      .then(response => setPlaylists(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h2>Your Playlists</h2>
      <ul>
        {playlists.map(pl => (
          <li key={pl.id}>{pl.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Playlists;
