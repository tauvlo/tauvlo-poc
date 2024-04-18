
let fr = window.freighterApi;

function getBalanceInfo(accountPublicKey) {
    fetch("/api/v1/stellar/get_balance/" + accountPublicKey)
    .then(
        response => response.json()
    ).then(jsonResponse => {
        document.getElementById("freighter-details").innerHTML = "" + JSON.stringify(jsonResponse);
    });
}

async function testFreighter() {
    if (await fr.isConnected()) {
        document.getElementById("freighter-test").innerHTML = "Freighter user connected, if this is your first visit, check the extension...";
        if (await fr.isAllowed()) {
            let publicKey = "N/A";
            try {
                publicKey = await fr.getPublicKey();
                document.getElementById("freighter-test").innerHTML = "Freighter user connected, public key: " + publicKey;
            } catch (e) {
                error = e;
                document.getElementById("freighter-test").innerHTML = "Freighter user connected but error occurred, check console";
                console.log(e);
            }

            try {
                getBalanceInfo(publicKey);
            } catch (e) {
                error = e;
                document.getElementById("freighter-details").innerHTML = "Error occurred, check console";
                console.log(e);
            }

        } else {
            const isAllowed = await fr.setAllowed();
            if (isAllowed) {
                document.getElementById("freighter-test").innerHTML = "Freighter connected and app allowed, please refresh the page";
            } else {
                document.getElementById("freighter-test").innerHTML = "Freighter connected but user has not allowed Tauvlo app";
            }
        }
    } else {
        document.getElementById("freighter-test").innerHTML = "Freighter extension unavailable";
    }
}