(function() {
    if (document.querySelector('.prototype-banner')) return;
    var banner = document.createElement('div');
    banner.className = 'prototype-banner';
    banner.innerHTML = '\u26A0\uFE0F STATIC DEMO ONLY \u2014 Client-side prototype. No backend, localStorage only. Not for production. <a href="https://github.com/Santhakumarramesh/smart-grievance-system#readme">Full app requires Flask backend</a>.';
    var style = document.createElement('style');
    style.textContent = '.prototype-banner{position:fixed;top:4px;left:0;right:0;background:#DC2626;color:white;padding:8px 16px;text-align:center;font-size:13px;font-weight:600;z-index:9999;box-shadow:0 2px 8px rgba(0,0,0,0.2)}.prototype-banner a{color:#FEF3C7;text-decoration:underline}';
    document.head.appendChild(style);
    document.body.insertBefore(banner, document.body.firstChild);
})();
