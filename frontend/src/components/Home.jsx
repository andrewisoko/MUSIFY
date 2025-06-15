import "../css/Home.css"
import logo from '../assets/logo.png';
import Footer from "./Footer";
import SpotifyLogin from "./SpotifyLogin";
import DownloadBar from "./DownloadBar";

function Home() {
  return (
    <div className="App">
      <header>
        <img src={logo}  className="logo"  alt="Logo" />
          <p className="home-texts">Log in to your Spotify account to download your favourite playlist or insert url to download audio.</p>
          <SpotifyLogin/>
          <DownloadBar/>
      </header>
      <Footer/>

    </div>
  );
};

export default Home;
