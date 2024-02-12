document.getElementById("download_screen_one").onclick = function () {
    const screenshotTarget = document.getElementById("download_screen_two");
    html2canvas(screenshotTarget).then((canvas) => {
        const base64image = canvas.toDataURL("image/png");
        var anchor = document.createElement('a');
        anchor.setAttribute("href", base64image);
        anchor.setAttribute("download", "Документ.png");
        anchor.click();
        anchor.remove();
    });
};