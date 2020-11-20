const BASEURL = "http://127.0.0.1:8000";

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
      if (this.search_text == "") {
        return;
      }
      this.clearSearchResult();
      axios
        .get(BASEURL + "/readbook/?title=" + this.search_text)
        .then(function (res) {
          res = res.data;
          console.log(res)
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    viewDetails: function ({ row }) {
      // add reviews here
      console.log(row);
      // click to close, if the detail window is already open
      if (this.showDetails) {
        this.showDetails = false;
        return;
      }
      this.detailData = ["name", "role", "num", "num1"].map((field) => {
        return { label: field, value: row[field] };
      });
      this.showDetails = true;
    },
    addBook: function () {
      this.clearSearchResult();
      this.bookData = ["name", "role", "num", "num1"].map((field) => {
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
