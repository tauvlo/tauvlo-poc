/* Tauvlo JS lib, assumes jQuery to be present and imported before this file. */

var TAUVLO_SESSION_TOKEN = "";
const TAUVLO_API_ROOT = "/api/v1";
const STELLAR_NETWORK_TYPE = "TESTNET";


class TauvloTemplates {

    static createTrustlineButton(assetCode) {
        let buttonText = "Establish trustline";
        if (assetCode == "USDC") {
            buttonText = "Establish USDC trustline";
        }
        return `
            <a href="#" class="sell-tokens-black-button w-button" onclick="TauvloUtils.setTrustline('${assetCode}');">${buttonText}</a>
        `;
    }

    static createAssetOfferRow(offerType, assetCode, amount, pricePerTokenUSDC) {
        return `
                      <div data-w-id="8cf69cf0-6e30-2d06-123b-9c7bb6b9e230" class="accordeon-header">
                        <div class="w-layout-grid property-list offers-list">
                          <div class="portfolio-grid-text">${offerType}</div>
                          <div class="portfolio-grid-text">${assetCode}</div>
                          <div class="portfolio-grid-text">${amount}</div>
                          <div class="portfolio-grid-text">\$${pricePerTokenUSDC}</div>
                        </div>
                      </div>
        `;
    }

    static createToastBarStyles() {
        return `
             /* The snackbar - position it at the bottom and in the middle of the screen */
            #snackbar {
              visibility: hidden; /* Hidden by default. Visible on click */
              min-width: 250px; /* Set a default minimum width */
              margin-left: -125px; /* Divide value of min-width by 2 */
              background-color: #323232;
              color: #fff; /* White text color */
              text-align: center; /* Centered text */
              border-radius: 2px; /* Rounded borders */
              padding: 16px; /* Padding */
              position: fixed; /* Sit on top of the screen */
              z-index: 1; /* Add a z-index if needed */
              left: 50%; /* Center the snackbar */
              bottom: 30px; /* 30px from the bottom */
            }

            #snackbar.success {
              background-color: #578b4c;
            }

            #snackbar.fail {
              background-color: #b33f3f;
            }

            /* Show the snackbar when clicking on a button (class added with JavaScript) */
            #snackbar.show {
              visibility: visible; /* Show the snackbar */
              /* Add animation: Take 0.5 seconds to fade in and out the snackbar.
              However, delay the fade out process for 2.5 seconds */
              -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
              animation: fadein 0.5s, fadeout 0.5s 2.5s;
            }

            /* Show the snackbar when clicking on a button (class added with JavaScript) */
            #snackbar.persistent.show {
              visibility: visible; /* Show the snackbar */
              /* Add animation: Take 0.5 seconds to fade in and out the snackbar.
              However, delay the fade out process for 2.5 seconds */
              -webkit-animation: fadein 0.5s;
              animation: fadein 0.5s;
            }

            /* Animations to fade the snackbar in and out */
            @-webkit-keyframes fadein {
              from {bottom: 0; opacity: 0;}
              to {bottom: 30px; opacity: 1;}
            }

            @keyframes fadein {
              from {bottom: 0; opacity: 0;}
              to {bottom: 30px; opacity: 1;}
            }

            @-webkit-keyframes fadeout {
              from {bottom: 30px; opacity: 1;}
              to {bottom: 0; opacity: 0;}
            }

            @keyframes fadeout {
              from {bottom: 30px; opacity: 1;}
              to {bottom: 0; opacity: 0;}
            }
        `;
    }

