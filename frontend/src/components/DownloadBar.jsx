import "../css/Home.css"

function DownloadBar(){

    return  <div class="download-bar">
                <input type="text" class="download-input" placeholder="Enter a URL"/>
                <button class="download-btn" aria-label="Download">
                    <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                    <path d="M11 3v10" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
                    <path d="M7 11l4 4 4-4" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <rect x="5" y="17" width="12" height="2" rx="1" fill="#fff"/>
                    </svg>
                </button>
            </div>   
};

export default DownloadBar;