$(document).ready(() => {
    $("#change-theme-button").on("click", () => {
        $("body").toggleClass('dark light');
        Cookies.set("theme", $("body").attr("class"));
    });
    $("#home-button").on("click", () => window.location.assign("/"));
    $("#controller-settings-button").on("click", () => window.location.assign("/controller-settings"));
    $("#profile-settings-button").on("click", () => window.location.assign("/profile-settings"));
})
