function window_pos_x(window, where) {
    if (where === "center")
        $(window).css("left", `${$("main").width() / 2 - $(window).width() / 2}px`);
    else if (where === "left")
        $(window).css("left", '20px');
    else if (where === "right")
        $(window).css("left", `${$("main").width() - $(window).width() - 20}px`);
}

function window_pos_y(window, where) {
    if (where === "center")
        $(window).css("top", `${$("main").height() / 2 - $(window).height() / 2}px`);
    else if (where === "top")
        $(window).css("top", `${$("header").height() + 40}px`);
    else if (where === "bottom")
        $(window).css("top", `${$("main").height() - $(window).height() - 20}px`);
}

$(document).ready(() => {
    $(".window").each(function () {
        window_pos_x(this, $(this).data('winInitX'));
        window_pos_y(this, $(this).data('winInitY'));
        $(this).show();
    }).on("mousedown", function (e) {
        $("main").data('dragWindow', this);
        $(this)
        .data('p0', { x: e.pageX, y: e.pageY })
        .data('orig-pos', $(this).position());
    });
    $("main").on("mousemove", function(e) {
        if ((w = $(this).data('dragWindow')) != null) {
            const orig = $(w).data('orig-pos');
            const p0 = $(w).data('p0');
            if ((next_pos = orig.left + (e.pageX - p0.x)) >= 0)
                $(w).css("left", `${next_pos}px`);
            if ((next_pos = orig.top + (e.pageY - p0.y)) >= 0)
                $(w).css("top", `${next_pos}px`);
        }
    }).on("mouseup", function (e) {
        $(this).data('dragWindow', null);
    });
    $(".window-event-blocker").on("mousedown", e => {
        e.stopPropagation();
    });
})