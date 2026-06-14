<!-- distilled from alfa skills/voice-interface -->
<!-- > -->
# Voice Interface
> "Method over hacks."
## TL;DR
Design speech-to-text (STT), text-to-speech (TTS), and turn-taking voice UI: latency budgets, barge-in, error recovery, and accessibility. [EXPLICIT]
## Procedure
### Step 1: Discover
- Capture: languages/accents, ambient noise, device (phone/IVR/car/wearable), hands-free vs. mixed, privacy/regulatory scope. [EXPLICIT]
- Define the latency budget end-to-end: STT partials < 300 ms, first TTS audio < 700 ms perceived. [INFERENCIA]
### Step 2: Analyze
- Choose streaming vs. batch STT (streaming for conversation, batch for transcription) per Constitution XIII/XIV. [EXPLICIT]
- Decide TTS tier: cached/SSML-templated for fixed prompts, neural streaming for dynamic replies; tag the trade-off. [INFERENCIA]
- Model dialog state, barge-in policy, and a fallback to DTMF/touch when STT confidence is low. [EXPLICIT]
### Step 3: Execute
- Stream partial transcripts; commit on endpointing (VAD silence 500–800 ms) not on fixed timeout. [INFERENCIA]
- Gate actions on STT confidence + intent confidence; below threshold → confirm or re-prompt, never act. [EXPLICIT]
- Use SSML for numbers, dates, currency, and pronunciation; never read raw tokens aloud. [EXPLICIT]
### Step 4: Validate
- Measure WER on in-domain audio, end-to-end latency, barge-in success, and task completion rate. [MÉTRICA]
- Verify quality criteria met. [EXPLICIT]
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Latency budget met (STT partial <300 ms, first audio <700 ms) [INFERENCIA]
- [ ] Low-confidence path confirms or re-prompts before any irreversible action [EXPLICIT]
- [ ] Accessible: visual transcript + non-voice fallback available [EXPLICIT]
- [ ] Actionable output

## Decisions & Trade-offs
| Decision | Choose when | Cost |
|----------|-------------|------|
| Streaming STT | Live conversation, barge-in needed | Higher infra cost, partial-result handling [INFERENCIA] |
| Batch STT | Offline transcription, no turn-taking | Unusable for dialog latency [EXPLICIT] |
| Cached/templated TTS | Fixed prompts, high volume | Rigid wording [EXPLICIT] |
| Neural streaming TTS | Dynamic, personalized replies | Cost + first-byte latency [INFERENCIA] |

## Usage

Example invocations:

- "/voice-interface" — Run the full voice interface workflow
- "voice interface on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Anti-scope: does not cover wake-word/keyword-spotting model training or telephony carrier provisioning [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Low STT confidence / heavy noise | Re-prompt or confirm; fall back to DTMF/touch, never act on guess [EXPLICIT] |
| User barge-in mid-TTS | Halt playback immediately, capture new utterance [EXPLICIT] |
| Silence / no speech (timeout) | Re-prompt once, then offer non-voice path or graceful exit [INFERENCIA] |
| Homophones, numbers, spelled names | Confirm via readback with SSML before committing [SUPUESTO] |
| Code-switching / mixed language | Detect locale per utterance or pin expected language to cut WER [INFERENCIA] |
