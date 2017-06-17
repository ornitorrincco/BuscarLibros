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

indexApp.service('indexService', ['$http', function($http){
  this.getGandhi = function(queryParams){
    var API = 'http://localhost:8000/Gandhi';
    return $http.get(API + qp(queryParams || {}))
  }
}]);

indexApp.controller('indexController', ['$scope', 'indexService', function($scope, indexService){
  $scope.data = {};
  $scope.data.elements = [];
  $scope.search = function(){
    var queryParams = {
      q: $scope.data.search.replace(/ /g, "+").normalize('NFD').replace(/[\u0300-\u036f]/g, "")
    };
    indexService.getGandhi(queryParams).then(function(response){
      if (response.status == httpStatus.HTTP_200_OK){
        $scope.data.elements = [];
        var parser = new DOMParser();
        var doc = parser.parseFromString(response.data, "text/html");
        var items = doc.querySelectorAll('li.item');
        var name, price, author, library;
        for (var j = 0, len = items.length; j < len; j++){
            name = items[j].querySelector('h2>a').textContent;
            while ($scope.data.elements.indexOf(name) !== -1){
              name += '-';
            }
            price = items[j].querySelector('p.special-price>span.price');
            price = price ? price.textContent : "";
            author = items[j].querySelector('h3>a');
            author = author ? author.textContent : "";
            $scope.data.elements.push({
              title: name,
              price: price,
              author: author,
              library: "Gandhi"
            });
        }
        $scope.data.elements = $scope.data.elements.slice(0,20)
      }
    });
  };
}]);
