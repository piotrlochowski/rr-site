Ext.onReady(function() {
var paragraphClicked = function(e) {
var paragraph = Ext.get(e.target);
paragraph.highlight();
Ext.MessageBox.show({
title: 'Paragraph Clicked',
msg: paragraph.dom.innerHTML,
width:400,
buttons: Ext.MessageBox.OK,
animEl: paragraph
});
}
Ext.select('p').on('click', paragraphClicked);
});

//
//Ext.onReady(function() {
//    var buttonClicked = function() {
//        Ext.Ajax.defaultHeaders = {
//            'Accept': 'application/json'
//        };
//        var resp = Ext.Ajax.request({
//            url: 'http://localhost:8000/api/v1/lap/2/?format=json',
//            method: 'GET',
//            success: function(resp) {
//                var item = Ext.decode(resp.responseText);
//                var myDiv = Ext.get('myDiv');
//                myDiv.update('The first item in the to-do list is: <br />' + item);
//            },
//            failure: function() {
//                Ext.Msg.alert('Failed');
//            },
//        });
//
//    }
//    Ext.get('myButton').on('click', buttonClicked);
//});