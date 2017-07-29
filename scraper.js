// From https://morph.io/documentation
var request = require('request');
var sqlite3 = require("sqlite3").verbose();

// Fetch JSON from data.govt.nz that is caching MPs data in CSV.
// By default CKAN returns pages of 100 records, so specify a larger limit.
var url = "https://catalogue.data.govt.nz/api/action/datastore_search?resource_id=89069a40-abcf-4190-9665-3513ff004dd8&limit=200";

var mps = [];

// Open a database handle
var db = new sqlite3.Database("data.sqlite");
db.serialize(function() {

  // Create new table
  db.run("CREATE TABLE IF NOT EXISTS data (title TEXT)");

  // Insert a new record
  var statement = db.prepare("INSERT INTO data(title) VALUES (?)");
  statement.run('A new title to add');
  statement.finalize();
});

request(url, function (error, response, body) {
  if (!error && response.statusCode == 200) {

    var data = JSON.parse(body);
    //console.log(data.result.records.length);
    for (var i = 0; i < data.result.records.length; i++) {
      var record = data.result.records[i];
      var mp = {
        "name": process_name(record.Contact),
        "honorific_prefix": record["Salutation/Title (Contact)"],
        "electorate": record.Electorate,
        "sort_name": record.Contact,
        "party": record.Party
      };
      mps.push(mp);
      // Augment record with additional data.
    }
    
    //console.log('data');
    //console.log(JSON.stringify(data.result.records));
    
    //var mps_raw = data.result.records.each(function(i, entry) {
    //  console.log('i=' + i, entry);
    //});
    
    //console.log('response', response);
    console.log(JSON.stringify(mps));
  }
});

// We get name in format "surname, additional names".
function process_name(name) {
 return name;
}
