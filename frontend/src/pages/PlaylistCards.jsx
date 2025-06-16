import "../css/PlaylistCards.css"
//    downloading process here

function PlaylistCards({pl_item}){
           

    return <div className="pl-card"> 
            <div className="pl-poster">
                <img src={pl_item.url} 
                     alt={pl_item.name}
                />
            </div>
            <div className="pl-title">{pl_item.name}
                <p className="pl-songs">{`${pl_item.tracks} songs`}</p>
            </div>
        </div>
}

export default PlaylistCards;