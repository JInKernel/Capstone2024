/*메가커피 - 스크린 크기와 동일한 버튼을 누르면 
1. 광고 포스터 이미지 사라짐
2. 포스터와 같은 크기의 투명한 버튼 사라짐
3. 오더 창 나타남
4. 4x3의 메뉴창 뜸
5. 페이지 표시 버튼 뜸
6. 결제 관련 페이지 뜸
7. 담은 항복 가려짐
*/
document.addEventListener("DOMContentLoaded", function() {
    const video = document.getElementById('webcam');
    console.log("DOM이 로드되었습니다.");

    // 미디어 장치 접근 권한 요청
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        console.log("getUserMedia 지원됨");
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            console.log("스트림을 가져왔습니다.");
            // 스트림을 비디오 요소에 설정
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error("웹캠 접근 에러: ", error);
        });
    } else {
        console.error("이 브라우저는 getUserMedia를 지원하지 않습니다.");
    }
});



function start_btn() {  

    navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        // 웹캠 스트림을 비디오 요소에 연결합니다.
        const video = document.createElement('video');
        if (video === null) {
            console.error('Video element could not be created');
            return;
        }
        video.srcObject = stream;
        video.play();
        // 비디오가 재생되면 한 프레임을 캡처합니다.
        video.onplaying = () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // 캔버스에서 이미지 데이터를 추출합니다.
            const imageData = canvas.toDataURL('image/png');

            // CSRF 토큰을 가져옵니다.
            let csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
            let csrftoken = csrfCookie ? csrfCookie.split('=')[1] : '';

            // 이미지 데이터를 서버로 전송합니다.
            fetch('/get-prediction/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ image: imageData }),
            })
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
        };
    });
}



