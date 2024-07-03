function load_app(appid) {
    fetch(`/$api/app-request`, {
        method: "POST",
        body: JSON.stringify({
            appid: appid,
            command: 'init',
            data: {}
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then((response) => response.json()).then((json) => {
        let data = json;
        if (data.result == "done") {
            addToStack("log-stack", $(`<span>Application loaded.</span>`));
            
        }
        else {
            addToStack("log-stack", $(`<span>Application loading error (${data.ecode}): ${data.cause}</span>`));
        }
    }).catch(function (err) {
        addToStack("log-stack", $(`<span>Connection error: ${err}</span>`));
    })
}

$(document).ready(() => {
    fetch(`/$api/get-apps`, { method: "GET" })
    .then((response) => response.json())
    .then((json) => {
        let data = json;
        if (data.result == "done") {
            addToStack("log-stack", $(`<span>Applications list loaded.</span>`));
            data.value.forEach(element => {
                $("#applications-menu").append($(`
                    <md-menu-item id='app-btn-${element.id}'>
                        <div slot="headline">${element.headline}</div>
                        <md-icon slot="end" class="override-material-icons">${element.icon}</md-icon>
                    </md-menu-item>
                `));
                $(`#app-btn-${element.id}`).on("click", () => {
                    load_app(element.id);
                });
            });
        }
        else {
            addToStack("log-stack", $(`<span>Applications list loading error (${data.ecode}): ${data.cause}</span>`));
        }
    }).catch(function (err) {
        addToStack("log-stack", $(`<span>Connection error: ${err}</span>`));
    });
    $("#open-app-button").on("click", () => {
        $("#applications-menu").attr("open", true);
    });
});