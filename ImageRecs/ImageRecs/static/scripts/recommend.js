
let recImgCont = $("#rec-image-container");
var selectedMethod = "category";

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
                        <a href="/image/${data[i].name}">
                            <img src="/static/images/${data[i].name}.jpg">
                            <div class="similarity__container">
                                <div class="similarity__bar" style="width:${data[i].sim*100}%"></div>
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