
let recImgCont = $("#rec-image-container");
var selectedMethod = "jaccard";
var imgWidth = $("#image-width");
var imgHeight = $("#image-height");

$(document).ready(function() {
    var im = new Image();
    im.src = "/static/images/" + imgUrl;
    getRecommendations(selectedMethod, imgUrl);

    im.onload = function() {
        imgWidth.text("Width: " + String(this.width));
        imgHeight.text("Height: " + String(this.height));
    };
    console.log(im);
})

$(".rec__tab").click(function(event) {
    changeMethod(event);
})

function changeMethod(e) {
    selectedMethod = e.currentTarget.dataset.tab;
    $("*.rec__tab").removeClass("rec__tab--active");
    $(`*[data-tab="${selectedMethod}"]`).addClass("rec__tab--active");
    getRecommendations(selectedMethod, imgUrl);
}

function getRecommendations(method, url) {
    console.log("lähetettävä data: ", method, url);
    $.ajax({
        type : "POST",
        url : "recommend",
        data : {
            method:method,
            url:url
        },
        dataType : "json",
        success : function(data) {
            console.log("palautus :", data);
            recImgCont.empty();
            for (let i = 0; i < 10; i++) {
                recImgCont.append(`
                    <div class="rec__image">
                        <a href="/image/${data[i].url}">
                            <img src="/static/images/${data[i].url}">
                            <div class="similarity__container">
                                <div class="similarity__bar" style="width:${(1 - data[i].value) * 100}%"></div>
                            </div>
                        </a>
                    </div>
                `);
            }
        },
        error: function (req, status, error) {
            console.log("ERROR: ", req, status, error);
        }
    })
}
