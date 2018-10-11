(function() {

    // ignore clicks if the input is empty
    $("#search-button").click(function(event) {
        if ($.trim($("#search-input").val()) == "") {
            event.preventDefault();
        }
    });

    // workaround to fix font-rendering problem in Android Chrome
    WebFontConfig = { google: { families: ["Lato", "PT Sans"] } };
    $.getScript("//ajax.googleapis.com/ajax/libs/webfont/1/webfont.js");

}());
