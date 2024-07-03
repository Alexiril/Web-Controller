$(document).ready(() => {
    $("#back-button").attr("href", document.referrer)
    .on("click", () => {
        history.back();
        return false;
    });
})