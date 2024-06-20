/*메가커피 - 스크린 크기와 동일한 버튼을 누르면 
1. 광고 포스터 이미지 사라짐
2. 포스터와 같은 크기의 투명한 버튼 사라짐
3. 오더 창 나타남
4. 4x3의 메뉴창 뜸
5. 페이지 표시 버튼 뜸
6. 결제 관련 페이지 뜸
7. 담은 항복 가려짐
*/
const videoOutput = document.getElementById("webcam");
const constraints = {audio: false, video: true};

navigator.mediaDevices.getUserMedia(constraints)
  .then(function(mediaStream){
    // MediaStream을 HTMLVideoElement의 srouce로 설정
    videoOutput.srcObject = mediaStream;
    // metadata가 로드될 때 실행되는 이벤트
    videoOutput.onloadedmetadata = function() {
      // HTMLVideoElement로 카메라의 화면을 출력하기 시작
      videoOutput.play();
    };
  })


function start_btn() {  
    
    fetch('/get-prediction/') // '/get-prediction/'은 AI 모델의 예측값을 반환하는 Django 뷰의 URL입니다.
        .then(response => response.json()) // 응답을 JSON 형식으로 파싱합니다.
        .then(data => {
            // 예측값에 따라 적절한 페이지를 불러옵니다.
            if (data.prediction === 'under') {
                window.location.href = '/under60/'; // '/under60/'은 Django URL 패턴입니다.
            } 
            else if (data.prediction === 'over') {
                window.location.href = '/over60/'; // '/over60/'은 Django URL 패턴입니다.
            }
            else {
                // 예외 처리: 예측값이 'under'도 'over'도 아닌 경우
                console.error('Invalid prediction value:', data.prediction);
            }
        });
}



