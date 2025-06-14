import "../css/Footer.css"


function Footer (){
    return <div className="footer-separator"> 
        <footer className="site-footer">
        <nav className="footer-links">
            <a href="/terms">Terms</a>
            <span>｜</span>
            <a href="/privacy">Privacy</a>
            <span>｜</span>
            <a href="/license">License Agreement</a>
            <span>｜</span>
            <a href="/dmca">DMCA</a>
            <span>｜</span>
            <a href="/gdpr">GDPR</a>
            <span>｜</span>
            <a href="/cookies">Cookies</a>
            <span>｜</span>
            <a href="/refund">Refund</a>
        </nav>
        <div className="footer-copyright">
            Copyright © 2014 - 2025 AmoyShare. All Rights Reserved.
        </div>
        </footer>
    </div>
};

export default Footer

