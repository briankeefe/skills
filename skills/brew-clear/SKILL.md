---
name: brew-clear
description: Write, revise, or review a Brew article or page in Brian's voice. Use for Brew content, diagrams, and article edits, especially when the audience needs a short, self-contained explanation without jargon or AI slop.
---

# Brew, clearly

Read `skill://brian-voice` and the Brew repository's `AUTHORING.md` before writing. Write as **Brian explaining work to colleagues**, never as an assistant replying to Brian. Assume the reader hasn't seen the ticket, chat, or earlier draft.

- Lead with the answer: what changed or was learned, why it matters, and how certain we are. Define the problem before comparing attempts or saying “the first result.”
- Keep it short. Prefer a few purposeful sections, brief paragraphs, and one useful table over a lab notebook. Cut repeated conclusions, process chronology, and details that don't change the takeaway. More length is justified only by a reader's real question.
- Ground claims in the source. Separate observed results, interpretation, and untested recommendations. Include the denominator, important failure modes, data/privacy boundaries, and what still needs validation. Don't dress a small exploratory result up as a production verdict.
- Use Brian's natural, direct phrasing. Replace vague labels and jargon with what a person actually does or sees. No generic openers, self-congratulation, inflated adjectives, or paragraphs that merely restate a table. If a sentence could fit any project, delete or make it specific.
- Use a diagram only when it clarifies a real flow. Label nodes as plain actions, inputs, or outcomes (for example, “Compare the policy with the customer's billing history,” not “Match locally”). Make public/model inputs and private/customer inputs visibly distinct. Describe the decision branches in words a new reader understands. Prefer a vertical layout if a wide diagram shrinks inside the article; check the rendered result at the actual page width. Provide an accessible Mermaid title and description.
- Final pass: read the opening and diagram as someone new to the project. Can they explain the system and the decision without your narration? Remove any sentence, box, or section that repeats an answer. Validate Brew content and inspect the rendered page after edits.
