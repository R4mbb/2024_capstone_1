import aiohttp
import asyncio
import aiofiles  # 비동기 파일 처리를 위한 라이브러리
import json

api_key = "328f86764abe3a3565fbcfb8fa2490b7d6b20dca6d1f9c673dc5a897948d6d03"
url = "https://www.virustotal.com/api/v3/files"

# 요청 제한을 위한 세마포어 (동시 요청 수를 4개로 제한)
semaphore = asyncio.Semaphore(4)

# 비동기로 파일 업로드 및 분석 결과 확인하는 함수
async def upload_and_analyze(session, i):
    async with semaphore:  # 동시 요청 수 제한 적용
        i = i.upper()
        json_name = f'json/{i[:-1]}.json'

        async with aiofiles.open(json_name, 'w', encoding='utf-8') as f2:
            file_name = f'sample/{i[:-1]}'

            # 파일 읽기
            async with aiofiles.open(file_name, 'rb') as f:
                file_data = await f.read()

            # 파일 업로드 요청을 위한 데이터 구성
            form = aiohttp.FormData()
            form.add_field('file', file_data, filename=i)

            headers = {
                "accept": "application/json",
                "x-apikey": api_key
            }

            # 파일 업로드
            async with session.post(url, data=form, headers=headers) as response:
                if response.status == 200:
                    upload_result = await response.json()
                    if "data" in upload_result:
                        analysis_id = upload_result["data"]["id"]
                        print(f"File uploaded successfully. Analysis ID: {analysis_id}")

                        # 25초 대기 후 분석 결과 확인 (API 요청 제한 맞추기 위해)
                        await asyncio.sleep(25)  # 25초 대기

                        # 분석 결과 확인 URL
                        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

                        # 분석 상태를 주기적으로 확인
                        for _ in range(35):  # 최대 35회까지 시도
                            async with session.get(analysis_url, headers=headers) as response:
                                if response.status == 200:
                                    analysis_result = await response.json()
                                    status = analysis_result["data"]["attributes"]["status"]

                                    if status == "completed":
                                        print("Analysis completed!")
                                        stats = analysis_result["data"]["attributes"]["stats"]
                                        filtered_stats = {
                                            "malicious": stats["malicious"],
                                            "undetected": stats["undetected"]
                                        }
                                        await f2.write(json.dumps(filtered_stats, indent=4))
                                        break
                                    else:
                                        print(f"Analysis still in progress, status: {status}. Retrying in 15 seconds...")
                                        await asyncio.sleep(25)  # 다시 요청 전에 25초 대기
                                else:
                                    print(f"Failed to get analysis result. Status code: {response.status}")
                                    break

                        else:
                            print("Analysis did not complete within the time limit.")
                    else:
                        print("Upload response does not contain 'data'. Check the response:", upload_result)
                else:
                    print(f"Failed to upload file. Status code: {response.status}")
                    print(await response.text())  # 추가적인 오류 메시지 출력

# 비동기로 파일 처리 작업을 수행하는 메인 함수
async def main():
    async with aiohttp.ClientSession() as session:
        with open('./train.txt', 'r', encoding='utf-8') as f1:
            content = f1.readlines()

        # 각 파일에 대한 작업을 비동기로 처리
        tasks = [upload_and_analyze(session, i) for i in content]
        await asyncio.gather(*tasks)

# asyncio 이벤트 루프 실행
if __name__ == "__main__":
    asyncio.run(main())

