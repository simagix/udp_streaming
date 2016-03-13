/**
 * controller.js
 * Author: Ken Chen
 */
var app = angular.module('stream', ['ui.bootstrap']);

app.controller('StreamController', function($scope, $http, $log) {
    angular.element(document).ready(function() {
        $log.info('ready!');
        $scope.getTitles();
    });

    $scope.title = 'Select ...';
    $scope.titles = [];

    $scope.getTitles = function() {
        var url = '/streaming/titles';
        $http.get(url).success(function(data) {
            $scope.titles = data;
        });
    }

    $scope.titleSelected = function(doc) {
        var url = '/streaming/udp/remote/1234/' + doc.index;
        $scope.title = doc.title;
        $http.post(url).success(function(data) {
            $log.info('playing ... ' + JSON.stringify(data));
            var uri = 'udp://@:1234';
            var video = document.getElementById('video');
            video.playlist.clear();
            video.playlist.add(uri);
            video.playlist.play(); 
        });
    }
});

