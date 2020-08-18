function translate(sourceElem, destElem, sourceLang, destLang) {
    $.ajax({
        data : {
            text: $(sourceElem).text(),
            source_language: sourceLang,
            dest_language: destLang
        },
        type : 'POST',
        url : '/translate'
    })
    .done(function(response) {
        $(destElem).text(response['text'])
    })
    .fail(function() {
        $(destElem).text("{{ 'Error: Could not contact server.' }}");
    });
}