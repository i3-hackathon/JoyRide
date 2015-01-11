
var PLATFORM = new H.service.Platform({ app_id: '3DKIFtUyS48YAkTDWAqt', app_code: 'cOid823wHl_7LYvg3HWjAQ', useCIT: true });
var DEFAULT_LAYERS = PLATFORM.createDefaultLayers();

function random_int(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function semi_random(value, max_variation) {
  return (value + (Math.random() * 2 - 1) * (value * max_variation)).toFixed(1);
}

function new_point(latitude, longitude) {
  return new H.geo.Point(latitude, longitude);
}

function draw_route(map, route){
  var strip = new H.geo.Strip(),
    routeShape = route.shape,
    polyline;

  routeShape.forEach(function(point) {
    var parts = point.split(',');
    strip.pushLatLngAlt(parts[0], parts[1]);
  });

  polyline = new H.map.Polyline(strip, {
    style: {
      lineWidth: 4,
      strokeColor: 'rgba(0, 128, 255, 0.8)'
    }
  });

  map.addObject(polyline);
  map.setViewBounds(polyline.getBounds(), true);
}

function draw_points(map, points){
  var svgMarkup = '<svg width="18" height="18" ' +
    'xmlns="http://www.w3.org/2000/svg">' +
    '<circle cx="8" cy="8" r="8" ' +
      'fill="#1b468d" stroke="white" stroke-width="1"  />' +
    '</svg>',
    dotIcon = new H.map.Icon(svgMarkup, {anchor: {x:8, y:8}}),
    group = new  H.map.Group(),
    i,
    j;

  for (i in points) {
    var marker =  new H.map.Marker({
        lat: points[i].lat,
        lng: points[i].lng} ,
        {icon: dotIcon});
    group.addObject(marker);
  }

  map.addObject(group);
}

function extract_points(shape, average_speed /* [m] */, target_interval /* [s] */) {
  var distance = to_point(shape[0]).distance(to_point(shape[shape.length - 1]));
  var target_distance = average_speed * target_interval;

  var points = [];
  var i = 1;
  var j = 0;

  while (i < shape.length - 1) {
    points[j++] = to_point(shape[i]);
    current_distance = target_distance;
    while (current_distance > 0 && i < shape.length - 1) {
      current_distance -= to_point(shape[i]).distance(to_point(shape[i - 1]));
      i++;
    }
  }
  
  points[j] = to_point(shape[i]);
  return points;
}

function to_point(lat_lng) {
  var split_lat_lng = lat_lng.split(',');
  return new H.geo.Point(split_lat_lng[0], split_lat_lng[1]);
}

function scroll_to(id) {
  $('html, body').animate({
    scrollTop: ($(id).offset().top - 400)
  }, 300);
}

if (!String.format) {
  String.format = function(format) {
    var args = Array.prototype.slice.call(arguments, 1);
    return format.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number] 
        : match
      ;
    });
  };
}

