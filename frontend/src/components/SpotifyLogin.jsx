import "../css/Home.css"


function SpotifyLogin (){

    const spotifyloginref = () => {
        window.location.href = "http://127.0.0.1:8888/spot-login";
    }
 
    return <button onClick={spotifyloginref}
    className="spotify-login-btn">Login With Spotify
    </button>
};

export default SpotifyLogin;

