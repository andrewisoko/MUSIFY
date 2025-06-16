import "../css/PlaylistCards.css"
import folder from  "../assets/folder.png"
//    downloading process here

function PlaylistCards({pl_item}){
           

    return <div className="pl-card"> 
            <div className="pl-poster">
                <img src={pl_item.url} 
                     alt={pl_item.name}
                />
            </div>
            <div className="pl-title">{pl_item.name}
                <div className="pl-songs">
                <span className="song-count">{pl_item.tracks} song/s</span>
                <img src={folder}  className="folder-style" alt="folder"/>
              </div>
            </div>
        </div>
}

export default PlaylistCards;