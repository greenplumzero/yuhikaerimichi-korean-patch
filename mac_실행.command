#!/bin/bash
cd "$(dirname "$0")"
chmod +x "./YuhiKaerimichiKoreanPatch" 2>/dev/null
"./YuhiKaerimichiKoreanPatch"
STATUS=$?
if [ $STATUS -ne 0 ]; then
  echo
  echo "실행 중 오류가 발생했습니다."
  read -p "Enter를 누르면 종료합니다..."
fi
