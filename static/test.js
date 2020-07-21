//자스에는 simpledateformat 같은 클래스가 없기에 직접 메소드를 만듬(사실 가져옴)
Date.prototype.format = function (f) {

    if (!this.valueOf()) return " ";

    var weekKorName = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
    var weekKorShortName = ["일", "월", "화", "수", "목", "금", "토"];
    var weekEngName = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var weekEngShortName = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var d = this;

    return f.replace(/(yyyy|yy|MM|dd|KS|KL|ES|EL|HH|hh|mm|ss|a\/p)/gi, function ($1) {
        switch ($1) {
            case "yyyy": return d.getFullYear(); // 년 (4자리)
            case "yy": return (d.getFullYear() % 1000).zf(2); // 년 (2자리)
            case "MM": return (d.getMonth() + 1).zf(2); // 월 (2자리)
            case "dd": return d.getDate().zf(2); // 일 (2자리)
            case "KS": return weekKorShortName[d.getDay()]; // 요일 (짧은 한글)
            case "KL": return weekKorName[d.getDay()]; // 요일 (긴 한글)
            case "ES": return weekEngShortName[d.getDay()]; // 요일 (짧은 영어)
            case "EL": return weekEngName[d.getDay()]; // 요일 (긴 영어)
            case "HH": return d.getHours().zf(2); // 시간 (24시간 기준, 2자리)
            case "hh": return ((h = d.getHours() % 12) ? h : 12).zf(2); // 시간 (12시간 기준, 2자리)
            case "mm": return d.getMinutes().zf(2); // 분 (2자리)
            case "ss": return d.getSeconds().zf(2); // 초 (2자리)
            case "a/p": return d.getHours() < 12 ? "오전" : "오후"; // 오전/오후 구분

            default: return $1;
        }
    });
};

String.prototype.string = function (len) { var s = '', i = 0; while (i++ < len) { s += this; } return s; };
String.prototype.zf = function (len) { return "0".string(len - this.length) + this; };
Number.prototype.zf = function (len) { return this.toString().zf(len); };

function sendMessage(message) {
        $.post( "/sendMessage", {'message': message}, receiveResponse);
//        $.ajax({url:"/sendMessage",data:{'message': message},type:'post',success:receiveResponse})
        function receiveResponse(data) {
          //chat-container에 bot의 응답 추가
          var data = data.message;
          var data_message = data.split('!@#$')
            console.log(data_message);
          $('.au-chat__content').append(`
                <div class="recei-mess-wrap">
                    <span class="mess-time">`+setDate()+`</span>
                    <div class="recei-mess__inner">
                        <div class="avatar avatar--tiny">
                            <img src="/static/logo.png">
                        </div>
                        <div class="recei-mess-list">
                            <div class="recei-mess">${data_message[0]}</div>
                        </div>
                    </div>
                </div>
          `)
          scrollBottom()
          if(data_message.length>1){
              setTimeout(function() {
                  window.parent.postMessage({ childData : data_message[1] }, '*');
              }, 500);
          }

        }
    }
//메세지 보내거나 받을 시 스크롤을 맨 아래로 가게 해주는 함수
function scrollBottom(){
    $('.au-chat__content')
        .stop()
        .animate({ scrollTop: $('.au-chat__content')[0].scrollHeight }, 1000);
}
//메세지 보내는 함수
function chat_send()
{
    var query = $("#query").val()
    console.log(query)
    if (!query) {//텍스트를 입력하지 않는 경우
        $("#query").attr('placeholder','내용을 입력해주세요');
        return
    }
    //chat-container에 사용자의 응답 추가
    $('.au-chat__content').append(`
        <div class="send-mess-wrap">
            <span class="mess-time">`+setDate()+`</span>
            <div class="send-mess__inner">
                <div class="send-mess-list">
                    <div class="send-mess">${query}</div>
                </div>
            </div>
        </div>
    `)
    // 입력창 클리어
    $("#query").val('')
    $("#query").attr('placeholder','질문을 입력하세요');

    scrollBottom()
    //메시지 전송
    sendMessage(query)
}

//위에서 만든 format 함수를 통해 오전/오후 ~시/~분 형태로 시간이 나오게 함
function setDate(){
    var _today = new Date();
    return _today.format('a/p hh:mm');
}

//JQuery 부분
$("#queryButton").on('click',chat_send);
$("#query").on('keypress',function(e) {
    if (e.keyCode == 13){
        chat_send();
    }
});
$('.mess-time').html(setDate());
