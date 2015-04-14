// node nzmps1.js
var cheerio = require('cheerio');
var request = require('request');

var base = "http://www.parliament.nz";
var url = base + "/en-nz/mpp/mps/current?Criteria.ViewAll=1";

var mps = [];

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

    console.log(JSON.stringify(mps));
  }
});
