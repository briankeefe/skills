# Explaining the approach

How to write the Brew explanation page for the **Pre-work Socratic checkpoint** in `skill://execute`.
Create or update it with `skill://brew-clear`, verify the rendered page, then send only the takeaway,
page link and agreement question in chat. Keep it separate from the UI-only testing guide.

## Reader

A developer who can follow code but is new to this task's domain and product. The goal is that
they can explain what normally happens, what goes wrong, why, and how the fix changes the result.
Unfamiliar domain concepts are the hard part, not the programming.

## Content, in order

1. **Context and normal behavior.** The few concepts and relationships this task needs, with
   domain terms defined at first use: who does what, and what a number or document means. Teach
   the relationship, not a plainer synonym. For example, distinguish money from reports describing
   that money, or a policy from its dated revisions and their stored summaries and rules.
2. **Before.** One concrete example from its starting facts through current behavior to the wrong
   result and why it matters. Name the causal step that produces the failure, in terms of visible
   behavior rather than callbacks or tables. Separate reported facts from assumptions and label
   invented teaching numbers.
3. **After.** The same example through the proposed behavior: why the failure is gone, what stays
   unchanged and how success will be recognized. Don't invent a missing real amount; if stored
   content already exists, say so rather than implying new extraction. For discovery work,
   separate what the investigation delivers from a possible later product change.
4. **Flow and proposed fix.** One small labeled flowchart of the system's behavior (current and/or
   proposed) with plain-language actions and only meaningful branches. It shows the product, not
   the agent's work schedule, a review queue or fallback branches nobody proposed. Follow with the
   short engineering explanation, the recommendation and the decision needed. Detailed callers,
   tradeoffs and verification stay in the task plan or a short optional technical section.

## Style

Size to understanding: a simple UI change can be short; an unfamiliar payment calculation may need
a few more paragraphs. Use a few short labeled paragraphs and give each fact once. When cutting,
cut repeated safeguards, generic process language, test inventories and file lists before cutting
context the reader needs. Name whether this is a code PR, a data repair or both, and keep material
uncertainty, scope and risk. Keep key checks and the approval boundary brief.

Before sharing, reread the opening, before/after and diagram as a domain newcomer and add any
missing conceptual bridge. "Recognize repeated payment reports" still needs the sentence that two
reports may describe one payment. The reader should not need follow-up questions for prerequisites.

## Revisions

When the discussion changes the approach, update the same page. Feedback that the page is
confusing, too complex or poorly worded means rework the page and verify the rendered revision;
suggesting replacement prose in chat does not address it. A request to rewrite the explanation is
different from a request to stop implementation; honor an explicit stop-all.
