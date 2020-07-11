// Generated by CoffeeScript 1.3.1
(function() {
  var MainView, exports,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  exports = window || this;

  MainView = (function(_super) {

    __extends(MainView, _super);

    MainView.name = 'MainView';

    function MainView() {
      return MainView.__super__.constructor.apply(this, arguments);
    }

    MainView.prototype.initialize = function() {
      this.model = {
        encodings: [],
        codepoint: null,
        raw: 'A'
      };
      return this.render();
    };

    MainView.prototype.render = function() {
      var template;
      template = _.template($("#template").html(), this.model);
      return $(this.el).html(template);
    };

    MainView.prototype.events = {
      "click #lookup": "searchCharacter",
      "click #reverse_lookup": "searchCodepoint"
    };

    MainView.prototype.searchCharacter = function() {
      return this._fetchData(function(input) {
        return "/characters/utf8/" + input;
      });
    };

    MainView.prototype.searchCodepoint = function() {
      return this._fetchData(function(input) {
        return "/characters/unicode/U+" + input;
      });
    };

    MainView.prototype._fetchData = function(inputcallback) {
      var char, url,
        _this = this;
      char = $("#input").val();
      url = inputcallback(char);
      return $.get(url, null, function(data) {
        _this.model = data;
        return _this.render();
      });
    };

    return MainView;

  })(Backbone.View);

  new MainView({
    el: ".main"
  });

  exports.MainView = MainView;

}).call(this);
