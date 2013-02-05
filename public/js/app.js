$(document).ready( function() {
  'use strict';

  // Template directory
  infuser.defaults.templateUrl = "templates";

  var isPlaying = false;

  // --------------
  // Models
  //---------------

  // Represents a single radio station item
  var RadioStation = function( station ) {
    this.id = station.id;
    this.name = ko.observable(station.name);
    this.mrl = ko.observable(station.mrl);
    this.website = ko.observable(station.website);
    this.logo = ko.observable(station.logo);
    this.genre = ko.observable(station.genre);
    this.lastPlayed = ko.observable(station.last_played);
    this.plays = ko.observable(station.plays);
    this.favorite = ko.observable(station.favorite);
    this.myStation = ko.observable(station.myStation);
  };

  var GoogleMusicSong = function( song ) {
    this.id = song.id;
    this.title = ko.observable(song.title);
    this.artist = ko.observable(song.artist);
    this.album = ko.observable(song.album);
  };

  var AppSettings = function( settings ) {
    this.gmUsername = ko.observable(settings.gmUsername);
    this.gmPassword = ko.observable(settings.gmPassword);
  };

  // Obsolete! Info about the currently playing song/radio station
  var ServerInfo = function( info ) {
    this.artist = ko.observable();
    this.song = ko.observable();
  };

  // Info about the currently playing song/radio
  var CurrentlyPlaying = function( url ) {
    this.url = ko.observable(url);
  };

  // Our main view model
  var ViewModel = function( radioStations ) {
    var self = this;

    // Page Sections
    self.sections = [
                          {
                            name: "Start Page",
                            link: "StartPage",
                            template: "startPage",
                            subsections: [] 
                          },
                          {
                            name: "Internet Radio",
                            link: "InternetRadio",
                            template: "rdMyStations",
                            subsections: [
                                          {
                                            name: "My Stations",
                                            link: "MyStations",
                                            template: "rdMyStations"
                                          },
                                          {
                                            name: "Radio Stations",
                                            link: "Stations",
                                            template: "rdStations"
                                          }
                                         ]
                          },
                          {
                            name: "Google Music",
                            link: "GoogleMusic",
                            template: "gmTitles",
                            subsections: [
                                          {
                                            name: "Titles",
                                            link: "titles",
                                            template: "gmTitles"
                                          },
                                          {
                                            name: "Artists",
                                            link: "artists",
                                            template: "gmArtists"
                                          },
                                          {
                                            name: "Albums",
                                            link: "albums",
                                            template: "gmAlbums"
                                          },
                                          {
                                            name: "Genres",
                                            link: "genres",
                                            template: "gmGenres"
                                          }
                                         ]
                          }
                        ];
    self.appSettings = ko.observable();
    self.isPlaying = ko.observable(false);
    self.activeRadioStation = ko.observable();
    self.chosenSection = ko.observable();
    self.chosenSubSection = ko.observable();
    self.activeSubSections = ko.observable();
    self.selectedTemplate = ko.observable();
    self.editedRadioStation = ko.observable();
    self.radioStationToDelete = ko.observable();

    // Map array of passed radio stations to an observableArray of RadioStations objects
    self.radioStations = ko.observableArray(ko.utils.arrayMap( radioStations, function( station ) {
      return new RadioStation( station );
    }));

    // This function loads the google music library
    var getGoogleMusicLibrary = function() {
      $.getJSON('/api/gm', function( data ) {
        self.googleMusicLibrary = ko.observableArray(ko.utils.arrayMap( data, function( song ) {
          return new GoogleMusicSong( song );
        }));
      });
    }

    // Get the google music library
    getGoogleMusicLibrary();

    // This function loads the app settings from the server
    var getAppSettings = function() {
      $.getJSON('/api/settings', function( data ) {
        self.appSettings(new AppSettings(data));
      });
    }

    // Load app settings
    getAppSettings();

    // My radio stations
    self.myStations = ko.computed(function() {
      var myStations = new Array();
      $.each(self.radioStations(), function(index, station) {
        if (station.myStation()) {
          myStations.push(station);
        }
      });

      return myStations;
    });

    self.goToSection = function( section ) {
      location.hash = section.link;
    }

    self.goToSubsection = function( subsection ) {
      location.hash = self.chosenSection().link + "/" + subsection.link;
    }

    self.goToSettings = function() {
      location.hash = "#settings";
    }

    self.saveSettings = function( ) {
      $.ajax({
        url: "/api/settings",
        type: "POST",
        data: ko.toJS(self.appSettings()),
        dataType: "JSON",
        success: function( data ) {

        }
      });
    }

    self.playStation = function( station ) {
      $.ajax({
        url: "/api/play_station",
        type: "POST",
        data: { mrl: station.mrl },
        dataType: "JSON",
        success: function( data ) {
          isPlaying = true;
          self.isPlaying = true;
          $('#playPause i').attr('class', 'icon-white icon-pause');
        }
      });
    }

    self.addStation = function( formElement ) {
      var name = $('#stationName').val();
      var mrl = $('#mrl').val();
      var website = $('#website').val();
      var logo = $('#logo').val();

      var newStation = {
        name: name,
        mrl: mrl,
        website: website,
        logo: logo
      };

      // Send the new radio station to the server and receive the created station
      var data = ko.toJS(newStation);
      $.ajax({
        url: "/api/stations",
        type: "POST",
        data: data,
        dataType: "JSON",
        success: function( data ) {
          var station = new RadioStation(data);
          self.radioStations.push(station);
        }
      });

      // Reset all dialog values
      $('#stationName').val("");
      $('#mrl').val("");
      $('#website').val("");
      $('#logo').val("");

      // Close the dialog
      $('#add-station-modal').modal('hide');
    }

    self.updateStation = function( station ) {
      var data = ko.toJS(station);
      $.ajax({
        url: "/api/stations/" + station.id,
        type: "PUT",
        data: data,
        dataType: "JSON",
        success: function( data ) {
        }
      });
    }

    self.deleteStation = function( station ) {
      self.radioStations.remove(station);

      $.ajax({
        url: "/api/stations/" + station.id,
        type: "DELETE",
        dataType: "JSON",
        success: function( data ) {
        }
      });
    }

    self.setVolume = function( volume ) {
      var data = {
        volume: volume
      };

      $.ajax({
        url: "/api/volume",
        type: "POST",
        data: ko.toJS(data),
        dataType: "JSON",
        success: function( data ) {
          // TODO
        }
      });
    }

    self.editStation = function( station ) {
      // Set the station to edit
      self.editedRadioStation(station);
    }

    self.onRadioStationEdit = function( ) {
      // Close the dialog
      $('#edit-station-modal').modal('hide');

      // Update the radio station
      var station = self.editedRadioStation();
      self.updateStation(station);
    }

    self.addStationToMyStations = function( station ) {
      var index = self.radioStations().indexOf(station);
      var rds = self.radioStations()[index];
      rds.myStation(true);
      self.updateStation(rds);
    }

    self.removeStationFromMyStations = function( station ) {
      var index = self.radioStations().indexOf(station);
      var rds = self.radioStations()[index];
      rds.myStation(false);
      self.updateStation(rds);
    }

    self.setRadioStationToDelete = function( station ) {
      self.radioStationToDelete(station);
    }

    self.onRadioStationDelete = function( modalId ) {
      // Delete the radio station
      self.deleteStation(self.radioStationToDelete());

      // Hide modal
      $('#' + modalId).modal('hide');
    }

    self.playGoogleMusicSong = function( song ) {
       $.ajax({
        url: "/api/play_gm_song",
        type: "POST",
        data: { id: song.id },
        dataType: "JSON",
        success: function( data ) {
          isPlaying = true;
          self.isPlaying = true;
          $('#playPause i').attr('class', 'icon-white icon-pause');
        }
      });
    }

    self.onSaveSettings = function() {
      self.saveSettings();
    }

    // Resets the given form
    self.resetForm = function ( formId ) {
      var form = $('#' + formId);
      form.validate().resetForm();
      form.get(0).reset();
    }

    // Routing
    Sammy(function() {
      this.get('#:section', function() {
        var section = this.params.section;

        // Check if the settings site was called
        if (section == "settings") {
          self.selectedTemplate('settings');
          return;
        }

        // Get section entry by hash name
        $.each(self.sections, function(index, value) {
          if (value.link == section) {
            // Set the selected section
            self.chosenSection(value);
            // Set the subsections
            self.activeSubSections(value.subsections);
            // Set template
            self.selectedTemplate(value.template)
          }
        });
      });

      this.get('#:section/:subsection', function() {
        var selectedSection = this.params['section'];
        var selectedSubsection = this.params['subsection'];
        $.each(self.sections, function(index, section) {
          if (section.link == selectedSection) {
            $.each(section.subsections, function(subIndex, subsection) {
              if (subsection.link == selectedSubsection) {
                self.chosenSection(section);
                self.chosenSubSection(subsection);
                self.selectedTemplate(subsection.template);
              }
            });
          }
        });
      });

      this.get('', function() { this.app.runRoute('get', '#StartPage') });
    }).run();
  }

  // Initial load of all available radio stations
  var viewModel;
  $.getJSON('/api/stations', function( data ) {
    viewModel = new ViewModel( data );
    ko.applyBindings( viewModel );
  });

  // View model for the add radio station modal dialog
  var AddRadioStationViewModel = function() {
    var self = this;

    self.name = ko.observable();
    self.mrl = ko.observable();
    self.website = ko.observable();
    self.logo = ko.observable();

    // The name of the template to render
    self.template = "addRadioStationModal";

    self.add = function() {
      var newStation = {
        name: self.name(),
        mrl: self.mrl(),
        website: self.website(),
        logo: self.logo()
      };
      self.modal.close(newStation);
    };

    self.cancel = function() {
      self.modal.close();
    };
  }

  //---------------
  // UI functions
  //---------------

  $('#playPause').click(function() {
    if (isPlaying) {
      $.getJSON('/api/pause', function(data){
        isPlaying = false;

        // Change the start button icon
        $('#playPause i').attr('class', 'icon-white icon-play');
      });
    }
    else {
      $.getJSON('/api/start', function(data){
        isPlaying = true;

        // Change the start button icon
        $('#playPause i').attr('class', 'icon-white icon-pause');
      });
    }
  });

  // Gets info about the current playing song/station
  function updateSongInfos() {
    $.getJSON('/api/song', function(data) {
      var station = data.station;
      var song = data.song;

      $("#title_label").text(station);
      $("#song_label").text(song);
    });

    setTimeout(updateSongInfos, 1000);
  }

  // Start updating
  updateSongInfos();

  // Radio Stations Tab
  $("#radio-stations-tab a[href=#my-stations-tab]").click(function(e) {
    e.preventDefault();
    $(this).tab('show');
  });

  $("#radio-stations-tab a[href=#browse-radio-stations-tab]").click(function(e) {
    e.preventDefault();
    $(this).tab('show');
  });

  // Volume control
  var volume_slider = $('#volume-slider');
  var tooltip = $('.tooltip');
  volume_slider.slider({
    range: "min",
    min: 1,
    value: 50,

    start: function(event, ui) {
      tooltip.fadeIn('fast');
    },

    slide: function(event, ui) {
      var value = volume_slider.slider('value');
      var volume = $('.volume');

      tooltip.css('left', value).text(ui.value);

      if (value <= 10) {
        volume.css('background-position', '0 0');
      }
      else if (value <= 25) {
        volume.css('background-position', '0 -27px');
      }
      else if (value <= 75) {
        volume.css('background-position', '0 -54px');
      }
      else {
        volume.css('background-position', '0 -81px');
      }

      // Send volume to server
      viewModel.setVolume(value);
    },

    stop: function(event, ui) {
      tooltip.fadeOut('fast');
    }
  });

  //////////////
  // Helper functions
  /////////////

  var createModalElement = function(templateName, viewModel) {
    var temporaryDiv = addHiddenDivToBody();
    var deferredElement = $.Deferred();
    ko.renderTemplate(
        templateName,
        viewModel,
        // We need to know when the template has been rendered,
        // so we can get the resulting DOM element.
        // The resolve function receives the element.
        {
            afterRender: function (nodes) {
                // Ignore any #text nodes before and after the modal element.
                var elements = nodes.filter(function(node) {
                     return node.nodeType === 1; // Element
                });
                deferredElement.resolve(elements[0]);
            }
        },
        // The temporary div will get replaced by the rendered template output.
        temporaryDiv,
        "replaceNode"
    );
    // Return the deferred DOM element so callers can wait until it's ready for use.
    return deferredElement;
  };

  var addHiddenDivToBody = function() {
    var div = document.createElement("div");
    div.style.display = "none";
    document.body.appendChild(div);
    return div;
  };

  var showModal = function(options) {
    if (typeof options === "undefined") throw new Error("An options argument is required.");
    if (typeof options.viewModel !== "object") throw new Error("options.viewModel is required.");

    var viewModel = options.viewModel;
    var template = options.template || viewModel.template;
    var context = options.context;

    if (!template) throw new Error("options.template or options.viewModel.template is required.");

    return createModalElement(template, viewModel)
      .pipe($) // jQueryify the DOM element
      .pipe(function($ui) {
        var deferredModalResult = $.Deferred();
        addModalHelperToViewModel(viewModel, deferredModalResult, context);
        showTwitterBootstrapModal($ui);
        whenModalResultCompleteThenHideUI(deferredModalResult, $ui);
        whenUIHiddenThenRemoveUI($ui);
        return deferredModalResult;
      });
  };

  var addModalHelperToViewModel = function (viewModel, deferredModalResult, context) {
    // Provide a way for the viewModel to close the modal and pass back a result.
    viewModel.modal = {
      close: function (result) {
        if (typeof result !== "undefined") {
          deferredModalResult.resolveWith(context, [result]);
        } else {
          // When result is undefined, we don't want any `done` callbacks of
          // the deferred being called. So reject instead of resolve.
          deferredModalResult.rejectWith(context, []);
        }
      }
    };
  };

  var showTwitterBootstrapModal = function($ui) {
    // Display the modal UI using Twitter Bootstrap's modal plug-in.
    $ui.modal({
      // Clicking the backdrop, or pressing Escape, shouldn't automatically close the modal by default.
      // The view model should remain in control of when to close.
      backdrop: "static",
      keyboard: false
    });
  };

  var whenModalResultCompleteThenHideUI = function (deferredModalResult, $ui) {
    // When modal is closed (with or without a result)
    // Then always hide the UI.
    deferredModalResult.always(function () {
      $ui.modal("hide");
    });
  };

  var whenUIHiddenThenRemoveUI = function($ui) {
    // Hiding the modal can result in an animation.
    // The `hidden` event is raised after the animation finishes,
    // so this is the right time to remove the UI element.
    $ui.on("hidden", function() {
      // Call ko.cleanNode before removal to prevent memory leaks.
      $ui.each(ko.cleanNode);
      $ui.remove();
    });
  };

});

