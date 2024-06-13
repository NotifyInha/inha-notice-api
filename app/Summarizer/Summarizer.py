import json
import os
import requests


class Summarizer:

    @classmethod
    def summarize(cls, title, content):
        url = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": os.environ['SUMMARIZEID'],
            "X-NCP-APIGW-API-KEY": os.environ['SUMMERIZESECRET'],
            "Content-Type": "application/json",
        }

        data = {
            "document": {
                "title": title,
                "content": content
            },
            "option": {
                "language": "ko",
                "model": "general",
                "tone": 2,
                "summaryCount": 3
            }
        }

        res = requests.post(url, headers=headers,
                            data=json.dumps(data).encode('utf-8'))
        resobj = json.loads(res.text)
        if res.status_code == 200:
            return resobj['summary']
        elif res.status_code == 401:
            raise Exception("api 인증 오류")
        elif res.status_code == 400:
            raise Exception(resobj['error']['errorCode'])
        else:
            raise Exception("알 수 없는 오류")


if __name__ == "__main__":
    content = """현장실습지원센터에서는 공학계열 연구개발을 통해 국가 및 산업계 발전에 기여하는 기관 '한국철도기술연구원' 에서 2024학년도 하계방학 및 2학기 표준 현장실습학기제(Co-op)에 참여할 학생을 다음과 같이 모집합니다. 한국철도기술연구원 실습 참여자에게는 학교지원금이 확대 되었으니, 관심 있는 학생들의 많은 참여 바랍니다.



○ 실습기업 : 한국철도기술연구원

○ 기업 홈페이지 : https://www.krri.re.kr/



○ 실습기간 : 2024. 7. 1. ~ 2024. 12. 31.(6개월)

             *공고된 실습기간 전체를 이수할 수 있는 학생에 한해 신청 가능 

        

○ 접수마감 : ~ 2024. 6. 16.(일) 23:59
              *직무별 조기마감될 수 있으므로 최대한 빠른 지원 필요!!


○ 지원방법 : 현장실습온라인시스템(https://internship.inha.ac.kr/) 내 이력서 및 자소서 작성 후 온라인 지원8             

*자소서 최종본이 완성된 후 지원해 주세요! ○ 면접일정 : 2024년 6월 13일(목) 오전 10시 (교내 면접 시행 예정)

○ 실습근무지 : 경기 의왕시

○ 실습직무 :  공학계열 기술개발 등
               *세부내용 현장실습온라인시스템 내 운영계획서 확인

○ 모집인원 : 직무별 1~3명(총 20명 모집)


○ 모집학과 : 이공계열 전체학과


○ 지원자격 

 - 2024-1학기 기준 3학년 이상(학기 초과자의 경우 2024-2학기 부분등록 시 신청 가능, 2024년 8월 졸업예정자 신청불가!!)

 - 성실하고 책임감있는 학생

 - 업무에 적극적인 학생

 - 협약된 실습기간을 준수할 수 있는 학생




○ 실습지원비 : 월 1,680,740원



○ 학교지원금 : 다음 조건 충족 시, 학교 지원금(방학 기준 80만원, 학기 기준 120만원) 추가 지급(실습종료 후 지급)

+ 월 10만원 기준 학교 지원금 추가 지급!!

   1) 협약된 실습기간 이수
   2) 방학 기준 실제 출석일수 40일 이상, 학기 기준 실제 출석일수 60일 이상 충족
   3) 현장실습 학점 취득(Pass) 



○ 유의사항

  1) 실습기관에 대한 이해가 충분히 반영된 자기소개서 작성 필요

  2) 최종 선발된 학생은 다음 일정의 교내 사전교육 필수 이수해야 함(교육부 규정 필수절차)

   - 2024년 6월 26일(수) 오후 2시 / 학생회관 346호
 

  2) 학점 취득 : 방학 최대 6학점, 학기 최대 18학점 이내 신청 가능

   - 실제 전공인정학점은 학과 기준에 따르므로 소속학과로 문의(세부사항은 사전교육에서 안내함)



○ 문의 

 - Tel : 032-860-8441~8443
 - 카카오톡 플러스친구 : 인하대학교 현장실습지원센터"""
    print(Summarizer.summarize(
        "[현장실습지원센터] 2024-하계방학 및 2학기 '한국철도기술연구원' 현장실습생 모집(마감임박)", content))
