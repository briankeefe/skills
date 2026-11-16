---
name: brew-clear
description: Write, revise, or review a Brew article or page in Brian's voice. Use for Brew content, diagrams, and article edits, especially when the audience needs a short, self-contained explanation without jargon or AI slop.
---

# Brew, clearly

Read `skill://brian-voice` and the Brew repository's `AUTHORING.md` before writing. Write as **Brian explaining work to colleagues**, never as an assistant replying to Brian. Assume the reader hasn't seen the ticket, chat, or earlier draft.

Resolve the current local renderer from personal/project runtime guidance before serving.
Reuse its shared styles and theme controls; don't launch an older feature worktree's bundle
just because a preview already responds. Keep existing page URLs and assets when updating a
stale preview, and verify the rendered theme rather than only its HTTP status.

- Lead with the answer: what changed or was learned, why it matters, and how certain we are. Define the problem before comparing attempts or saying “the first result.”
- Keep it focused, not compressed. Prefer a few purposeful sections, brief paragraphs, and one useful table over a lab notebook. Cut repeated conclusions, process chronology, and implementation detail before cutting the context a new reader needs. Don't use a word target as a substitute for understanding.
- For proposed fixes, assume a developer who is new to the domain, not new to programming. Explain the necessary concepts and normal behavior first, then carry one concrete example through the failure and proposed result. Define terms through their relationships: two payment reports can describe one actual payment; a policy revision has its own stored summary and rules. A plainer synonym alone isn't an explanation. Label illustrative numbers and distinguish research deliverables from possible future features. Put engineering detail after the reader-facing story.
- Ground claims in the source. Separate observed results, interpretation, and untested recommendations. Include the denominator, important failure modes, data/privacy boundaries, and what still needs validation. Don't dress a small exploratory result up as a production verdict.
- Use Brian's natural, direct phrasing. Replace vague labels and jargon with what a person actually does or sees. No generic openers, self-congratulation, inflated adjectives, or paragraphs that merely restate a table. If a sentence could fit any project, delete or make it specific.
- Use a diagram only when it clarifies a real flow. Label nodes as plain actions, inputs, or outcomes (for example, “Compare the policy with the customer's billing history,” not “Match locally”). Make public/model inputs and private/customer inputs visibly distinct. Describe the decision branches in words a new reader understands. Prefer a vertical layout if a wide diagram shrinks inside the article; check the rendered result at the actual page width. Provide an accessible Mermaid title and description.
- Every authored link must open a fresh tab, not replace the Brew page or reuse a named tab. Markdown links get `target="_blank" rel="noopener"` from the Brew renderer. For raw HTML links in newly generated content, set those attributes explicitly. Check by clicking a rendered link twice: two new tabs should open and the Brew page should remain unchanged.
- Final pass: can someone new to the domain explain what normally happens, what goes wrong, why, and how the proposed fix changes the result without your narration? Supply missing conceptual bridges, not just shorter wording. Remove repeated answers. Validate Brew content and inspect the rendered page after edits.
