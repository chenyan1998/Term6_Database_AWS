const BASEURL = "http://127.0.0.1:8000";
var HAS_REVIEW;

var Main = {
  data() {
    return {
      search_text: "",
      showDetails: false,
      showAddBook: false,
      detailData: [],
      bookData: [],
      tableData: [],
    };
  },
  methods: {
    clearSearchResult: function () {
      this.tableData = [];
    },
    search_book: function () {
      var _that = this;
      if (this.search_text == "") {
        return;
      }
      this.clearSearchResult();
      axios
        .get(BASEURL + "/readbook/?title=" + this.search_text)
        .then(function (res) {
          res = res.data;
          _that.tableData = res;
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    viewDetails: function ({ row }) {
      // add reviews here
      var _that = this;
      console.log(row);
      // click to close, if the detail window is already open
      if (this.showDetails) {
        this.showDetails = false;
        return;
      }
      this.detailData = ["asin", "title", "imUrl", "description", "price"].map(
        (field) => {
          return { label: field, value: row[field] };
        }
      );
      axios
        .get(BASEURL + "/readreview?asin=" + row["asin"])
        .then(function (res) {
          res = res.data;
          console.log(res);
          HAS_REVIEW = false;
          res.forEach((element) => {
            if (!HAS_REVIEW) {
              _that.detailData.push({
                label: "Reviews",
                value: element.review,
              });
              HAS_REVIEW = true;
            } else {
              _that.detailData.push({ label: "", value: element.review });
            }
          });
        })
        .catch();
      this.showDetails = true;
    },
    addReview: function () {
      var _that = this;
      var bookAsin = document
        .querySelectorAll(".viewDetail td")[1]
        .querySelector("span").innerText;
      var reviewContent = document.querySelector(".reviewContent");
      if (reviewContent.value == "") {
        return;
      }
      console.log(reviewContent);
      axios
        .get(
          BASEURL +
            "/addreview/" +
            "?asin=" +
            bookAsin +
            "&content=" +
            reviewContent.value
        )
        .then(function (res) {
          if (HAS_REVIEW) {
            _that.detailData.push({ label: "", value: reviewContent.value });
          } else {
            _that.detailData.push({
              label: "Reviews",
              value: reviewContent.value,
            });
            HAS_REVIEW = true;
          }
          reviewContent.value = "";
          alert("Successfully add a review");
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    addBook: function () {
      this.clearSearchResult();
      this.bookData = ["title", "imUrl", "description", ""].map((field) => {
        return { label: field, value: "1" };
      });
      this.showAddBook = true;
    },
    getAddBook: function () {
      var spans = document.querySelectorAll(
        ".addBookPage.vxe-table .col--edit span"
      );
    },
  },
};

var Ctor = Vue.extend(Main);
var app = new Ctor().$mount("#app");
