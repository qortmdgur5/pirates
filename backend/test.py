from locust import User, task, between, events
import asyncio
import websockets
import json
import time

# 채팅룸, 파티, 유저 정보 (테스트용 데이터)
chat_room_user_map = {
    448: [2, 1],
    449: [3, 2],
    450: [5, 4],
    451: [4, 3],
    452: [6, 5],
    453: [7, 6],
    454: [8, 7],
    455: [9, 8],
    456: [10, 9],
    457: [11, 10],
    458: [12, 11],
    459: [13, 12],
    460: [14, 13],
    461: [15, 14],
    462: [16, 15],
    463: [17, 16],
    464: [18, 17],
    465: [19, 18],
    466: [20, 19],
    467: [21, 20],
    468: [22, 21],
    469: [23, 22],
    470: [24, 23],
    471: [25, 24],
    472: [26, 25],
    473: [27, 26],
    474: [28, 27],
    475: [29, 28],
    476: [30, 29],
    477: [31, 30],
    478: [32, 31],
    479: [33, 32],
    480: [34, 33],
    481: [35, 34],
    482: [36, 35],
    483: [37, 36],
    484: [80, 37],
    485: [82, 80],
    486: [84, 82],
    487: [85, 84],
    488: [86, 85],
    489: [87, 86],
    490: [88, 87],
    491: [89, 88],
    492: [90, 89],
    493: [91, 90],
    494: [92, 91],
    495: [93, 92],
    496: [94, 93],
    497: [4, 1]
}

class WebSocketUser(User):
    wait_time = between(1, 3)  # 각 유저의 요청 간격 (1~3초)
    
    def on_start(self):
        """테스트 시작 시 실행"""
        self.loop = asyncio.get_event_loop()

    @task
    def websocket_test(self):
        """WebSocket 연결 및 메시지 전송"""
        self.loop.run_until_complete(self.ws_connect())

    async def ws_connect(self):
        # 현재 유저 ID 기반으로 chat_room_user_map에서 적절한 채팅방과 유저 찾기
        user_id = self.environment.runner.user_count  # 현재 유저 수를 기반으로 user_id 생성
        chatRoom_id = None
        
        for room_id, users in chat_room_user_map.items():
            if user_id in users:
                chatRoom_id = room_id
                break

        if chatRoom_id is None:
            print(f"Error: No chat room found for user {user_id}")
            return

        uri = f"ws://localhost:9000/user/ws/chat/{chatRoom_id}/{user_id}"

        try:
            async with websockets.connect(uri) as websocket:
                start_time = time.time()  # 응답 시간 측정 시작

                # 서버에 메시지 전송
                message = json.dumps({"content": f"Hello from user {user_id}"})
                await websocket.send(message)

                # 서버 응답 수신
                response = await websocket.recv()
                response_time = int((time.time() - start_time) * 1000)  # 밀리초 변환

                # 결과 로깅
                self.environment.events.request_success.fire(
                    request_type="WebSocket",
                    name="ws/chat",
                    response_time=response_time,
                    response_length=len(response)
                )

        except Exception as e:
            self.environment.events.request_failure.fire(
                request_type="WebSocket",
                name="ws/chat",
                response_time=0,
                exception=e
            )
            
# locust -f test.py --host=http://127.0.0.1:9000