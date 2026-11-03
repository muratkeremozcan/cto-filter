---
name: cto-filter
description: Reviews and repairs professional messages, decks, documents, and emails before they are sent. Use when the user says "communication filter," "CTO filter," "filter this before I send it," or asks whether workplace communication is ready. Also trigger for leadership updates, cross-team rollouts, escalations, incident responses, private workplace criticism, named holdouts, or claims that need Jira and GitHub evidence. Applies the communication gates to every company channel, then adds executive cold-read gates when the audience is a leader.
---

# Communication and CTO Filter

Treat every company message as quotable, including private channels. Preserve the writer's technical truth while removing language and routing choices that create avoidable trust or ownership problems.

It serves two modes:

1. The communication filter runs for every workplace artifact.
2. The leadership filter adds executive cold-read checks for a CTO, CEO, VP, director, or manager.

## Required input

Confirm that the real artifact is present as pasted text, a file, or a specific thread. A summary of the artifact cannot receive a reliable verdict. Ask for the actual artifact when it is missing.

Identify the audience and channel. Use available context when the answer is already known. Ask one precise question only when audience, ownership, or incident context would change the verdict.

Never send or post on the user's behalf unless the user explicitly asks for that action.

## Route the review

Run the core communication gates every time. Add the relevant specialized gates:

- Leadership audience: run the executive gates and signal-placement check.
- Cross-team change or rollout: run ownership, routing, and fleet-visibility checks.
- Incident or disruption: run the impact-first check.
- Status or accomplishment report: run evidence traceability and lever checks.

## Core communication gates

Score each gate as PASS, FAIL, or UNKNOWN. Attach the exact correction to every FAIL. Name the missing fact for every UNKNOWN.

1. **Observable facts:** Describe behavior, state, dates, and impact. Distinguish observations from inference and keep genuine uncertainty. Remove character judgments, contempt, and unsupported motive claims. Character and motive words such as `lazy`, `incompetent`, `rubberstamp`, and `doesn't care` require observable evidence or removal.
2. **Ownership consent:** Before changing another team's repository, confirm the real owner and explicit go-ahead. Approvals from people who do not own the repository do not establish consent.
3. **Impact first:** When a change disrupted someone, acknowledge the recipient's impact before explaining mechanism, intent, or the fix.
4. **Routing discipline:** Use one owner, one primary channel, and one agreed follow-up date. Give the owner one week unless urgency or an incident requires a shorter window. Escalate to the writer's manager before opening a second public route.
5. **Human decision boundary:** Preserve owner judgment where the owner controls risk, priority, exception, or local design. Automate repeated policy, mechanical verification, and state collection.
6. **Fleet visibility:** Let a dashboard or status page expose rollout state. Remove public callouts of the final holdouts and avoid mass tagging reviewers.
7. **Materiality:** Correct a disputed detail when it changes ownership, accountability, incident classification, or the next action. State a non-material correction once, accept the operating feedback, and move forward.
8. **Private-channel safety:** Apply the same professional standard in DMs and private groups as in public channels. Convert raw frustration into the event, its impact, and the requested next step.
9. **Narrative balance:** Keep delivery metrics. Remove the `I delivered, they blocked` storyline. Name dependencies and decisions without turning colleagues into the opposing side.

## Evidence traceability

For status reports, accomplishments, spend summaries, and shipped-work claims:

- Trace each number to a named source, date range, or reproducible query.
- Link each GitHub activity claim to its Jira issue when company policy expects a ticket.
- Flag work with no Jira home. Recommend the correct initiative or a new initiative before calling the report complete.
- Separate merged, open, delivered, and planned work in every completion claim.
- Lead with the full true scope and state the filtering rule beside it.

## Executive gates

Use the reader's known priorities from the conversation or the writer's notes. When none are known, mark the priorities gate UNKNOWN.

1. **Priorities:** Map the artifact to a named priority. State an honest miss when no connection exists.
2. **Math:** Source every number through a ticket, link, date range, count, or named origin.
3. **Format:** Present the problem, solution, next step, then stop. Remove repeated framing.
4. **Political wall:** If action spans organizations, make the cross-org sponsorship ask explicit.
5. **Approval boundary:** State what the writer owns, what decision the reader owns, and any genuine external dependency.
6. **Lever:** End with a concrete decision, approval, resource, owner, or next action the reader can provide.

## Signal placement

The most important outcome and requested action must be visible in the first sentence, slide title, or subject line. A reader who stops after that line should still understand the result and the ask.

## Voice pass

These checks are specific to this filter. The de-AI pass below owns the general tells.

- Replace vague `we` with the actual owner when ownership matters.
- Replace `guess`, `hope`, and `should` with a known fact, open question, requirement, or feasibility question.
- Keep peer messages one or two sentences when the task permits.
- Do not add rhetoric, marketing language, or claims unsupported by the source artifact.
- For technical prose, load `~/.claude/skills/de-ai/references/technical-writing.md` and apply its sentence checks.
  Use its document modes for documentation only; keep messages in their channel's form and length.

## De-AI pass

After the gates pass and before returning the draft, run the `de-ai` skill over the text. Load `~/.claude/skills/de-ai/references/ai-tells.md` and `~/.claude/skills/de-ai/references/murat-voice.md` and apply all four passes: tells, bloat, voice, line structure. Those two files own the dash, antithesis, slogan, label-colon, blockquote, and formatting rules, so this skill does not restate them.

Two things this filter has gotten wrong before, so check them explicitly on the way out:

- Tightening a soft offer must not introduce calendar-bot phrasing. "happy to pair if useful" became "want to grab 30 minutes this week?" and that was worse. See tell 5 in `ai-tells.md`.
- The draft must come back at the writer's length or shorter, unless missing evidence requires a compact addition. This filter adds structure; structure is not a licence to add lines.

Fold the tells found into the gate results as one line with the count. Any unfixed tell makes the verdict REVISE.
After the voice edit, confirm that the rewrite preserves the original conditions, completion states, ownership, uncertainty, and requested decision.
Keep missing evidence visible in the verdict and evidence gaps; a shorter draft cannot resolve an UNKNOWN gate.

## Output

Return these sections in order:

1. **Verdict:** Use exactly READY, REVISE, or STOP. Do not invent another verdict label.
2. **Gate results:** one concise line per applicable gate, including the exact fix for each failure, plus one line for the de-AI pass with the count of tells removed.
3. **Evidence gaps:** Jira links, GitHub links, dates, owners, or sources still required. Omit when empty.
4. **Sendable version:** a corrected artifact that preserves the writer's facts and voice. Include it whenever the verdict is REVISE. For STOP, provide the safe partial draft and name the blocking fact.
5. **Cold-read lead:** one sentence for leadership artifacts only. It must carry the key outcome and requested action.

Be direct.
