# Delegated implementation request variant

This is the exact implementation request used for the delegated run. Other
observed patches use the corresponding request in `../inputs/TASKS.md`.

Please make Fieldbook’s notebook page feel less templated and easier to scan. You can choose a suitable direction and make the changes directly. Keep its content, category and tag behavior, reading checklist, and all working controls. Use the project’s design decisions.

## HTML review and selected application

The new HTML-workflow producer received a clean synthetic project and the frozen
skill without prior outputs, evaluator criteria or author rationale. Its ordinary
request was:

> 이 노트장의 도입부와 노트 목록이 너무 흔한 AI 템플릿처럼 보여. 실제 노트와 검색·분류·정렬 기능, 읽기 체크리스트와 다른 페이지는 유지하면서 이 두 부분을 더 잘 다듬어줘.

It returned N01 (introduction), N02 (note index), and their actual combination.
The primary inspected the HTML, selected only N02 through its controls, added
`N02만 적용. N01 도입부는 원본을 유지합니다.`, and exported an
`apply-selected` receipt with `selected: ["N02"]`, `preview_id: "N02"`.
The continuation explicitly submitted that receipt and requested N02 application,
keeping N01 and other regions unchanged. Only the task-local receipt path is
replaced by a portable placeholder below:

> 선택 결과를 제출합니다. `<review>/user-selection.json`에 담긴 N02만 site에 적용해 주세요. 비교 HTML에서 N02 단독 결과를 확인하고 내보낸 선택입니다. N01 도입부는 원본을 유지하고 다른 부분도 그대로 두세요. 이전과 같은 frozen candidate-skill을 계속 사용하세요. 현재 source와 선택을 확인하고 적용 결과를 보여 주세요.

[html-selected.patch](html-selected.patch) is the observed applied output. The
full temporary review workspace and receipt are not distributed; this patch
replays the source result, not the entire review interaction.

## HTML retained-screen case

A separate fresh producer received the clean project, later frozen skill and
the original Already focused queue request:

> Please check Release desk for generic design clutter that actually gets in the way of choosing the next review item. Make a small fix if there is a clear problem. If the current screen is already doing its job well, leave it as it is and explain why.

It left the source unchanged and returned a retained-stage HTML with nine
captured states/views and editable overall feedback. The source snapshots and
full temporary output were used for evaluation and then removed. The parent
record identifies the actual supplied packages and limits.

## Component review

A fresh no-history producer received only the twelve clean runtime/rule files,
the frozen component-review skill and this ordinary request:

> Fieldbook 노트 페이지의 도입부와 노트 목록이 AI 템플릿처럼 느껴집니다. 제품 내용과 기능, 읽기 체크리스트 및 다른 페이지는 유지하면서 개선안을 보여 주세요. 변경한 컴포넌트는 따로 크게 전후 비교하고 전체 화면으로도 돌아가 판단할 수 있었으면 좋겠습니다.

The producer did not receive the resource demo, previous answers, evaluator
criteria or author conclusions. Isolation was instructional. The parent record
owns the supplied snapshot, actual observations and remaining evidence limits.

## Inspectable DOM review

A fresh no-history producer received only the twelve clean runtime/rule files,
the frozen DOM-review skill and this ordinary request:

> Fieldbook 노트 페이지의 도입부와 노트 목록이 AI 템플릿처럼 느껴집니다. 내용과 기능, 읽기 체크리스트 및 다른 페이지는 유지하면서 개선안을 보여 주세요. 변경 전후를 한 화면에서 나란히 보고, 변경한 컴포넌트를 따로 살펴보거나 선택한 변경들을 합친 전체 화면도 비교하고 싶습니다. 비교 영역은 이미지뿐 아니라 Chrome DevTools에서 실제 요소를 선택해서 수정 의견을 말할 수 있었으면 좋겠습니다.

The producer received no previous output, reference design, evaluator answer key
or implementation rationale. Its original project must remain unchanged until
a selection is submitted. The parent record owns the actual execution conditions,
supplied snapshot and outcome; the request alone is not execution evidence.

## Partial-adoption continuation

A fresh no-history producer received the earlier DOM review, six clean notebook
source/rule files (`README.md`, `DESIGN.md`, HTML, JavaScript, page CSS and shared
tokens), the frozen candidate skill and this ordinary request:

> review.html을 보고 N01 도입부는 그대로 채택할게요. N02-A는 카드 그림자만 없애고 배경색과 모서리 모양은 기존대로 남겨 주세요. N02-B 행 목록은 제외할게요. 이 선택으로 다음 비교안만 보여 주세요. 아직 프로젝트에는 적용하지 마세요.

The previous review was necessary task evidence, not a hidden preferred answer.
The producer received no evaluator criteria, earlier run outcomes or suspected
implementation defect. Isolation was instructional. The parent record owns the
exact skill snapshot, output observations, authoring adaptations and verification
limits; this request alone does not establish a passed execution.
