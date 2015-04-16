// Fetch PDF order paper, extract CSV using Tabula, parse CSV
// @todo: Fetch & extract!
var fs = require('fs');
var csv = require('csv');
var parse = require('csv-parse');
//var request = require('request');

var file = '/Users/jonathan/Downloads/Final-Order-Paper-for-Thursday-02-April-2015.csv';

var rows = [];
var orders = [];

var parser = parse({delimiter: ','}, function(err, data) {
  var initial = data.slice(0,30);
  //console.log(JSON.stringify(initial));
  for (i = 0; i < initial.length; i++) {
    // Tidy initial data.
    rows[i] = initial[i].map(Function.prototype.call, String.prototype.trim);
    
  }
  
  orders = parse_rows(rows);
  
});

fs.createReadStream(file).pipe(parser);

function parse_rows(rows) {
  var currentOrder = {};

  for (j = 0; j < rows.length; j++) {
    console.log('row ' + j + ':' + JSON.stringify(rows[j]));
    // iterate over each row.
    console.log('number?' + rows[j][0] + ':' + isNaN(parseInt(rows[j][0])));
    if (isNaN(rows[j][0]) == false) {
      currentOrder.order = rows[j][0];
      console.log('currentOrder=', currentOrder);
    }
    for (k = 0; k < rows[j].length; k++) {
      console.log('cell ' + k + ':' + rows[j][k]);
    }
    
  }
}