    static createMyOffersRow(offerId, offerType, assetCode, tauvloAmount, pricePerTokenUSDC) {
        return `
        <div class="property-accordeon">
          <div data-w-id="6cc1d96d-0fee-dbcd-b7ed-982d989378b3" class="accordeon-header">
            <div class="w-layout-grid property-list">
              <div class="portfolio-grid-text">${offerType}</div>
              <div class="portfolio-grid-text">${assetCode}</div>
              <div id="w-node-_6cc1d96d-0fee-dbcd-b7ed-982d989378b9-3c3c6057" class="portfolio-grid-text">${tauvloAmount}</div>
              <div id="w-node-_6cc1d96d-0fee-dbcd-b7ed-982d989378bb-3c3c6057" class="portfolio-grid-text-profit my-offers">\$${pricePerTokenUSDC}</div>
            </div>
          <div class="accordeon-icon-wrapper">
            <div class="drop-down" onclick="TauvloUtils.cancelOffer('${assetCode}', '${offerId}', '${offerType}');">Cancel ❌ </div>
          </div>
          </div>
        </div>
        `;
    }

    static createAssetRow(
        assetCode,
        amount,
        totalValue,
        totalProfitPct
    ) {
        return `
                <div class="property-accordeon">
                    <div data-w-id="dd4b68a5-7a5d-5989-d2f1-d2ae5a7f0343" class="accordeon-header">
                      <div class="w-layout-grid property-list">
                        <div class="portfolio-grid-text">${assetCode}</div>
                        <div class="portfolio-grid-text">${amount}</div>
                        <div class="portfolio-grid-text">${totalValue}</div>
                        <div class="portfolio-grid-text-profit">${totalProfitPct}</div>
                      </div>
                      <a href="/property.html?c=${assetCode}" class="w-inline-block">
                        <div class="accordeon-icon-wrapper">
                          <div class="drop-down">Details</div>
                        </div>
                      </a>
                    </div>
                  </div>
        `
    }

    static createPropertyCell(
        propertyName,
        imageUrl,
        propertyType,
        propertyStatus,
        propertySTOValue,
        propertyPricePerToken,
        propertyYieldPct,
        propertyHighlight,
        propertyAssetCode
    ) {
        return `
        <div class="w-layout-cell property-cell">
            <div class="property-card"><img src="${imageUrl}" loading="lazy" sizes="(max-width: 479px) 277.7778015136719px, 267.7778015136719px" alt="" class="card-image">
              <div class="div-block-2">
                <div class="w-layout-layout property-stack-high wf-layout-layout">
                  <div class="w-layout-cell">
                    <h5 class="location">${propertyName}</h5>
                  </div>
                  <div class="w-layout-cell">
                    <p class="card-type-or-property">${propertyType}</p>
                  </div>
                  <div class="w-layout-cell">
                    <p class="card-status-of-property">${propertyStatus}</p>
                  </div>
                </div>
                <div class="w-layout-layout proeprty-stack-low wf-layout-layout">
                  <div class="w-layout-cell">
                    <p class="price-per-token">STO Value</p>
                  </div>
                  <div class="w-layout-cell">
                    <p class="price-per-token-value">${propertySTOValue}</p>
                  </div>
                  <div class="w-layout-cell">
                    <p class="price-per-token">Price per token</p>
                  </div>
                  <div class="w-layout-cell">
                    <p class="price-per-token-value">${propertyPricePerToken}</p>
                  </div>
                  <div class="w-layout-cell">
                    <p class="yield">Yield</p>
                  </div>
                  <div class="w-layout-cell">
                    <p class="yield-value">${propertyYieldPct}</p>
                  </div>
                </div>
                <p class="property-highlight">${propertyHighlight}</p>
                <div class="w-layout-blockcontainer container-7 w-container">
                  <a href="property.html?c=${propertyAssetCode}" class="show-me-property-detail w-button">More</a>
                </div>
              </div>
            </div>
          </div>`;
    }
};

class TauvloAPI {

    static async postRequest(url, data) {
        return await $.ajax({
            "url": url,
            "type": "POST",
            "data": JSON.stringify(data),
            "dataType": "json",
            "contentType": "application/json; charset=utf-8"
        }).promise()
    }

    static async registerProperty(registerPropertyRequestData) {
        return await TauvloAPI.postRequest(TAUVLO_API_ROOT + "/property/register", registerPropertyRequestData);
    }

    static async getPropertiesPage(pageNumber, pageSize) {
        // TODO add paging support and error catching
        const response = await $.getJSON(TAUVLO_API_ROOT + "/property/list");
        return response;
    }

