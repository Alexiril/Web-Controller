$(document).ready(() => {
    addToStack("log-stack", $(`<span>Loaded authentication page.</span>`));
    $("#auth-action").on("click", () => {
        $("#auth-failed").hide();
        $("#auth-billboard").hide();
        $("#auth-loader").fadeIn(200);
        const w = $("#auth-window").get();
        window_pos_x(w, "center");
        window_pos_y(w, "center");
        addToStack("log-stack", $(`<span>Started authentication request...</span>`));
        fetch(`/$api/get-token`, {
            method: "POST",
            body: JSON.stringify({
                user: $("#auth-form-login").val(),
                key: $("#auth-form-key").val(),
                csrf: $("#csrf").val()
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then((response) => response.json()).then((json) => {
            let data = json;
            if (data.result == "done") {
                Cookies.set("token", data.value);
                addToStack("log-stack", $(`<span>Logged in successfully!</span>`));
                $("#auth-loader").hide();
                $("#auth-success").show();
                window_pos_x(w, "center");
                window_pos_y(w, "center");
                setTimeout(() => {
                    window.location.assign("/");
                }, 1000);
            }
            else {
                if (data.ecode == 0x16 || data.ecode == 0x18)
                    window.location.reload();
                addToStack("log-stack", $(`<span>Authentication error (${data.ecode}): ${data.cause}</span>`));
                let fail_text = `Sorry, authentication error occured: ${data.cause}`;
                if (data.ecode == 0x17)
                    fail_text = "Sorry, username or key (password) is incorrect.";
                $("#auth-failed").show().text(fail_text);
                $("#auth-loader").hide();
                $("#auth-billboard").fadeIn(200);
                window_pos_x(w, "center");
                window_pos_y(w, "center");
            }
        }).catch(function (err) {
            addToStack("log-stack", $(`<span>Connection error: ${err}</span>`));
            $("#auth-failed").show().text(`Sorry, connection error occured: ${err}`);
            $("#auth-loader").fadeOut(200, () => $("#auth-billboard").fadeIn(200));
        }).finally(function () {
            addToStack("log-stack", $(`<span>Authentication attempt finished.</span>`));
        });
    });
    $("#signout-action").on("click", () => {
        $("#signout-billboard").hide();
        $("#auth-loader").fadeIn(200);
        const w = $("#auth-window").get();
        window_pos_x(w, "center");
        window_pos_y(w, "center");
        addToStack("log-stack", $(`<span>Signing out...</span>`));
        setTimeout(() => {
            Cookies.set("token", "");
            window.location.reload();
        }, 500);
    });
})