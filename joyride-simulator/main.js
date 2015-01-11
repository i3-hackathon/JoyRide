
$(document).ready(function() {
  add_events([
    [ add_event_engine_on, [ new_point(37.775946, -122.389871) ] ],
    [ add_event_drive, [ new_point(37.775946, -122.389871), new_point(36.362613, -121.900190) ] ],
    [ add_event_engine_off, [ new_point(36.362613, -121.900190) ] ],
    [ add_event_walk, [ new_point(36.362613, -121.900190), new_point(36.362613, -121.900190), new_point(36.362760, -121.898656) ] ],
    [ add_event_idle, [ new_point(36.362613, -121.900190), new_point(36.362760, -121.898656), 7 ] ],    
    [ add_event_picture, [ 'img/1.jpg', new_point(36.362613, -121.900190), new_point(36.362760, -121.898656) ] ],
  ]);
  /*add_events([
    [ add_event_walk, [ new_point(36.518360, -121.936811), new_point(37.779286, -122.402599), new_point(36.518360, -121.936811) ] ],
    [ add_event_engine_on, [ 36.518360, -121.936811 ] ],
    [ add_event_drive, [ new_point(36.518360, -121.936811), new_point(36.319998, -121.891664) ] ],
  ]);*/
});
