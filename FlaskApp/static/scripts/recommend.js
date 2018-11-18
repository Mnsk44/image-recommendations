
let recImgCont = $("#rec-image-container");
var selectedMethod = "category";

//for testing
let images = ["dragonfly", "moss", "mountain", "mountain2", "mountain3", "guitar"];

$(document).ready(function() {
    getRecommendations(selectedMethod, imgID);
})

$(".rec__tab").click(function(event) {
    changeMethod(event);
})


function changeMethod(e) {
    selectedMethod = e.currentTarget.dataset.tab;
    $("*.rec__tab").removeClass("rec__tab--active");
    $(`*[data-tab="${selectedMethod}"]`).addClass("rec__tab--active");
    getRecommendations(selectedMethod, imgID);
}

function getRecommendations(method, id) {
    console.log("lähetettävä data: ", method, id);
    $.ajax({
        type : "POST",
        url : "recommend",
        data : {
            method:method,
            id:id
        },
        dataType : "json",
        success : function(data) {
            console.log("palautus :", data);
            recImgCont.empty();
            for (let i = 0; i < 5; i++) {
                recImgCont.append(`
                    <div class="rec__image">
                        <a href="/image/${data[i]}">
                            <img src="/static/images/${data[i]}.jpg">
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