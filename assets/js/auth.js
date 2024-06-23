$(document).ready(() => {
    $("#auth-action").on("click", () => {
        $("#auth-billboard").fadeOut(200, () => $("#auth-loader").fadeIn(200));
        makeStack("auth-log-stack", "left-side bottom-side", 8);
        $("#auth-log-stack").addClass("side-stack-text");
        addToStack("auth-log-stack", $(`<span>Started authentication request...</span>`));
    });
})