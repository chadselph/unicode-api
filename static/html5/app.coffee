exports = window || this

class MainView extends Backbone.View
    initialize: ->
        @model =
            encodings: []
            codepoint: null
            raw: 'A'
        @render()
    render:  ->
        template = _.template($("#template").html(), @model)
        $(@el).html(template)

    events:
        "click #lookup": "searchCharacter"
        "click #reverse_lookup": "searchCodepoint"

    searchCharacter: ->
        @_fetchData (input) -> "/characters/utf8/#{input}"

    searchCodepoint:  ->
        @_fetchData (input) -> "/characters/unicode/U+#{input}"

    _fetchData: (inputcallback) ->
        char = $("#input").val()
        url = inputcallback(char)
        $.get(url, null, (data) =>
            @model = data
            @render()
        )



new MainView({ el: ".main" })
exports.MainView = MainView
