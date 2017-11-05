var file = new File(["foo"], "source.csv", {
  type: "text/plain",
});

Papa.parse(file, {
  complete: function(results) {
    console.log(results);
  }
});

var results = Papa.parse(csv, {
  header: true
});
