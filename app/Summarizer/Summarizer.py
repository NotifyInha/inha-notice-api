import re
from functools import wraps
import Summarizer.SummerizeFunctions as SummerizeFunctions


class Summarizer:
    @classmethod
    def compress(cls, text):
        text = text.strip()
        txt = re.sub('\n+', '\n', text)
        return txt

    @classmethod
    def summarize(cls, title, content):
        title = cls.compress(title)
        content = cls.compress(content)

        summarize_functions = [
            [SummerizeFunctions.clova_ai_studio,'HyperCLOVA X'],
            [SummerizeFunctions.naverapi,'CLOVA']
            # Add more summarization functions here as they are implemented
        ]

        for func, name in summarize_functions:
            try:
                result = func(title, content)
                if result:
                    return result, name
            except Exception as e:
                print(f"Error using {func.__name__}: {str(e)}")
                continue

        raise Exception("All summarization methods failed")


if __name__ == "__main__":
    content = '\n[학부-국가장학] 2024학년도 국가우수장학금(이공계_성적우수유형(1학년)) 신규장학생 선발\n\n\n\n\n 선발목적 : 우수 이공계재학생을 지원하여 이공계학업 장려 및 진출 유도\n 선발개요\n\n\n\n\n명칭\n국가우수장학금(이공계_성적우수유형)\n\n\n\n\n선발인원\n14명\n\n\n신청자격\n1. 대한민국 국적 소지자(주민등록 상 해외이주 신고자, 영주권자 제외)\n2. 2024학년도 공학/자연과학계열 및 자유전공학부 신입생\n  (과거연도 신입학 후 즉시 휴학하여 금학기가 1학년 1학기인 재학생 포함)3. 고교성적 기준충족자(수시유형) 및 수능성적 기준충족자(정시유형)\n\n\n신청제외대상\n1. 휴학생, 정규학기 내 부분등록생\n2. 타장학금(대통령과학, 인문100년, 예술체육비전, 희망사다리1,2, 국가(유공)보훈대상자,\n   북한이탈주민) 전액장학생3. 기타 한국장학재단에서 정한 신청 제외 대상\n\n\n선발기준\n1. 입학성적(80%) + 소득구간(10%) + 봉사활동(10%)\n2. 소득구간이 낮을수록 가점 부여3. 동점자 발생시 입학성적 높은순, 소득구간 낮은순, 봉사시간 높은순으로 우선 선발\n\n\n\n 선발기준(상세)\n\n 입학성적\n\n 고교성적기준(수시전형)\n\n\n\n\n구분\n유형\n성적기준\n이수단위합계\n\n\n\n\n석차등급 적용 학교\n과학고\n석차등급 6등급 이내과목\n24단위 이상\n\n\n일반고\n석차등급 3등급 이내과목\n24단위 이상\n\n\n학점 적용 학교\n영재학교\nB-학점 이상 과목\n24단위 이상\n\n\n※ 고교성적은 교내 입학 자료를 근거로 평가 실시(학생 별도 제출사항 없음)\n 수능성적기준(정시전형)\n\n\n\n\n구분\n수학\n과학탐구영역(2개과목)\n\n\n\n\n수도권대학\n1순위\n1등급\n1등급 + 1등급 또는1등급(과학Ⅱ) + 3등급이내\n\n\n2순위\n1등급\n1등급 + 3등급이내\n\n\n※ 수능성적은 교내 입학 자료를 근거로 평가 실시(학생 별도 제출사항 없음)\n\n 소득구간 및 봉사활동\n\n\n\n\n구분\n소득구간\n봉사활동\n\n\n\n\n배점\n기준\n10\n10\n\n\n구간\n점수\n구분(시간)\n점수\n\n\n기초/차상위\n10\n50 이상\n10\n\n\n1\n9\n\n\n2\n8\n50 미만 ~ 30 이상\n8\n\n\n3\n7\n\n\n4\n6\n30 미만 ~ 10 이상\n6\n\n\n5\n5\n\n\n6\n4\n10 미만\n4\n\n\n7\n3\n\n\n8\n2\n실적없음\n-\n\n\n9,10\n1\n\n\n평가\n기준\n한국장학재단에서 산출된2024-1 소득구간\n2021.3.1~2024.2.29\n봉사활동인증서\n(VMS,1365)\n\n\n\n※ 2024-1학기 한국장학재단 소득구간 미산정자는 10구간으로 간주하여 최저점 부여 (4월 16일 기준 한국장학재단 소득구간 미산정자는 이후 소득구간 확정결과에 관계없이 최저점 부여할 수 있음)\n\n 장학금 지원내용 : 계속장학생 기준 충족시 등록금 전액(정규학기기준 최대 8회)\n 신청방법 및 절차\n\n신청방법 : 제출서류를 장학복지팀으로 직접제출 or 우편제출(제출기한내 도착 기준)\n제출서류 : 장학금 신청서 (첨부파일 참조)\n제출기한 : 2024. 5. 14.(화) 18:00    (제출시간 : 평일 10시 - 18시 / 점심 12시 -13시 제외)\n제출장소\n- 직접제출시 : 인하대학교 7호관(하나은행 건물) 343호 장학복지팀\n- 우편제출시 : 위와 동일\n※우편주소 : (22212) 인천광역시 미추홀구 인하로 100 인하대학교 7호관 343호 장학복지팀 국가우수장학금 담당자\n※우편제출시 반드시 등기우편으로 송부하여야하며, 접수후 도착여부 확인 요망※우편제출시 제출기한내 도착 우편물만 인정\n\n 추후 일정(안)\n1) 선정결과 발표 : 2024.5.28.(화)2) 장학금 지급 : 2024.6월말 예정\n 기타유의사항\n본 장학금을 수혜하는 학생은 의무종사제도에 의거하여 졸업 후 연구장려금 지급횟수 x 6(개월) x 30(일) 이상 이공계 산·학·연에 의무적으로 근무해야하며 이공계 이외의 분야로 전공을 변경할 수 없으니 참고하시기 바랍니다. 관련 상세내용은 해당홈페이지에서 확인 요망 https://bit.ly/37Oo59N\n※ 자유전공학부 학생이 본 장학금 수혜 후 비이공계 학과로 진급하는경우 장학생 자격박탈 및 수혜한 장학금 전액 반환\n문의처 : 장학복지팀 문유진 (032-860-7075)\n\n'
    print(Summarizer.summarize(
        '[학부-국가장학]2024학년도 국가우수장학금(이공계_성적우수유형(1학년)) 신규장학생 선발 새글', content))
