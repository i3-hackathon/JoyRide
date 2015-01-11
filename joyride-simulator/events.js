
var TRIP_ID = random_int(10, 100000);
var USER_ID = "user@domain.com";
var AVERAGE_TEMP = 75; // [F]
var API_ENDPOINT = "http://localhost:13373/joyride/event";
//var API_ENDPOINT = "http://54.83.23.239:13373/joyride/event"

var EVENTS = [];
var TIME = 0; // [s]
var NEXT_EVENT = 0;

EVENT_IDS = {
  engine_on: 1,
  engine_off: 11,
  picture: 3,
  heartbeat: 6,
  post: 10
}

TEMPLATE_ENGINE_ON = '\
  <div id="block-{0}" class="block">\
    <div class="title">Car engine ON</div>\
    <div id="event-{0}" class="event">{1}</div>\
  </div>\
';

TEMPLATE_ENGINE_OFF = '\
  <div id="block-{0}" class="block">\
    <div class="title">Car engine OFF</div>\
    <div id="event-{0}" class="event">{1}</div>\
  </div>\
';

TEMPLATE_DRIVE = '\
  <div id="block-{0}" class="block clearfix">\
    <div class="title">Drive</div>\
    <div class="left"><div class="map"></div></div>\
    <div class="right"></div>\
  </div>\
';

TEMPLATE_WALK = '\
  <div id="block-{0}" class="block clearfix">\
    <div class="title">Walk</div>\
    <div class="left"><div class="map"></div></div>\
    <div class="right"></div>\
  </div>\
';

TEMPLATE_MULTIPLE = '\
  <div id="event-{0}" class="event">{1}</div>\
';

TEMPLATE_PICTURE = '\
  <div id="event-{0}" class="block clearfix">\
    <div class="title">Picture taken</div>\
    <div class="left"><div><img src="{1}" /></div></div>\
    <div class="right"><div class="event">{2}</div></div>\
  </div>\
';

TEMPLATE_IDLE = '\
  <div id="block-{0}" class="block clearfix">\
    <div class="title">Idle for {1} minutes</div>\
    <div class="left"><div class="map"></div></div> \
    <div class="right"></div> \
  </div>\
';

function build_event(event_id, car_mph, car_gps, phone_gps, picture_data) {
  return {
    EventIndex: 0,
    EventID: EVENT_IDS[event_id],
    TripID: TRIP_ID,
    UserID: USER_ID,
    CarMPH: Math.round(car_mph),
    CarGPS: [ car_gps.lat, car_gps.lng ],
    PhoneGPS: [ phone_gps.lat, phone_gps.lng ],
    Temperature: Math.round(semi_random(AVERAGE_TEMP, 0.2)),
    PictureData: picture_data,
    CarDestination: null,
    Malfunction: false,
    Fuel: 50,
    Battery: 70,
    Timestamp: TIME,
    CarWeather: 0.0,
  }
}

function printable_event(event, fields) {
  fields = ['EventIndex', 'EventID', 'Timestamp'].concat(fields);
  filtered_event = {};
  for (i in fields) {
    key = fields[i];
    filtered_event[key] = event[key];
  }
  return JSON.stringify(filtered_event);
}

function add_events(events) {
  if (events.length == 0 || !events) {
    enable_controls();
    return;
  }
  event = events.shift();
  event[1].push(events);
  event[0].apply(this, event[1]);
}

function enable_controls() {
  console.log('trip_id', TRIP_ID);
  $('#controls BUTTON').html('Next Event').removeAttr('disabled');
}

function pause_controls() {
  $('#controls BUTTON').html('Working...').attr('disabled', 'disabled');
}

function stop_controls() {
    $('#controls BUTTON').html('Done').attr('disabled', 'disabled');
}

function simulate_next_event() {
  console.log('simulate_next_event', NEXT_EVENT);
  if (NEXT_EVENT == EVENTS.length) {
    stop_controls();
    $('#event-' + (NEXT_EVENT - 1)).removeClass('event-active').addClass('event-past');
    return;
  }

  if (NEXT_EVENT > 0) {
    $('#event-' + (NEXT_EVENT - 1)).removeClass('event-active').addClass('event-past');
  }

  pause_controls();
  scroll_to('#event-' + NEXT_EVENT);
  $('#event-' + NEXT_EVENT).addClass('event-active');
  console.log('Sending event', EVENTS[NEXT_EVENT]);
  $.ajax({
    type: "POST",
    url: API_ENDPOINT,
    data: JSON.stringify(EVENTS[NEXT_EVENT]),
    success: function(data, status) {
      console.log('event success', status, data);
      enable_controls();
    },
    error: function(jqXHR, status, error) {
      console.log('event error', status, error);
      alert('API Error: ' + status + ', ' + error);
    }
  });
  
  NEXT_EVENT++;
}

