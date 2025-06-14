import "../css/Home.css"
import logo from '../assets/logo.png';
import Footer from "./Footer";

function Home() {
  return (
    <div className="App">
      <header>
        <img src={logo}  className="logo"  alt="Logo" />
          <p className="home-texts">Log in to your Spotify account to download your favourite playlist or insert url to download audio.</p>
          <button className="spotify-login-btn">Login With Spotify</button>
            <div class="download-bar">
                <input type="text" class="download-input" placeholder="Enter a URL"/>
                <button class="download-btn" aria-label="Download">
                    <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                    <path d="M11 3v10" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
                    <path d="M7 11l4 4 4-4" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <rect x="5" y="17" width="12" height="2" rx="1" fill="#fff"/>
                    </svg>
                </button>
            </div>   
      </header>
      <Footer/>

    </div>
  );
};

export default Home
