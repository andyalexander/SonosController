var sonosApp = angular.module('sonosApp',[]);
var SERVER = "http://" + location.host + "/";


sonosApp.controller('ItemCtrl',['$scope','$http',function ($scope, $http){
    var self = this;
    self.currentId = '';
    self.parentId = [''];
    self.items = [];
    self.showBack = false;
    self.type = 'genres';
    self.TABNAMES = ['Genre','Artist','Album'];

    /// determine whether to show the back button
    self.hideBack = function(){
        var hide = false;
        isTrack = false;
        if (self.items && self.items.length > 0) {
            isTrack = self.items[0].istrack;
        }

        if (self.parentId.length == 1){
            hide = true;
        }

        return hide;
    };

    self.goBack = function() {
        var temp = self.parentId[self.parentId.length-2];
        self.parentId.pop();
        self.updateCurrentId(temp);
    };


    self.updateCurrentId = function(newVal) {
        var oldVal = self.currentId;
        self.currentId = newVal;
        if (newVal && newVal.length > oldVal.length) {
            self.parentId.push(newVal);              // update the parentid for the selected item
        }
        
        if (oldVal != newVal) self.getData();
    };


    self.getData = function(){
        var id = self.currentId;
        id = encodeURI(id);
        $http.get(SERVER + 'detail' + '?id=' + id + "&type=" + self.type).
        success(function(data, status, headers, config) {
            self.items = data.items;
        }).
        error(function(data, status, headers, config) {});
    };


    self.playTrack = function(uri){
        console.log("Playing track at URI: " + uri);
        $http.get(SERVER + "playTrack?uri=" + uri);
    };

    //change sort type.  called by change in tab
    self.setType = function(newType){
        newType = newType.toLocaleLowerCase() + 's';
        if (newType == self.type) return;

        self.parentId = [''];
        self.currentId = '';
        self.type = newType;
        self.getData();

        return self.type;
    };

    self.getTabClass = function(tabName){
        var testName = tabName.toLocaleLowerCase() + 's';
        return {'tab-item': true,
            'active': this.type == testName
        };
    };

    self.playPause = function(){
        $http.get(SERVER + 'playPause');
    };
    
    // finally load the data into the initial array
    self.getData();

}]);