function add_event(event, duration) { 
  event["EventIndex"] = EVENTS.length;
  console.log('add_event', event, duration);
  EVENTS.push(event);
  TIME += duration;
}

function add_event_engine_on(gps, remaining_events) {
  event = build_event("engine_on", 0, gps, gps, null);
  add_event(event, 60);
  $('BODY').append(String.format(TEMPLATE_ENGINE_ON, event["EventIndex"], printable_event(event, ['CarGPS'])));
  add_events(remaining_events);
}

function add_event_engine_off(gps, remaining_events) {
  event = build_event("engine_off", 0, gps, gps, null);
  add_event(event, 60);
  $('BODY').append(String.format(TEMPLATE_ENGINE_OFF, event["EventIndex"], printable_event(event, ['CarGPS'])));
  add_events(remaining_events);
}

function add_event_drive(start_gps, end_gps, remaining_events) {
  $('BODY').append(String.format(TEMPLATE_DRIVE, EVENTS.length));
  var map = new H.Map($('#block-' + EVENTS.length + ' .map').get(0), DEFAULT_LAYERS.normal.map, { bounds: H.geo.Rect.coverPoints([start_gps, end_gps]) }); 
  generate_route(EVENTS.length, map, 'fastest;car', 15, 600, null, start_gps, end_gps, remaining_events);
}

function add_event_walk(car_gps, start_gps, end_gps, remaining_events) {
  $('BODY').append(String.format(TEMPLATE_WALK, EVENTS.length));
  var map = new H.Map($('#block-' + EVENTS.length + ' .map').get(0), DEFAULT_LAYERS.normal.map, { bounds: H.geo.Rect.coverPoints([start_gps, end_gps]) }); 
  generate_route(EVENTS.length, map, 'fastest;pedestrian', 1, 60, car_gps, start_gps, end_gps, remaining_events);
}

function add_event_picture(url, car_gps, phone_gps, remaining_events) {
  event = build_event("heartbeat", 0, car_gps, phone_gps, url);
  add_event(event, 30);
  $('BODY').append(String.format(TEMPLATE_PICTURE, event["EventIndex"], url, printable_event(event, ['CarGPS', 'PhoneGPS', 'PictureData'])));
  add_events(remaining_events);
}

function add_event_idle(car_gps, phone_gps, duration /* [minute] */, remaining_events) {
   $('BODY').append(String.format(TEMPLATE_IDLE, EVENTS.length, duration));
   var map = new H.Map($('#block-' + EVENTS.length + ' .map').get(0), DEFAULT_LAYERS.normal.map, { center: phone_gps, zoom: 16 }); 
   generate_point(EVENTS.length, map, car_gps, phone_gps, duration); 
   add_events(remaining_events);
}

function generate_point(id, map, car_gps, phone_gps, duration /* [minute] */) {
  draw_points(map, [ phone_gps ]);
  for (j = 0; j < duration; j += 5) {
    event = build_event("heartbeat", 0, car_gps, phone_gps, null);
    add_event(event, 60 * 5);
    $('#block-' + id + ' .right').append(String.format(TEMPLATE_MULTIPLE, event["EventIndex"], printable_event(event, ['CarGPS', 'PhoneGPS'])));    
  }
}

function generate_route(id, map, mode, average_speed /* [m/s] */, target_interval /* [s] */, car_gps, start_gps, end_gps, remaining_events) {
  var routeParams = { mode: mode, representation: 'display', waypoint0: start_gps.lat + ',' + start_gps.lng, waypoint1: end_gps.lat + ',' + end_gps.lng };
  
  PLATFORM.getRoutingService().calculateRoute(
    routeParams,
    function(result) {
      console.log('calculateRoute success', result);
      var route = result.response.route[0];
      draw_route(map, route);
      var points = extract_points(route.shape, average_speed, target_interval);
      draw_points(map, points);
      for (i in points) {
        var speed = car_gps != null ? 0 : semi_random(average_speed, 0.4) * 2.23693629 /* [mph] */
        var event = build_event("heartbeat", speed.toFixed(1), (car_gps != null ? car_gps : points[i]), points[i], null);
        add_event(event, target_interval);
        $('#block-' + id + ' .right').append(String.format(TEMPLATE_MULTIPLE, event["EventIndex"], printable_event(event, [ 'CarMPH', 'CarGPS', 'PhoneGPS']))); 
      }      
      add_events(remaining_events);
    },
    function(error) {
      console.log('calculateRoute error', error);
    });
}