    static async getPropertyDetail(propertyId) {
        const response = await $.getJSON(TAUVLO_API_ROOT + "/property/" + propertyId);
        return response;
    }

    static async buyPropertyTokensXDR(
        buyingTokensAmount,
        usdcPricePerToken,
        tauvloAssetCode,
        offerId
    ) {
        let data = {
            "usdc_price_per_token": usdcPricePerToken,
            "buying_tokens_amount": buyingTokensAmount,
            "tauvlo_asset_code": tauvloAssetCode,
            "offer_id": offerId
        };
        return await TauvloAPI.postRequest(TAUVLO_API_ROOT + "/assets/buy", data)
    }

    static async sellPropertyTokensXDR(
        sellingTokensAmount,
        usdcPricePerToken,
        tauvloAssetCode,
        offerId
    ) {
        let data = {
            "selling_tokens_amount": sellingTokensAmount,
            "usdc_price_per_token": usdcPricePerToken,
            "tauvlo_asset_code": tauvloAssetCode,
            "offer_id": offerId
        };
        return await TauvloAPI.postRequest(TAUVLO_API_ROOT + "/assets/sell", data)
    }

    static async getOffersForProperty(assetCode) {
        const response = await $.getJSON(TAUVLO_API_ROOT + "/assets/offers/" + assetCode);
        return response;
    }

    static async getMyPortfolio() {
        const response = await $.getJSON(TAUVLO_API_ROOT + "/portfolio");
        return response;
    }

    static async getMyOffers() {
        const response = await $.getJSON(TAUVLO_API_ROOT + "/offers");
        return response;
    }

    static async getTrustlineXDR(assetCode) {
        const response = await $.getJSON(TAUVLO_API_ROOT + "/assets/trustline/" + assetCode);
        return response;
    }

    static async executeTransaction(transactionXDR, refreshOnSuccess) {
        TauvloUtils.showToast("Executing transaction...", null, true);
        const response = await TauvloAPI.postRequest(
            TAUVLO_API_ROOT + "/execute_transaction",
            {"transaction_xdr": transactionXDR}
        );
        if (response == null) {
            TauvloUtils.showToast("Transaction failed: No response", false);
        }
        if (response.success_flag) {
            TauvloUtils.showToast("Transaction succeeded", true);
            if (refreshOnSuccess) {
                TauvloBasicRouter.refreshPage();
            }
        } else {
            let failure_code = "Unknown error";
            console.log(response);
            try {
                failure_code = response.response.extras.result_codes.operations[0];
            } catch {}
            TauvloUtils.showToast("Transaction failed: " + failure_code, false);
        }
        return response;
    }

    static async login(username, password) {
        const response = await $.post(
            TAUVLO_API_ROOT + "/login",
            {"username": username,"password": password},
            null,
            "json"
        ).promise();
        if (response.access_token) {
            $.ajaxSetup({
                headers: {
                    'Authorization': "Bearer " + response.access_token
                }
            });
            TAUVLO_SESSION_TOKEN = response.access_token;
        }
    }
};


class TauvloWallet {

    static FR = window.freighterApi;

    static async getPublicKey() {
        return await TauvloWallet.FR.getPublicKey();
    }

    static async signTransaction(transactionXDR) {
        return await TauvloWallet.FR.signTransaction(transactionXDR, STELLAR_NETWORK_TYPE);
    }

