// node nzmps3.js
// post fetch processing of party_electorate and name.
var cheerio = require('cheerio');
var request = require('request');

var base = "http://www.parliament.nz";
var url = base + "/en-nz/mpp/mps/current?Criteria.ViewAll=1";

var mps = [];

// We used this in Kimono: Modify results...
function split_party_electorate(row) {
  // Split on , and trim.
  var parts = row['party_electorate'].split(',');
  row['party'] = parts[0].trim();
  row['electorate'] = parts[1].trim();
  delete row.party_electorate;
  return row;
}

function parse_name(row) {
  var parts = row.name.split(',');
  row.lastname = parts[0].trim();
  row.firstnames = parts[1].trim();
  row.name = row.firstnames + " " + row.lastname;
  return row;
}

request(url, function (error, response, body) {
  if (!error && response.statusCode == 200) {
    var $ = cheerio.load(body);

    // 
    $('.listing tr td a').each(function(i, element) {
      var name = $(this).text().trim();
      var href = $(this).attr('href');
      mps[i] = {'name': name, 'href': base + href};
    });

    $('.listing>tbody tr td:last-of-type').each(function(i, element) {
      mps[i].party_electorate = $(this).text().trim();
    });

    mps = mps.map(split_party_electorate);
    mps = mps.map(parse_name);

    console.log(JSON.stringify(mps));
  }
});
