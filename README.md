# Web-Crawling

## Daum Movie Review와 Steam Game Review
### Daum Movie Review
  - Daum Movie는 loop를 돌려서 진행할 수 있지만, 인기영화가 아닌 이상 많은 User Review를 기대하기 힘들다.
  - 즉, 데이터가 많이 모이지 않는다.
  - 다음 웹에서 검색을 한 뒤에 url을 보면 movie id가 있기 때문에 그것을 이용해 Review를 가져온다.

### Stream Game Review
  - Scroll의 횟수를 정해서 모든 것을 자동화하여 Review를 가져온다.
  - 인기 게임 목록을 기반으로 하기 때문에 많은 자동화하여도 많은 수의 User Review를 가져올 수 있다.

### Youtube Comments
  - 핫셀러 OJT로 간단하게 ChatGPT 댓글 Bot을 구현
  - config에 있는 keyword를 youtube에서 검색 후 동영상의 댓글을 가져와 chatgpt에게 비슷한 댓글을 생성하라고 요청한다.
  - chatgpt의 response를 댓글로 입력하게하는 간단한 웹 매크로 프로그램
