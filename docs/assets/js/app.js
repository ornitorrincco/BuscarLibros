// TOOLS
var httpStatus = {
  HTTP_100_CONTINUE: 100,
  HTTP_101_SWITCHING_PROTOCOLS: 101,
  HTTP_200_OK: 200,
  HTTP_201_CREATED: 201,
  HTTP_202_ACCEPTED: 202,
  HTTP_203_NON_AUTHORITATIVE_INFORMATION: 203,
  HTTP_204_NO_CONTENT: 204,
  HTTP_205_RESET_CONTENT: 205,
  HTTP_206_PARTIAL_CONTENT: 206,
  HTTP_300_MULTIPLE_CHOICES: 300,
  HTTP_301_MOVED_PERMANENTLY: 301,
  HTTP_302_FOUND: 302,
  HTTP_303_SEE_OTHER: 303,
  HTTP_304_NOT_MODIFIED: 304,
  HTTP_305_USE_PROXY: 305,
  HTTP_306_RESERVED: 306,
  HTTP_307_TEMPORARY_REDIRECT: 307,
  HTTP_400_BAD_REQUEST: 400,
  HTTP_401_UNAUTHORIZED: 401,
  HTTP_402_PAYMENT_REQUIRED: 402,
  HTTP_403_FORBIDDEN: 403,
  HTTP_404_NOT_FOUND: 404,
  HTTP_405_METHOD_NOT_ALLOWED: 405,
  HTTP_406_NOT_ACCEPTABLE: 406,
  HTTP_407_PROXY_AUTHENTICATION_REQUIRED: 407,
  HTTP_408_REQUEST_TIMEOUT: 408,
  HTTP_409_CONFLICT: 409,
  HTTP_410_GONE: 410,
  HTTP_411_LENGTH_REQUIRED: 411,
  HTTP_412_PRECONDITION_FAILED: 412,
  HTTP_413_REQUEST_ENTITY_TOO_LARGE: 413,
  HTTP_414_REQUEST_URI_TOO_LONG: 414,
  HTTP_415_UNSUPPORTED_MEDIA_TYPE: 415,
  HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE: 416,
  HTTP_417_EXPECTATION_FAILED: 417,
  HTTP_428_PRECONDITION_REQUIRED: 428,
  HTTP_429_TOO_MANY_REQUESTS: 429,
  HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE: 431,
  HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS: 451,
  HTTP_500_INTERNAL_SERVER_ERROR: 500,
  HTTP_501_NOT_IMPLEMENTED: 501,
  HTTP_502_BAD_GATEWAY: 502,
  HTTP_503_SERVICE_UNAVAILABLE: 503,
  HTTP_504_GATEWAY_TIMEOUT: 504,
  HTTP_505_HTTP_VERSION_NOT_SUPPORTED: 505,
  HTTP_511_NETWORK_AUTHENTICATION_REQUIRED: 511,
  isInformational: function(code) {
    return code >= 100 && code <= 199;
  },
  isSuccess: function(code) {
    return code >= 200 && code <= 299;
  },
  isRedirect: function(code) {
    return code >= 300 && code <= 399;
  },
  isClientError: function(code) {
    return code >= 400 && code <= 499;
  },
  isServerError: function(code) {
    return code >= 500 && code <= 599;
  }
};
var qp = function(params) {
  var buff, i, j, key, keys, len;
  i = 0;
  keys = Object.keys(params);
  buff = keys.length ? '?' : '';
  for (j = 0, len = keys.length; j < len; j++) {
    key = keys[j];
    buff += key + '=' + params[key] + (i++ < keys.length - 1 ? '&' : '');
  }
  return buff;
};

// APP
var indexApp = angular.module('indexApp', []);

indexApp.service('indexService', ['$http', '$q', function($http, $q){
  this.getInfo = function(queryParams, s){
    return $q(function(resolve, reject){
      var API = s.API;
      $http.get(API + qp(queryParams || {})).then(function(response){
        if (response.status == httpStatus.HTTP_200_OK){
          var elements = [];
          var parser = new DOMParser();
          var doc = parser.parseFromString(response.data, "text/html");
          var items = doc.querySelectorAll(s.items);
          var name, price, author, library;
          for (var j = 0, len = items.length; j < len; j++){
              name = items[j].querySelector(s.name).textContent;
              price = items[j].querySelector(s.price);
              price = price ? +price.textContent.replace(/[^0-9]/g, "") : -1;
              author = items[j].querySelector(s.author);
              author = author ? author.textContent : "";
              elements.push({
                title: name,
                price: price,
                author: author,
                library: s.library
              });
          }
          resolve( elements.slice(0,15) );
        }
      }, function(response){
        reject( 'Error al comunicar con ' + s.library );
      });
    });
  };
}]);

indexApp.controller('indexController', ['$scope', 'indexService', function($scope, indexService){
  $scope.data = {};
  $scope.data.elements = [];
  $scope.data.orderBy = "price"
  $scope.search = function(){
    $scope.data.elements = [];
    var selector;
    var queryParams = {
      q: $scope.data.search.replace(/ /g, "+").normalize('NFD').replace(/[\u0300-\u036f]/g, "")
    };
    // Gandhi
    selector = {
      API: 'http://localhost:8000/BuscarLibros/Gandhi',
      items: 'li.item',
      name: 'h2>a',
      price: 'p.special-price>span.price',
      author: 'h3>a',
      library: 'Gandhi'
    };
    indexService.getInfo(queryParams, selector)
      .then(
        (response) => $scope.data.elements = $scope.data.elements.concat(response),
        (response) => console.log(response)
      );
    // El Péndulo
    selector = {
      API: 'http://localhost:8000/BuscarLibros/ElPendulo',
      items: 'div.articulo_resultado',
      name: 'h4',
      price: 'div.der_articuloResultados>p>span>span:first-of-type',
      author: 'div.der_articuloResultados>ul>li:first-of-type>a',
      library: 'El Péndulo'
    };
    indexService.getInfo(queryParams, selector)
      .then(
        (response) => $scope.data.elements = $scope.data.elements.concat(response),
        (response) => console.log(response)
      );
    // El Sótano
    selector = {
      API: 'http://localhost:8000/BuscarLibros/ElSotano',
      items: 'figure',
      name: 'p.susTit',
      price: 'span.subTit1',
      author: 'p.subTitulo',
      library: 'El Sótano'
    };
    indexService.getInfo(queryParams, selector)
      .then(
        (response) => $scope.data.elements = $scope.data.elements.concat(response),
        (response) => console.log(response)
      );
    // Fondo de Cultura Económica
    selector = {
      API: 'http://localhost:8000/BuscarLibros/FCE',
      items: 'div.row.spacer',
      name: 'span.text-titulo',
      price: 'span.text-precio',
      author: 'span.text-autor',
      library: 'FCE'
    };
    indexService.getInfo(queryParams, selector)
      .then(
        (response) => $scope.data.elements = $scope.data.elements.concat(response),
        (response) => console.log(response)
      );
  };
}]);