    static async testFreighter() {
        if (await TauvloWallet.FR.isConnected()) {
            document.getElementById("freighter-test").innerHTML = "Freighter user connected, if this is your first visit, check the extension...";
            if (await TauvloWallet.FR.isAllowed()) {
                let publicKey = "N/A";
                try {
                    publicKey = await TauvloWallet.FR.getPublicKey();
                    document.getElementById("freighter-test").innerHTML = "Freighter user connected, public key: " + publicKey;
                } catch (e) {
                    error = e;
                    document.getElementById("freighter-test").innerHTML = "Freighter user connected but error occurred, check console";
                    console.log(e);
                }

            } else {
                const isAllowed = await TauvloWallet.FR.setAllowed();
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
}


class TauvloContentRenderer {

    static async renderToastBar() {
        let styleSheet = document.createElement("style")
        let snackbar = document.createElement("div");
        snackbar.id = "snackbar";
        styleSheet.innerText = TauvloTemplates.createToastBarStyles();
        document.head.appendChild(styleSheet);
        document.body.appendChild(snackbar);
    }

    static async renderPropertiesPage() {
        let pageHTML = "";
        const response = await TauvloAPI.getPropertiesPage();
        const properties = response.properties;
        for (let i=0; i<properties.length; i++) {
            const propertyData = properties[i].details;
            const propertyAssetCode = properties[i].property_id;
            pageHTML += "\n" + TauvloTemplates.createPropertyCell(
                propertyData.name,
                propertyData.image_urls[0],
                propertyData.type,
                propertyData.status,
                propertyData.sto_value,
                propertyData.price_per_token,
                propertyData.yield_irr_pct,
                propertyData.highlight_text,
                propertyAssetCode
            );
        }
        $(".property-grid").html(pageHTML);
    }

    static async renderPortfolioPage() {
        let assetsListHTML = "";
        const portfolio = await TauvloAPI.getMyPortfolio();
        const assets = portfolio.assets;
        for (let i=0; i<assets.length; i++) {
            const asset = assets[i];
            assetsListHTML += "\n" + TauvloTemplates.createAssetRow(
                asset.asset_code,
                asset.amount,
                asset.total_value,
                asset.total_profit_pct
            );
        }

        let offersListHTML = "";
        const offersResponse = await TauvloAPI.getMyOffers();
        const offers = offersResponse.offers;
        for (let i=0; i<offers.length; i++) {
            const offer = offers[i];
            offersListHTML += "\n" + TauvloTemplates.createMyOffersRow(
                offer.offer_id,
                offer.offer_type,
                offer.tauvlo_asset_code,
                offer.amount,
                offer.usdc_per_token
            );
        }
        $("#w-tabs-0-data-w-pane-0 .property-accordeon-wrapper").html(assetsListHTML);
        $("#w-tabs-0-data-w-pane-1 .property-accordeon-wrapper").html(offersListHTML);
        $(".total-balance").html(portfolio.total_balance);
        $(".total-gains").html(portfolio.total_gains);
    }

    static async renderPropertyDetailOffersList(propertyAssetCode) {
        let offersListHTML = "";
        const offersResponse = await TauvloAPI.getOffersForProperty(propertyAssetCode);
        const offers = offersResponse.offers;
        for (let i=0; i<offers.length; i++) {
            const offer = offers[i];
            offersListHTML += "\n" + TauvloTemplates.createAssetOfferRow(
                offer.offer_type,
                offer.tauvlo_asset_code,
                offer.amount,
                offer.usdc_per_token
            );
        }
        $(".property-accordeon").html(offersListHTML);
    }

    static async renderPropertyDetail() {
        const searchParams = new URLSearchParams(window.location.search);
        const propertyAssetCode = searchParams.get("c");
        if (!propertyAssetCode) {
            // TODO render 404
            return;
        }
        const propertyData = await TauvloAPI.getPropertyDetail(propertyAssetCode);

        $(".property-detail-big-thumbnail").attr("src", propertyData.details.image_urls[0]);
        $(".property-detail-big-thumbnail").attr("srcset", null);
        $(".property-detail-image").attr("src", propertyData.details.image_urls[1]);
        $(".property-detail-image").attr("srcset", null);
        $(".proeprty-detail-image-2").attr("src", propertyData.details.image_urls[2]);
        $(".proeprty-detail-image-2").attr("srcset", null);

        $("#w-node-_4fcd3e90-d39b-632d-49f0-f64d9d829467-c878b982").html(propertyData.details.tokens_issued);
        $("#w-node-_06189bd6-e66f-4992-8e3f-a294d8ff5b4c-c878b982").html(propertyData.details.price_per_token);

        $(".my-portfolio-heading").html(propertyData.details.highlight_text);
        $("#property-id").html(propertyData.property_id);
        $(".short-description").html(propertyData.details.type);
        $(".proeprty-price").html(propertyData.details.sto_value);
        $(".proeprty-status .status").html(propertyData.details.status);
        $(".yield").html(propertyData.details.yield_irr_pct);

        const portfolio = await TauvloAPI.getMyPortfolio();
        const assetTrusted = TauvloUtils.isAssetTrusted(portfolio, propertyAssetCode);
        const usdcTrusted = portfolio.usdc_trusted;

        if (!usdcTrusted) {
            $("#token-buy-sell-buttons-container").hide();
            $("#token-trustline-buttons-container").show();
            $("#token-trustline-buttons-container").html(TauvloTemplates.createTrustlineButton("USDC"));
        } else if (!assetTrusted) {
            $("#token-buy-sell-buttons-container").hide();
            $("#token-trustline-buttons-container").show();
            $("#token-trustline-buttons-container").html(TauvloTemplates.createTrustlineButton(propertyAssetCode));
        } else {
            $("#token-buy-sell-buttons-container").show();
            $("#token-trustline-buttons-container").hide();
        }

        $(".buy-tokens-button").attr("onclick", "TauvloUtils.submitBuyTokens('" + propertyAssetCode + "')");
        $(".sell-token-button").attr("onclick", "TauvloUtils.submitSellTokens('" + propertyAssetCode + "')");

        await TauvloContentRenderer.renderPropertyDetailOffersList(propertyAssetCode);
    }
};

class TauvloUtils {

    static toastTimeout = null;

    static showToast(message, success, persistent) {
        clearTimeout(TauvloUtils.toastTimeout);
        var x = document.getElementById("snackbar");
        x.innerHTML = message;
        x.className = "show";
        if (persistent) {
            x.className += " persistent";
        }
        if (success == true) {
            x.className += " success";
        } else if (success == false) {
            x.className += " fail";
        }
        if (persistent != true) {
            TauvloUtils.toastTimeout = setTimeout(function(){
                x.className = x.className.replace("show", "");
            }, 3000);
        }
    }

    static hideToast() {
        clearTimeout(TauvloUtils.toastTimeout);
        var x = document.getElementById("snackbar");
        x.className = x.className.replace("show", "");
    }

    static async walletLogin(password) {
        let loginTimeout1 = setTimeout( function() {
            TauvloUtils.showToast("Logging in with Freighter...", null, true);
        }, 1000);
        let loginTimeout2 = setTimeout( function() {
            TauvloUtils.showToast("Login with Freighter taking too long", false, true);
        }, 10000);
        let username = await TauvloWallet.getPublicKey();
        clearTimeout(loginTimeout1);
        clearTimeout(loginTimeout2);
        TauvloUtils.hideToast();
        if (username != null) {
            await TauvloAPI.login(username, password);
        } else {
            TauvloUtils.showToast("Failed to login with Freighter - please refresh the page", false, true);
        }
    }

    static async anonymousLogin(isReload) {
        if (!isReload) {
            await TauvloUtils.walletLogin("tauvlo2024");
        }
    }

    static async cancelOffer(tauvloAssetCode, offerId, offerType) {
        let transactionXDR = null;
        if (offerType == "SELLING") {
             transactionXDR = await TauvloAPI.sellPropertyTokensXDR(
                "0",
                "1",
                tauvloAssetCode,
                offerId
            );
        } else if (offerType == "BUYING") {
            transactionXDR = await TauvloAPI.buyPropertyTokensXDR(
                "0",
                "1",
                tauvloAssetCode,
                offerId
            );
        }
        let signedTransaction = await TauvloWallet.signTransaction(transactionXDR);
        if (signedTransaction) {
            return await TauvloAPI.executeTransaction(signedTransaction, true);
        }
    }

    static async setTrustline(assetCode, refreshOnSuccess) {
        let transactionXDR = await TauvloAPI.getTrustlineXDR(assetCode);
        let signedTransaction = await TauvloWallet.signTransaction(transactionXDR);
        if (refreshOnSuccess == null) {
            refreshOnSuccess = true;
        }
        if (signedTransaction) {
            return await TauvloAPI.executeTransaction(signedTransaction, refreshOnSuccess);
        }
    }

    static async sellAsset(sellingTokensAmount, usdcPricePerToken, tauvloAssetCode) {
        let transactionXDR = await TauvloAPI.sellPropertyTokensXDR(
            sellingTokensAmount,
            usdcPricePerToken,
            tauvloAssetCode
        );
        let signedTransaction = await TauvloWallet.signTransaction(transactionXDR);
        if (signedTransaction) {
            return await TauvloAPI.executeTransaction(signedTransaction, true);
        }
    }

    static async buyAsset(buyingTokensAmount, usdcPricePerToken, tauvloAssetCode) {
        let transactionXDR = await TauvloAPI.buyPropertyTokensXDR(
            buyingTokensAmount,
            usdcPricePerToken,
            tauvloAssetCode
        );
        let signedTransaction = await TauvloWallet.signTransaction(transactionXDR);
        if (signedTransaction) {
            return await TauvloAPI.executeTransaction(signedTransaction, true);
        }
    }

    static async submitSellTokens(propertyAssetCode) {
        let amount = $("#sell-amount").val();
        let pricePerToken = $("#sell-price-per-token").val();
        $("#sell-tokens-close").click();
        TauvloUtils.sellAsset(amount, pricePerToken, propertyAssetCode).then(
            () => {}
        ).catch(
            (error) => {
                console.error(error);
                TauvloUtils.showToast("Sell asset operation failed, check console for details", false);
            }
        );
    }

    static async submitBuyTokens(propertyAssetCode) {
        let amount = $("#buy-amount").val();
        let pricePerToken = $("#buy-price-per-token").val();
        TauvloUtils.buyAsset(amount, pricePerToken, propertyAssetCode).then(
            () => {}
        ).catch(
            (error) => {
                console.error(error);
                TauvloUtils.showToast("Buy asset operation failed, check console for details", false);
            }
        );
    }

    static isAssetTrusted(portfolio, assetCode) {
        if (portfolio == null || assetCode == null) {
            return null;
        }
        for (let idx in portfolio.assets) {
            let asset = portfolio.assets[idx];
            if (asset.asset_code == assetCode) {
                return true;
            }
        }
        return false;
    }

    static async registerPropertyTrustline() {
        let jsonData = null;
        let jsonString = $("#register-property-payload").val();
        try {
            jsonData = JSON.parse(jsonString);
        } catch {
            TauvloUtils.showToast("Failed to parse JSON payload", false);
            return;
        }
        await TauvloUtils.setTrustline(jsonData.property_id, false);
    }

    static async registerPropertySubmit() {
        let jsonData = null;
        let jsonString = $("#register-property-payload").val();
        try {
            jsonData = JSON.parse(jsonString);
        } catch {
            TauvloUtils.showToast("Failed to parse JSON payload", false);
            return;
        }

        TauvloAPI.registerProperty(jsonData).then(
            () => {TauvloUtils.showToast("Property registered", true);}
        ).catch(
            (error) => {
                console.error(error);
                TauvloUtils.showToast("Failed to register property, see log for details", false);
            }
        );
    }

}

class TauvloBasicRouter {

    static async renderPage(isReload) {
        let path = window.location.pathname;
        if (!isReload) {
            TauvloContentRenderer.renderToastBar();
        }
        if (path == "/index.html" || path == "/") {
            await TauvloContentRenderer.renderPropertiesPage();
        } else if (path == "/property.html") {
            await TauvloUtils.anonymousLogin(isReload);
            await TauvloContentRenderer.renderPropertyDetail();
        } else if (path == "/my-portfolio.html") {
            await TauvloUtils.anonymousLogin(isReload);
            await TauvloContentRenderer.renderPortfolioPage();
        } else if (path == "/register-property.html") {
            await TauvloUtils.anonymousLogin(isReload);
        }
    }

    static async refreshPage() {
        await TauvloBasicRouter.renderPage(true);
    }

}

TauvloBasicRouter.renderPage();
