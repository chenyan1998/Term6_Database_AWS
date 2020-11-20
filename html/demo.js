const BASEURL = "http://127.0.0.1:8000/";

function search() {
  var search = document.querySelector("input.search").value;
  axios
    .get(BASEURL + "readbook/?title=" + search)
    .then(function (res) {
      res = res.data;
      var temp;
      var td;
      removePrevTr();
      for (var i = 0; i < res.length; i++) {
        temp = document.createElement("tr");
        temp.classList.add("addedtr");
        td = document.createElement("td");
        td.setAttribute("asin", res[i].asin);
        td.innerText = res[i].title;
        temp.appendChild(td);
        td.addEventListener("click", function () {
          window.location = "detail.html?asin=" + this.getAttribute("asin");
        });
        td = document.createElement("td");
        img = document.createElement("img");
        img.src = res[i].imUrl;
        td.appendChild(img);
        temp.appendChild(td);
        td = document.createElement("td");
        td.innerText = res[i].description;
        temp.appendChild(td);
        td = document.createElement("td");
        td.innerText = res[i].price;
        temp.appendChild(td);
        td = document.createElement("td");
        td.innerText = res[i].categories;
        temp.appendChild(td);
        document.querySelector("table").appendChild(temp);
      }
    })
    .catch(function (err) {
      console.log(err);
    });
}

function removePrevTr() {
  document.querySelectorAll(".addedtr").forEach((element) => {
    element.remove();
  });
}

function detailPage() {
  var asin = window.location.href.split("=").pop();
  //
  axios.get(BASEURL + "readreview/?asin=" + asin).then(function (r) {
    td = document.createElement("td");
    r = r.data;
    for (var j = 0; j < r.length; j++) {
      div = document.createElement("div");
      if (r[j] != null && r[j].reviewText != null) {
        div.innerText = r[j].reviewText;
        document.querySelector(".container").appendChild(div);
      }
    }
  });
  //
}
