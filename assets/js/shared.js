$(document).ready(() => {
    $("#change-theme-button").on("click", () => {
        $("body").toggleClass('dark light');
        Cookies.set("theme", $("body").attr("class"));
    });
    $("#actual-header-bar-home-button").on("click", () => window.location.assign("/"));
})
