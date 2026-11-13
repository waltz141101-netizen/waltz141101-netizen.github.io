/* 샘플 회원(가상) — 세팅이 끝나면 지워도 됨. 새 회원은 CLAUDE.md '새 회원 PT 노트 만들기' */
window.MEMBER = {
  "name": "홍길동",
  "sex": "M",
  "since": "2026. 11",
  "goal": "근비대 · 주 6회 (샘플 회원)",
  "journey": {
    "start": "2026-09-15"
  },
  "notices": [
    {
      "date": "2026. 11. 11",
      "title": "PT 노트가 열렸어요",
      "body": "이건 샘플 회원 노트예요. 세팅이 끝나면 지워도 돼요."
    }
  ],
  "next_class": null,
  "forms": [],
  "routine": {
    "version": "v4",
    "updated": "2026. 11. 5",
    "title": "주 6회 · 근비대",
    "plan": [
      "가슴·등·하체 주 2번씩",
      "같은 종목, 무게만 조금씩 ↑",
      "일요일은 푹 쉬고 잘 먹기"
    ],
    "key_point": "지금 방향 맞아요! 루틴대로 하고 무게만 조금씩 올리기",
    "note": "덤벨 무게는 한 손 기준이에요",
    "cardio": {
      "minutes": 15,
      "options": "경사 걷기 · 천국의 계단 · 사이클 중 택1"
    },
    "days": [
      {
        "day": "월",
        "part": "가슴",
        "en": "Chest",
        "cardio": true,
        "items": [
          {
            "name": "플랫 덤벨프레스",
            "en": "Flat DB Press",
            "tag": "메인",
            "tip": "덤벨은 가슴 옆까지",
            "sets": [
              [
                15,
                8
              ],
              [
                12,
                8
              ],
              [
                10,
                10
              ],
              [
                8,
                10
              ]
            ]
          },
          {
            "name": "인클라인 덤벨 프레스",
            "en": "Incline DB Press",
            "tip": "윗가슴으로 밀기",
            "sets": [
              [
                12,
                8
              ],
              [
                12,
                8
              ],
              [
                12,
                8
              ]
            ]
          },
          {
            "name": "케이블 푸쉬다운",
            "en": "Cable Pushdown",
            "tip": "팔꿈치 옆구리 고정",
            "sets": [
              [
                15,
                15
              ],
              [
                15,
                15
              ],
              [
                15,
                15
              ]
            ]
          }
        ]
      },
      {
        "day": "화",
        "part": "등",
        "en": "Back",
        "cardio": true,
        "items": [
          {
            "name": "시티드 페이스풀",
            "en": "Seated Face Pull",
            "tag": "워밍업",
            "tip": "팔꿈치 높게 얼굴 쪽으로",
            "sets": [
              [
                20,
                10
              ],
              [
                15,
                15
              ]
            ]
          },
          {
            "name": "랫풀다운",
            "en": "Lat Pulldown",
            "tag": "메인",
            "tip": "팔꿈치로 당기기",
            "sets": [
              [
                15,
                25
              ],
              [
                12,
                25
              ],
              [
                10,
                30
              ],
              [
                8,
                30
              ]
            ]
          },
          {
            "name": "뉴텍 시티드 로우 머신",
            "en": "Seated Row Machine",
            "tip": "가슴 패드 붙이고 당기기",
            "sets": [
              [
                12,
                30
              ],
              [
                12,
                30
              ],
              [
                12,
                30
              ]
            ]
          },
          {
            "name": "리버스 펙덱",
            "en": "Reverse Pec Deck",
            "tip": "날개뼈 모으며 옆으로",
            "sets": [
              [
                15,
                15
              ],
              [
                15,
                15
              ],
              [
                15,
                15
              ]
            ]
          }
        ]
      },
      {
        "day": "수",
        "part": "하체",
        "en": "Legs A",
        "cardio": false,
        "items": [
          {
            "name": "레그 익스텐션",
            "en": "Leg Extension",
            "tag": "워밍업",
            "tip": "가볍게 무릎 풀기",
            "sets": [
              [
                20,
                15
              ],
              [
                15,
                20
              ]
            ]
          },
          {
            "name": "이너타이",
            "en": "Inner Thigh",
            "tag": "선행",
            "tip": "세트마다 무게 ↑",
            "sets": [
              [
                20,
                20
              ],
              [
                15,
                25
              ],
              [
                12,
                30
              ]
            ]
          },
          {
            "name": "아웃타이 머신",
            "en": "Outer Thigh",
            "tag": "선행",
            "tip": "세트마다 무게 ↑",
            "sets": [
              [
                20,
                20
              ],
              [
                15,
                25
              ],
              [
                12,
                30
              ]
            ]
          },
          {
            "name": "고블릿 스쿼트",
            "en": "Goblet Squat",
            "tag": "선행",
            "tip": "가슴 세우고 깊이 앉기",
            "sets": [
              [
                20,
                6
              ],
              [
                15,
                8
              ],
              [
                12,
                10
              ]
            ]
          },
          {
            "name": "핵스쿼트",
            "en": "Hack Squat",
            "tag": "메인",
            "tip": "등 패드에 붙이고",
            "sets": [
              [
                15,
                15
              ],
              [
                12,
                15
              ],
              [
                10,
                20
              ],
              [
                8,
                20
              ]
            ]
          }
        ]
      },
      {
        "day": "목",
        "part": "어깨·팔",
        "en": "Shoulder · Arm",
        "cardio": true,
        "items": [
          {
            "name": "시티드 페이스풀",
            "en": "Seated Face Pull",
            "tag": "워밍업",
            "tip": "팔꿈치 높게 얼굴 쪽으로",
            "sets": [
              [
                20,
                10
              ],
              [
                15,
                15
              ]
            ]
          },
          {
            "name": "사이드 레터럴 레이즈",
            "en": "Lateral Raise",
            "tag": "워밍업",
            "tip": "어깨 으쓱 금지",
            "sets": [
              [
                20,
                4
              ],
              [
                15,
                4
              ]
            ]
          },
          {
            "name": "숄더 프레스 머신",
            "en": "Shoulder Press",
            "tag": "메인",
            "tip": "허리 등받이에 붙이기",
            "sets": [
              [
                15,
                20
              ],
              [
                12,
                20
              ],
              [
                10,
                25
              ],
              [
                8,
                25
              ]
            ]
          },
          {
            "name": "사이드 레터럴 레이즈 머신",
            "en": "Standing Machine",
            "tip": "팔꿈치로 들어 올리기",
            "sets": [
              [
                15,
                10
              ],
              [
                15,
                10
              ],
              [
                15,
                10
              ]
            ]
          },
          {
            "name": "덤벨 컬",
            "en": "DB Curl",
            "tip": "팔꿈치 고정",
            "sets": [
              [
                12,
                6
              ],
              [
                12,
                6
              ],
              [
                12,
                6
              ]
            ]
          },
          {
            "name": "해머 컬",
            "en": "Hammer Curl",
            "tip": "엄지가 위로",
            "sets": [
              [
                12,
                6
              ],
              [
                12,
                6
              ],
              [
                12,
                6
              ]
            ]
          }
        ]
      },
      {
        "day": "금",
        "part": "가슴·등",
        "en": "Chest · Back",
        "cardio": true,
        "items": [
          {
            "name": "인클라인 덤벨 프레스",
            "en": "Incline DB Press",
            "tag": "메인",
            "tip": "윗가슴으로 밀기",
            "sets": [
              [
                15,
                6
              ],
              [
                12,
                6
              ],
              [
                10,
                8
              ],
              [
                8,
                8
              ]
            ]
          },
          {
            "name": "플랫 덤벨프레스",
            "en": "Flat DB Press",
            "tip": "덤벨은 가슴 옆까지",
            "sets": [
              [
                12,
                8
              ],
              [
                12,
                8
              ],
              [
                12,
                8
              ]
            ]
          },
          {
            "name": "랫풀다운",
            "en": "Lat Pulldown",
            "tip": "팔꿈치로 당기기",
            "sets": [
              [
                12,
                30
              ],
              [
                12,
                30
              ],
              [
                12,
                30
              ]
            ]
          },
          {
            "name": "뉴텍 시티드 로우 머신",
            "en": "Seated Row Machine",
            "tip": "가슴 패드 붙이고 당기기",
            "sets": [
              [
                12,
                30
              ],
              [
                12,
                30
              ],
              [
                12,
                30
              ]
            ]
          }
        ]
      },
      {
        "day": "토",
        "part": "하체 B",
        "en": "Legs B",
        "cardio": false,
        "items": [
          {
            "name": "레그 익스텐션",
            "en": "Leg Extension",
            "tag": "워밍업",
            "tip": "가볍게 무릎 풀기",
            "sets": [
              [
                20,
                15
              ],
              [
                15,
                20
              ]
            ]
          },
          {
            "name": "이너타이",
            "en": "Inner Thigh",
            "tag": "선행",
            "tip": "세트마다 무게 ↑",
            "sets": [
              [
                20,
                20
              ],
              [
                15,
                25
              ],
              [
                12,
                30
              ]
            ]
          },
          {
            "name": "아웃타이 머신",
            "en": "Outer Thigh",
            "tag": "선행",
            "tip": "세트마다 무게 ↑",
            "sets": [
              [
                20,
                20
              ],
              [
                15,
                25
              ],
              [
                12,
                30
              ]
            ]
          },
          {
            "name": "고블릿 스쿼트",
            "en": "Goblet Squat",
            "tag": "선행",
            "tip": "가슴 세우고 깊이 앉기",
            "sets": [
              [
                20,
                6
              ],
              [
                15,
                8
              ],
              [
                12,
                10
              ]
            ]
          },
          {
            "name": "핵스쿼트",
            "en": "Hack Squat",
            "tag": "메인",
            "tip": "등 패드에 붙이고",
            "sets": [
              [
                15,
                15
              ],
              [
                12,
                15
              ],
              [
                10,
                20
              ],
              [
                8,
                20
              ]
            ]
          },
          {
            "name": "레그프레스 (발 높게)",
            "en": "Leg Press · High",
            "tip": "뒤꿈치로 밀기",
            "sets": [
              [
                12,
                40
              ],
              [
                12,
                40
              ],
              [
                12,
                40
              ]
            ]
          }
        ]
      },
      {
        "day": "일",
        "part": "휴식",
        "en": "Rest",
        "rest": true,
        "items": []
      }
    ]
  },
  "diet": {
    "updated": "2026. 11. 5",
    "title": "다이어트 식단",
    "title_en": "Diet Meal Plan · 골라 먹는 식단 · 80kg대 남성",
    "rules": [
      "아침·저녁 탄수화물 1종",
      "아침·저녁 단백질 1종",
      "점심은 일반식, 밥 2/3공기"
    ],
    "rules_note": "양만 지키면 메뉴는 끼니마다 바꿔도 OK",
    "key_point": "점심은 편하게, 아침·저녁은 정확하게!",
    "stats": [
      {
        "label": "하루 칼로리",
        "value": "2,050",
        "unit": "kcal"
      },
      {
        "label": "하루 단백질",
        "value": "160",
        "unit": "g"
      },
      {
        "label": "하루 식사",
        "value": "3끼",
        "unit": "+ 1잔"
      },
      {
        "label": "하루 물",
        "value": "2~3",
        "unit": "L"
      }
    ],
    "formula": [
      {
        "icon": "rice_white",
        "title": "탄수화물",
        "sub": "1종"
      },
      {
        "icon": "chicken",
        "title": "단백질",
        "sub": "1종"
      },
      {
        "icon": "veg",
        "title": "채소",
        "sub": "듬뿍"
      }
    ],
    "formula_result": {
      "title": "한 끼 완성",
      "sub": "아침 · 저녁 2번"
    },
    "carbs": [
      {
        "icon": "sweet_potato",
        "name": "고구마",
        "amount": "240g"
      },
      {
        "icon": "rice_white",
        "name": "쌀밥",
        "amount": "200g (1공기)"
      },
      {
        "icon": "rice_brown",
        "name": "현미밥",
        "amount": "200g (1공기)"
      },
      {
        "icon": "potato",
        "name": "감자",
        "amount": "400g"
      },
      {
        "icon": "oatmeal",
        "name": "오트밀",
        "amount": "80g"
      }
    ],
    "prots": [
      {
        "icon": "chicken",
        "name": "닭가슴살",
        "amount": "200g"
      },
      {
        "icon": "beef",
        "name": "우둔·홍두깨살",
        "amount": "200g"
      },
      {
        "icon": "fish",
        "name": "흰살생선",
        "amount": "240g"
      },
      {
        "icon": "egg",
        "name": "계란",
        "amount": "전란 2개 + 흰자 8개"
      },
      {
        "icon": "pork",
        "name": "돼지 안심",
        "amount": "200g"
      },
      {
        "icon": "tofu",
        "name": "두부",
        "amount": "1모 (500g)"
      },
      {
        "icon": "shrimp",
        "name": "새우",
        "amount": "240g"
      }
    ],
    "day_sub": "3끼 + 프로틴 1잔",
    "day": [
      {
        "icon": "ic_sun",
        "name": "아침",
        "line1": "탄수 1종 + 단백 1종",
        "line2": "+ 채소 듬뿍"
      },
      {
        "icon": "ic_tray",
        "name": "점심",
        "line1": "일반식",
        "line2": "밥은 2/3공기만"
      },
      {
        "icon": "ic_moon",
        "name": "저녁",
        "line1": "탄수 1종 + 단백 1종",
        "line2": "자기 3시간 전까지"
      },
      {
        "icon": "ic_shaker",
        "name": "프로틴",
        "line1": "물에 1스쿱",
        "line2": "운동 끝나고 바로 마셔요",
        "line3": "쉬는 날엔 오후 간식 대신"
      }
    ],
    "lunch_do": [
      "밥은 2/3공기만, 남겨도 괜찮아요",
      "제육·생선구이·불고기처럼 고기 반찬 메뉴",
      "채소 반찬부터 먼저 먹기",
      "국은 건더기 위주로 떠먹기"
    ],
    "lunch_dont": [
      "짜장·짬뽕·라면 같은 면 메뉴",
      "돈가스·튀김 정식",
      "공기밥 추가, 국에 밥 말기",
      "식후 믹스커피·단 음료"
    ],
    "extras": [
      {
        "icon": "veg",
        "name": "채소",
        "tag": "매 끼 듬뿍",
        "lines": [
          "양배추·브로콜리·상추 등",
          "김치도 OK (조금만)",
          "아침·저녁 한 접시씩"
        ]
      },
      {
        "icon": "ic_water",
        "name": "음료",
        "tag": "물 2~3L",
        "lines": [
          "물·탄산수·블랙커피 OK",
          "주스·라떼·탄산음료 X"
        ]
      },
      {
        "icon": "salt",
        "name": "염분 조절",
        "tag": "조금은 OK",
        "lines": [
          "소금·소스는 찍어 먹기",
          "김치·국물은 조금만"
        ]
      }
    ],
    "notes_title": "참고사항",
    "notes_sub": "식단 양은 혼자 바꾸지 말고 트레이너와 함께 정해요",
    "notes": [
      {
        "icon": "ic_scale",
        "title": "인바디 측정",
        "chip": "한 달에 1번",
        "desc": "매달 같은 시기, 아침 공복에 재요"
      },
      {
        "icon": "talk",
        "title": "트레이너와 상담",
        "chip": "결과 같이 보기",
        "desc": "체지방·근육량 변화를 함께 확인해요"
      },
      {
        "icon": "clipboard",
        "title": "식단 수정",
        "chip": "새 식단표",
        "desc": "결과에 맞춰 탄수·단백 양을 다시 정해요"
      }
    ],
    "safety": "끼니를 굶지 마세요. 굶으면 저녁에 폭식해요. 어지럽거나 힘이 빠지면 바로 트레이너에게 알려 주세요"
  }
};
